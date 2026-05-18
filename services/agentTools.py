"""
Tool definitions for the TripSplit assistant.

Each entry pairs a JSONSchema (what Claude sees) with a thin executor
that delegates to existing services. The set is intentionally small —
covering both reads and the common writes (add expense, delete expense,
add note). All actions are scoped to a single trip; the trip_id is
threaded through closure, not exposed as a tool parameter.
"""
from datetime import datetime


def build_tools(trip_id, current_user_id, services):
    """
    Returns a list of (name, description, input_schema, handler) tuples.
    `services` is a dict with keys: tripUserService, expenseBalanceService,
    notesService, individualSpendingService.
    """
    tripUserService = services['tripUserService']
    expenseBalanceService = services['expenseBalanceService']
    notesService = services['notesService']
    individualSpendingService = services['individualSpendingService']

    MUTATIONS = {'add_expense', 'delete_expense', 'add_note'}

    def _list_users(_args):
        return tripUserService.fetchUserForTrip(trip_id)

    def _list_expenses(_args):
        return expenseBalanceService.fetchExpensesForTrip(trip_id)

    def _list_balances(_args):
        return expenseBalanceService.fetchBalanceV2(trip_id)

    def _individual_balance(_args):
        return expenseBalanceService.fetchIndividualBalance(trip_id)

    def _individual_spending(_args):
        return individualSpendingService.fetchIndividualSpending(trip_id)

    def _list_notes(args):
        page = int(args.get('page', 1))
        return notesService.fetchNotesForATrip(trip_id, page)

    def _add_expense(args):
        split = args['splitBetween']
        total = float(args['amount'])
        sum_split = round(sum(float(s['amount']) for s in split), 2)
        if abs(sum_split - round(total, 2)) > 0.01 and not args.get('selfExpense'):
            return {
                'ok': False,
                'error': f'splitBetween amounts ({sum_split}) must sum to total ({total}).',
            }
        payload = {
            'tripId': trip_id,
            'date': args.get('date') or datetime.utcnow().strftime('%Y-%m-%d'),
            'description': args['description'],
            'amount': total,
            'paidBy': int(args['paidBy']),
            'splitbw': [{'userId': int(s['userId']), 'amount': float(s['amount'])} for s in split],
            'selfExpense': bool(args.get('selfExpense', False)),
        }
        ok = expenseBalanceService.addExpenseForTrip(payload)
        return {'ok': bool(ok)}

    def _delete_expense(args):
        return {'ok': bool(expenseBalanceService.deleteExpenseFromTrip(int(args['expenseId'])))}

    def _add_note(args):
        notesService.createNote({
            'userId': current_user_id,
            'tripId': trip_id,
            'note': args['note'],
        })
        return {'ok': True}

    tools = [
        (
            'list_users',
            'List all users in the current trip with userId, userName, email.',
            {'type': 'object', 'properties': {}, 'required': []},
            _list_users,
        ),
        (
            'list_expenses',
            'List every expense in the current trip with id, date, description, amount (INR), paidBy userId, and splitBetween dict of userId -> share amount.',
            {'type': 'object', 'properties': {}, 'required': []},
            _list_expenses,
        ),
        (
            'list_balances',
            'List the minimum-transaction settlement plan: an array of {from, to, amount} entries showing who needs to pay whom in INR.',
            {'type': 'object', 'properties': {}, 'required': []},
            _list_balances,
        ),
        (
            'individual_balance',
            'Net amount each user is owed (positive) or owes (negative) after all expenses are split. Returns {expense: {userId: amount}, selfExpense: {userId: amount}, total: number}.',
            {'type': 'object', 'properties': {}, 'required': []},
            _individual_balance,
        ),
        (
            'individual_spending',
            'How much each user has actually paid out of pocket on this trip (sum of expenseAmount where they were the payer).',
            {'type': 'object', 'properties': {}, 'required': []},
            _individual_spending,
        ),
        (
            'list_notes',
            'Paginated list of free-form notes attached to the trip. 10 per page.',
            {
                'type': 'object',
                'properties': {'page': {'type': 'integer', 'minimum': 1, 'default': 1}},
                'required': [],
            },
            _list_notes,
        ),
        (
            'add_expense',
            (
                'Add a new expense. All amounts are in INR. paidBy is a userId. '
                'splitBetween is an array of {userId, amount}; amounts must sum to the total amount unless selfExpense=true. '
                'selfExpense=true is for a personal expense the user wants to track without splitting (no balances are created).'
            ),
            {
                'type': 'object',
                'properties': {
                    'description': {'type': 'string'},
                    'amount': {'type': 'number', 'description': 'Total in INR'},
                    'paidBy': {'type': 'integer', 'description': 'userId of the payer'},
                    'splitBetween': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'userId': {'type': 'integer'},
                                'amount': {'type': 'number'},
                            },
                            'required': ['userId', 'amount'],
                        },
                    },
                    'date': {'type': 'string', 'description': 'ISO date YYYY-MM-DD; defaults to today.'},
                    'selfExpense': {'type': 'boolean', 'default': False},
                },
                'required': ['description', 'amount', 'paidBy', 'splitBetween'],
            },
            _add_expense,
        ),
        (
            'delete_expense',
            'Delete an expense from the trip by expenseId.',
            {
                'type': 'object',
                'properties': {'expenseId': {'type': 'integer'}},
                'required': ['expenseId'],
            },
            _delete_expense,
        ),
        (
            'add_note',
            'Add a free-form note to the trip. Notes are attributed to the current user.',
            {
                'type': 'object',
                'properties': {'note': {'type': 'string'}},
                'required': ['note'],
            },
            _add_note,
        ),
    ]
    return tools, MUTATIONS
