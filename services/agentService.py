"""
TripSplit assistant — routes a user's natural-language message through
claude-agent-sdk with a custom MCP tool server backed by existing
TripSplit services.

The Flask app context is captured up-front and re-entered inside the
async tool handlers, because the SDK invokes tools from a worker task
that doesn't share Flask's request context (and our DB session lives
on flask.g).
"""
import json
import logging

import anyio
from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    SdkMcpTool,
    TextBlock,
    ToolUseBlock,
    create_sdk_mcp_server,
    query,
)

from services.agentTools import build_tools

logger = logging.getLogger(__name__)

MCP_SERVER_NAME = "tripsplit"
MAX_TURNS = 10
MODEL = "haiku"  # Cheapest model that still handles tool-use well.

SYSTEM_PROMPT_TEMPLATE = """You are an assistant inside TripSplit, a trip expense-splitting app.

Current trip: "{trip_title}" (id: {trip_id})
Trip currencies (display only): {currencies}
Current user: "{current_user_name}" (userId: {current_user_id}, email: {current_user_email})

Trip members:
{members_block}

Rules:
- ALL amounts are in INR. The trip's currencies list is for display; ignore for math.
- The trip_id and current user are set automatically — never ask for them.
- When the user names someone, match it to a userId from the member list above. If ambiguous, ask which one.
- "split equally between N people for X" means each share is X/N.
- "I paid X for [people]" -> paidBy is the current user; splitBetween includes the current user and each named person.
- "Alice paid X, my share is Y" -> paidBy is Alice; splitBetween includes you with amount Y (and Alice with X-Y).
- selfExpense=true is for personal spending the user wants logged but not split (no balances created).
- Default date is today (YYYY-MM-DD) unless the user specifies otherwise.
- After making changes, reply tersely confirming what you did. After read queries, summarize directly.
- Don't dump raw JSON to the user. Format numbers as INR (₹) with two decimals.
- If you must clarify, ask ONE concise question.
"""


def _format_members(users, current_user_id):
    lines = []
    for u in users:
        marker = " (you)" if u['userId'] == current_user_id else ""
        lines.append(f"  - userId {u['userId']}: \"{u['userName']}\" <{u['email']}>{marker}")
    return "\n".join(lines) if lines else "  (no members yet)"


class TripAgentService:
    def __init__(self, tripUserService, expenseBalanceService,
                 notesService, individualSpendingService):
        self.tripUserService = tripUserService
        self.expenseBalanceService = expenseBalanceService
        self.notesService = notesService
        self.individualSpendingService = individualSpendingService

    def handle_message(self, app, trip_id, trip_title, currencies,
                       current_user_email, message, history):
        """
        Synchronously run a single turn against Claude and return a dict:
            {reply, mutations, tool_calls, error?}
        `app` is the Flask app so tool handlers can re-enter app_context().
        """
        users = self._with_ctx(app, lambda: self.tripUserService.fetchUserForTrip(trip_id))
        current_user_id = self._with_ctx(
            app, lambda: self.tripUserService.fetchUserIDFromEmail(current_user_email)
        )
        current_user_name = next(
            (u['userName'] for u in users if u['userId'] == current_user_id), 'You'
        )

        services = {
            'tripUserService': self.tripUserService,
            'expenseBalanceService': self.expenseBalanceService,
            'notesService': self.notesService,
            'individualSpendingService': self.individualSpendingService,
        }
        tools, mutation_names = build_tools(trip_id, current_user_id, services)

        sdk_tools = []
        tool_calls_log = []
        mutations = []

        for name, description, schema, handler in tools:
            sdk_tools.append(self._wrap_tool(
                name, description, schema, handler, app,
                tool_calls_log, mutations, mutation_names,
            ))

        mcp_server = create_sdk_mcp_server(name=MCP_SERVER_NAME, tools=sdk_tools)
        allowed = [f"mcp__{MCP_SERVER_NAME}__{name}" for name, *_ in tools]

        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
            trip_title=trip_title,
            trip_id=trip_id,
            currencies=", ".join(currencies) if currencies else "INR",
            current_user_name=current_user_name,
            current_user_id=current_user_id,
            current_user_email=current_user_email,
            members_block=_format_members(users, current_user_id),
        )

        options = ClaudeAgentOptions(
            system_prompt=system_prompt,
            mcp_servers={MCP_SERVER_NAME: mcp_server},
            permission_mode="bypassPermissions",
            max_turns=MAX_TURNS,
            model=MODEL,
            allowed_tools=allowed,
        )

        prompt_text = self._format_conversation(history, message)
        text_parts = []
        error = None

        async def run():
            nonlocal error
            async def make_prompt():
                yield {
                    "type": "user",
                    "session_id": "",
                    "message": {"role": "user", "content": prompt_text},
                    "parent_tool_use_id": None,
                }
            async for msg in query(prompt=make_prompt(), options=options):
                if isinstance(msg, AssistantMessage):
                    for block in msg.content:
                        if isinstance(block, TextBlock):
                            text_parts.append(block.text)
                        elif isinstance(block, ToolUseBlock):
                            pass  # logged inside the handler wrapper
                elif isinstance(msg, ResultMessage) and msg.is_error:
                    error = msg.result or "Query failed"

        try:
            anyio.run(run)
        except Exception as ex:
            logger.exception("Agent SDK run failed")
            error = f"{type(ex).__name__}: {ex}"

        return {
            "reply": "".join(text_parts).strip(),
            "mutations": mutations,
            "tool_calls": tool_calls_log,
            **({"error": error} if error else {}),
        }

    def _wrap_tool(self, name, description, schema, handler, app,
                   tool_calls_log, mutations, mutation_names):
        async def sdk_handler(args, _n=name, _h=handler):
            try:
                result = self._with_ctx(app, lambda: _h(args))
            except Exception as ex:
                logger.exception("Tool %s failed", _n)
                result = {"error": f"{type(ex).__name__}: {ex}"}
            tool_calls_log.append({"name": _n, "input": args, "result": result})
            if _n in mutation_names and not (isinstance(result, dict) and result.get('error')):
                mutations.append(_n)
            return {
                "content": [{
                    "type": "text",
                    "text": json.dumps(result, default=str),
                }]
            }
        return SdkMcpTool(
            name=name,
            description=description,
            input_schema=schema,
            handler=sdk_handler,
        )

    @staticmethod
    def _with_ctx(app, fn):
        """Run fn inside the Flask app context so g.db is available."""
        from flask import g
        with app.app_context():
            g.db = app.db  # mirror what _setup_hooks does for requests
            return fn()

    @staticmethod
    def _format_conversation(history, latest):
        history = history or []
        if not history:
            return latest
        lines = []
        for msg in history:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            if not isinstance(content, str):
                content = str(content)
            prefix = 'User' if role == 'user' else 'Assistant'
            lines.append(f"{prefix}: {content}")
        return "Previous conversation:\n" + "\n".join(lines) + f"\n\nUser's latest message: {latest}"
