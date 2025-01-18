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
            tripId=expense['tripId']
        )
        self._dbSession.session.add(expense)
        self._dbSession.session.commit()
        return expense.expenseId

    def fetchExpForTrip(self, tripId):
        result = Expense.query.filter_by(tripId=tripId).all()
        return [
            {
                'expenseId': expense.expenseId,
                'date': expense.date,
                'expenseDesc': expense.expenseDesc,
                'amount': expense.amount,
                'paidBy': expense.paidBy,
                'splitBetween': expense.splitBetween,
                'tripId': expense.tripId,
            }
            for expense in result
        ]

    def fetchExpForTripJoined(self, tripId):
        result = (
            self._dbSession.session.query(
                Expense.expenseId,
                Expense.expenseDate,
                Expense.expenseDesc,
                Expense.expenseAmount,
                Expense.expensePaidBy,
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
                'tripId': row.tripId,
                'userId': row.userId,
                'splitAmount': row.amount,
                'borrowedFrom': row.borrowedFrom,
            }
            for row in result
        ]

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
        split_list = tripData['splitbw']
        split_user_ids = [split['userId'] for split in split_list]

        # Fetch the expense to update
        expense = self._dbSession.session.query(Expense).filter_by(expenseId=expenseId).first()

        if not expense:
            # If no expense found, return False
            return False

        # Update the expense fields
        expense.expenseDate = tripData['date']
        expense.expenseDesc = tripData['description']
        expense.expenseAmount = tripData['amount']
        expense.expensePaidBy = tripData['paidBy']
        expense.expenseSplitBw = str(split_user_ids)

        for index, user in enumerate(split_user_ids):
            balance: Balance = self._dbSession.session.query(Balance).filter_by(expenseId=expenseId).filter_by(
                userId=user).first()
            if not balance:
                # If no balance found, return False
                return False
            if balance.userId != expense.expensePaidBy:
                balance.amount = -1 * split_list[index]['amount']
            else:
                balance.amount = expense.expenseAmount-split_list[index]['amount']
        # Commit changes to the database
        self._dbSession.session.commit()

        # Return True if the update was successful
        return True

    def fetchSelfTransactions(self, userid):
        result = self._dbSession.session.query(Balance).filter(Balance.userId == userid).filter(
            Balance.userId == Balance.borrowedFrom).filter(Balance.amount < 0).all()

        total_amount = sum(balance.amount for balance in result)
        return [
            {
                'amount': total_amount
            }
            for balance in result
        ]

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
