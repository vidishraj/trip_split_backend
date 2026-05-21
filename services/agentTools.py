"""
Tool definitions for the TripSplit assistant.

Each entry pairs a JSONSchema (what Claude sees) with a thin executor
that delegates to existing services. The set is intentionally small —
covering both reads and the common writes (add expense, delete expense,
add note). All actions are scoped to a single trip; the trip_id is
threaded through closure, not exposed as a tool parameter.

Money: amounts can be denominated in any supported currency code
(`inr`, `usd`, `eur`, `gbp`, `aud`, `thb`, etc.). The tools convert to
INR server-side before persisting — the model never has to do FX math.
"""
from datetime import datetime, timezone

from services.fxService import to_inr, get_rates


def build_tools(trip_id, current_user_id, services):
    """
    Returns (tools, mutation_names) where tools is a list of
    (name, description, input_schema, handler) tuples.
    """
    tripUserService = services['tripUserService']
    expenseBalanceService = services['expenseBalanceService']
    notesService = services['notesService']
    individualSpendingService = services['individualSpendingService']

    MUTATIONS = {'add_expense', 'delete_expense', 'add_note', 'record_settlement'}

    # ─── reads ───────────────────────────────────────────────────────
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

    def _fx_rates(_args):
        rates = get_rates()
        # Return rates as "1 unit of X = N INR" — the human-facing direction.
        return {
            currency.upper(): round(1.0 / rate, 4) if rate else None
            for currency, rate in rates.items()
        }

    # ─── writes ──────────────────────────────────────────────────────
    def _add_expense(args):
        try:
            currency = (args.get('currency') or 'inr').lower()
            raw_amount = float(args['amount'])
            if raw_amount <= 0:
                return {'ok': False, 'error': 'amount must be > 0'}

            # Convert per-user split amounts in the source currency to INR
            # using the same rate as the total. This avoids rounding drift.
            split = args['splitBetween'] or []
            if not split:
                return {'ok': False, 'error': 'splitBetween must not be empty'}

            paidBy = int(args['paidBy'])
            split_norm = []
            for s in split:
                uid = int(s['userId'])
                amt = float(s['amount'])
                if amt < 0:
                    return {'ok': False, 'error': 'split amounts must be non-negative'}
                split_norm.append({'userId': uid, 'amount': amt})

            split_sum = round(sum(s['amount'] for s in split_norm), 2)
            self_expense = bool(args.get('selfExpense', False))
            if not self_expense and abs(split_sum - round(raw_amount, 2)) > 0.01:
                return {
                    'ok': False,
                    'error': (
                        f'splitBetween sum ({split_sum}) must equal amount ({raw_amount}) '
                        f'(in source currency {currency.upper()})'
                    ),
                }

            # Convert all amounts to INR before persisting.
            try:
                inr_total = to_inr(raw_amount, currency)
                inr_split = [
                    {'userId': s['userId'], 'amount': to_inr(s['amount'], currency)}
                    for s in split_norm
                ]
            except ValueError as ve:
                return {'ok': False, 'error': str(ve)}

            payload = {
                'tripId': trip_id,
                'date': args.get('date') or datetime.now(timezone.utc).strftime('%Y-%m-%d'),
                'description': args['description'],
                'amount': inr_total,
                'paidBy': paidBy,
                'splitbw': inr_split,
                'selfExpense': self_expense,
            }
            ok = expenseBalanceService.addExpenseForTrip(payload)
            if not ok:
                return {
                    'ok': False,
                    'error': 'persist failed — split may not balance or DB rejected the write',
                }
            return {
                'ok': True,
                'currency': currency.upper(),
                'amount_in_inr': round(inr_total, 2),
                'amount_in_source': round(raw_amount, 2),
            }
        except KeyError as ke:
            return {'ok': False, 'error': f'missing required field {ke}'}
        except (ValueError, TypeError) as ex:
            return {'ok': False, 'error': str(ex)}

    def _delete_expense(args):
        try:
            ok = expenseBalanceService.deleteExpenseFromTrip(
                int(args['expenseId']), trip_id,
            )
            if not ok:
                return {'ok': False, 'error': 'expense not found in this trip'}
            return {'ok': True}
        except (ValueError, TypeError, KeyError) as ex:
            return {'ok': False, 'error': str(ex)}

    def _add_note(args):
        try:
            notesService.createNote({
                'userId': current_user_id,
                'tripId': trip_id,
                'note': args['note'],
            })
            return {'ok': True}
        except KeyError as ke:
            return {'ok': False, 'error': f'missing required field {ke}'}

    def _record_settlement(args):
        """A settlement is just an expense where the debtor (paidBy) covers
        the creditor's owed amount. Implemented on top of addExpenseForTrip
        so balance accounting stays consistent.
        """
        try:
            currency = (args.get('currency') or 'inr').lower()
            from_user = int(args['fromUserId'])
            to_user = int(args['toUserId'])
            amount = float(args['amount'])
            if amount <= 0:
                return {'ok': False, 'error': 'amount must be > 0'}
            if from_user == to_user:
                return {'ok': False, 'error': 'fromUserId and toUserId must differ'}
            try:
                inr_amount = to_inr(amount, currency)
            except ValueError as ve:
                return {'ok': False, 'error': str(ve)}

            payload = {
                'tripId': trip_id,
                'date': args.get('date') or datetime.now(timezone.utc).strftime('%Y-%m-%d'),
                'description': args.get('description') or 'Settlement',
                'amount': inr_amount,
                'paidBy': from_user,
                'splitbw': [{'userId': to_user, 'amount': inr_amount}],
                'selfExpense': False,
            }
            ok = expenseBalanceService.addExpenseForTrip(payload)
            if not ok:
                return {'ok': False, 'error': 'persist failed'}
            return {
                'ok': True,
                'currency': currency.upper(),
                'amount_in_inr': round(inr_amount, 2),
                'amount_in_source': round(amount, 2),
            }
        except (ValueError, TypeError, KeyError) as ex:
            return {'ok': False, 'error': str(ex)}

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
            'fx_rates',
            'Current foreign-exchange rates expressed as 1 unit of X = N INR. Use to interpret amounts the user mentions in non-INR currencies.',
            {'type': 'object', 'properties': {}, 'required': []},
            _fx_rates,
        ),
        (
            'add_expense',
            (
                'Add a new expense.\n'
                'Amount may be in any supported currency (set `currency` to a 3-letter code like '
                '"eur", "usd", "gbp", "thb" — defaults to "inr"). The server converts to INR before '
                'persisting; do NOT convert in your head.\n'
                'splitBetween is an array of {userId, amount} pairs in the SAME `currency` as `amount`. '
                'Sum of split amounts must equal `amount` unless selfExpense=true.\n'
                'Include the payer in splitBetween when they share the expense; omit them if the payer '
                'paid entirely for someone else (e.g. "Alice paid X for Bob": paidBy=Alice, '
                'splitBetween=[{userId: Bob, amount: X}]).\n'
                'selfExpense=true: a personal expense logged for the bearer, no balances created. '
                'splitBetween must still be provided with a single entry for the payer.\n'
                'date is ISO YYYY-MM-DD; defaults to today.'
            ),
            {
                'type': 'object',
                'properties': {
                    'description': {'type': 'string', 'minLength': 1, 'maxLength': 350},
                    'amount': {'type': 'number', 'exclusiveMinimum': 0},
                    'currency': {
                        'type': 'string',
                        'description': '3-letter currency code (lowercase). Defaults to "inr".',
                        'default': 'inr',
                    },
                    'paidBy': {'type': 'integer'},
                    'splitBetween': {
                        'type': 'array',
                        'minItems': 1,
                        'items': {
                            'type': 'object',
                            'properties': {
                                'userId': {'type': 'integer'},
                                'amount': {'type': 'number', 'minimum': 0},
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
            'Delete an expense from the trip by expenseId. Only expenses belonging to this trip can be deleted.',
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
                'properties': {'note': {'type': 'string', 'minLength': 1, 'maxLength': 1000}},
                'required': ['note'],
            },
            _add_note,
        ),
        (
            'record_settlement',
            (
                'Record a real-world payment between two members. Use this when the user says they '
                'paid (or were paid) money to settle a debt — e.g. "I paid Alice ₹500 to settle up". '
                'fromUserId is the debtor (the one handing over money), toUserId is the creditor. '
                'amount may be in any supported currency (set `currency`); server converts to INR.'
            ),
            {
                'type': 'object',
                'properties': {
                    'fromUserId': {'type': 'integer'},
                    'toUserId': {'type': 'integer'},
                    'amount': {'type': 'number', 'exclusiveMinimum': 0},
                    'currency': {'type': 'string', 'default': 'inr'},
                    'date': {'type': 'string'},
                    'description': {'type': 'string', 'maxLength': 350},
                },
                'required': ['fromUserId', 'toUserId', 'amount'],
            },
            _record_settlement,
        ),
    ]
    return tools, MUTATIONS
