from collections import defaultdict

from sqlalchemy import func

from models import Balance, Expense
from flask import g


class ExpenseBalanceHandler:
    @property
    def _dbSession(self):
        return g.db

    def __init__(self):
        super().__init__()
        # self._dbSession = g.get('db')

    def addBalance(self, balance):
        balance = Balance(
            tripId=balance['tripId'],
            userId=balance['userId'],
            expenseId=balance['expenseId'],
            amount=balance['amount'],
            borrowedFrom=balance['borrowedFrom']
        )
        self._dbSession.session.add(balance)
        self._dbSession.session.commit()

    def addExpense(self, expense):
        expense = Expense(
            expenseDate=expense['date'],
            expenseDesc=expense['description'],
            expenseAmount=expense['amount'],
            expensePaidBy=expense['paidBy'],
            expenseSplitBw=expense['splitbw'],
            tripId=expense['tripId'],
            expenseSelf=expense['selfExpense']
        )
        self._dbSession.session.add(expense)
        self._dbSession.session.commit()
        return expense.expenseId

    def fetchExpForTrip(self, tripId):
        result = Expense.query.filter_by(tripId=tripId).all()
        return [
            {
                'expenseId': expense.expenseId,
                'date': expense.expenseDate,
                'expenseDesc': expense.expenseDesc,
                'amount': expense.expenseAmount,
                'paidBy': expense.expensePaidBy,
                'splitBetween': expense.expenseSplitBw,
                'tripId': expense.tripId,
            }
            for expense in result
        ]

    def fetchIndividualBalance(self, tripId):
        selfExpenses = (
            Expense.query.filter_by(tripId=tripId).filter_by(expenseSelf=True).all()
        )
        joined_data = (
            self._dbSession.session.query(Expense, Balance)
            .join(Balance, Expense.expenseId == Balance.expenseId)
            .filter(Expense.tripId == tripId)
            .all()
        )
        totalExpense = (
            self._dbSession.session.query(func.sum(Expense.expenseAmount))
            .filter_by(tripId=tripId)
            .scalar()
        )

        res = defaultdict(lambda: defaultdict(int))

        for expense in selfExpenses:
            res["selfExpense"][expense.expensePaidBy] += expense.expenseAmount

        for expense, balance in joined_data:
            # For all users: just add their balance amount (positive for payer, negative for debtors)
            res['expense'][balance.userId] += balance.amount

        res["total"] = totalExpense or 0
        return res

    def fetchExpForTripJoined(self, tripId):
        result = (
            self._dbSession.session.query(
                Expense.expenseId,
                Expense.expenseDate,
                Expense.expenseDesc,
                Expense.expenseAmount,
                Expense.expensePaidBy,
                Expense.expenseSelf,
                Balance.tripId,
                Balance.userId,
                Balance.amount,
                Balance.borrowedFrom,
            )
            .join(Balance, Expense.expenseId == Balance.expenseId)
            .filter(Expense.tripId == tripId)
            .all()
        )

        # Map results to dictionaries
        expenses = [
            {
                'expenseId': row.expenseId,
                'date': row.expenseDate,
                'expenseDesc': row.expenseDesc,
                'amount': row.expenseAmount,
                'paidBy': row.expensePaidBy,
                'expenseSelf': row.expenseSelf,
                'tripId': row.tripId,
                'userId': row.userId,
                'splitAmount': row.amount,
                'borrowedFrom': row.borrowedFrom,
            }
            for row in result
        ]
        selfExpensesInDb = Expense.query.filter_by(expenseSelf=True).filter_by(tripId=tripId).all()
        selfExpenses = [
            {
                'expenseId': selfExpense.expenseId,
                'date': selfExpense.expenseDate,
                'expenseDesc': selfExpense.expenseDesc,
                'amount': selfExpense.expenseAmount,
                'paidBy': selfExpense.expensePaidBy,
                'expenseSelf': selfExpense.expenseSelf,
                'tripId': selfExpense.tripId,
                'userId': selfExpense.expensePaidBy,
                'splitAmount': 0,
                'borrowedFrom': selfExpense.expensePaidBy,
            }
            for selfExpense in selfExpensesInDb
        ]
        expenses += selfExpenses
        # Combine results by expenseId and tripId
        combined_result = {}
        for expense in expenses:
            combined_key = f"{expense['tripId']}_{expense['expenseId']}"
            if combined_key not in combined_result:
                combined_result[combined_key] = {
                    'expenseId': expense['expenseId'],
                    'date': expense['date'],
                    'expenseDesc': expense['expenseDesc'],
                    'amount': expense['amount'],
                    'paidBy': expense['paidBy'],
                    'selfExpense': expense['expenseSelf'],
                    'tripId': expense['tripId'],
                    'splitBetween': {expense['userId']: expense['splitAmount']}
                }
            else:
                combined_result[combined_key]['splitBetween'][expense['userId']] = expense['splitAmount']

        return list(combined_result.values())

    def deleteExpenseFromTrip(self, expenseId):
        Expense.query.filter_by(expenseId=expenseId).delete()
        self._dbSession.session.commit()
        return True

    def updateExpense(self, expenseId, tripData):
        """
        Updated expense editing logic to handle new format and correct balance calculations
        """
        import json
        
        split_list = tripData['splitbw']
        
        # Fetch the expense to update
        expense = self._dbSession.session.query(Expense).filter_by(expenseId=expenseId).first()
        
        if not expense:
            return False
        
        # Store original values for rollback if needed
        original_amount = expense.expenseAmount
        original_split = expense.expenseSplitBw
        original_self = expense.expenseSelf
        
        try:
            # Update the expense fields
            expense.expenseDate = tripData['date']
            expense.expenseDesc = tripData['description']
            expense.expenseAmount = tripData['amount']
            expense.expensePaidBy = tripData['paidBy']
            expense.expenseSelf = tripData['selfExpense']
            
            # Format and store split data with full information preserved
            formatted_split_data = []
            for split in split_list:
                formatted_split_data.append({
                    'userId': split['userId'],
                    'amount': float(split['amount'])
                })
            expense.expenseSplitBw = json.dumps(formatted_split_data)
            
            # Handle balance record updates
            if original_self == 0 and tripData['selfExpense'] == 1:
                # Changed from split to self expense - delete all balance records
                Balance.query.filter_by(expenseId=expenseId).delete()
            elif tripData['selfExpense'] == 0:
                # Update or create balance records with correct logic
                self._update_balance_records(expenseId, split_list, tripData['paidBy'], tripData['amount'])
            
            # Commit changes
            self._dbSession.session.commit()
            
            # Validate balance sum for non-self expenses
            if tripData['selfExpense'] == 0:
                balances = self.fetchBalancesByExpense(expenseId)
                balance_sum = sum(b['amount'] for b in balances)
            return True
            
        except Exception as e:
            # Rollback on error
            self._dbSession.session.rollback()
            raise e

    # def fetchSelfTransactions(self, userid):
    #     result = self._dbSession.session.query(Balance).filter(Balance.userId == userid).filter(
    #         Balance.userId == Balance.borrowedFrom).filter(Balance.amount < 0).all()
    #
    #     total_amount = sum(balance.amount for balance in result)
    #     return [
    #         {
    #             'amount': total_amount
    #         }
    #         for balance in result
    #     ]

    def fetchBalances(self, tripId):
        result = self._dbSession.session.query(Balance).filter_by(tripId=tripId).all()
        return [
            {
                'tripId': balance.tripId,
                'userId': balance.userId,
                'expenseId': balance.expenseId,
                'amount': balance.amount,
                'borrowedFrom': balance.borrowedFrom,
            }
            for balance in result
        ]
    
    def fetchBalancesByExpense(self, expenseId):
        """Fetch all balance records for a specific expense"""
        result = self._dbSession.session.query(Balance).filter_by(expenseId=expenseId).all()
        return [
            {
                'tripId': balance.tripId,
                'userId': balance.userId,
                'expenseId': balance.expenseId,
                'amount': balance.amount,
                'borrowedFrom': balance.borrowedFrom,
            }
            for balance in result
        ]
    
    def _update_balance_records(self, expenseId, split_list, paidBy, totalAmount):
        """
        Update balance records for an edited expense with correct accounting logic
        """
        from util.logger import Logger
        logging = Logger().get_logger()
        
        # Delete existing balance records
        Balance.query.filter_by(expenseId=expenseId).delete()
        
        # Create new balance records with correct logic
        for split in split_list:
            user_id = split['userId']
            user_amount = split['amount']
            
            if user_id != paidBy:
                # User owes money (negative balance)
                new_balance = Balance(
                    tripId=self._get_trip_id_for_expense(expenseId),
                    userId=user_id,
                    expenseId=expenseId,
                    amount=-1 * user_amount,
                    borrowedFrom=paidBy
                )
                self._dbSession.session.add(new_balance)
        
        # Create balance record for payer
        payer_split = next((s for s in split_list if s['userId'] == paidBy), None)
        if payer_split:
            # Payer is in split - they are owed (total - their share)
            payer_owed = totalAmount - payer_split['amount']
            if payer_owed > 0:
                payer_balance = Balance(
                    tripId=self._get_trip_id_for_expense(expenseId),
                    userId=paidBy,
                    expenseId=expenseId,
                    amount=payer_owed,
                    borrowedFrom=paidBy
                )
                self._dbSession.session.add(payer_balance)
        else:
            # Payer not in split - they are owed the full amount
            payer_balance = Balance(
                tripId=self._get_trip_id_for_expense(expenseId),
                userId=paidBy,
                expenseId=expenseId,
                amount=totalAmount,
                borrowedFrom=paidBy
            )
            self._dbSession.session.add(payer_balance)
    
    def _get_trip_id_for_expense(self, expenseId):
        """Get the trip ID for a given expense ID"""
        expense = self._dbSession.session.query(Expense).filter_by(expenseId=expenseId).first()
        return expense.tripId if expense else None
