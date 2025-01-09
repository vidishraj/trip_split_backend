from sqlalchemy import text

from util.queries import Queries
from sqlalchemy.orm import sessionmaker, scoped_session

from flask_sqlalchemy import SQLAlchemy


class ExpenseBalanceHandler:

    def __init__(self, dbConnection: SQLAlchemy):
        super().__init__()
        self._dbSession = scoped_session(sessionmaker(autocommit=False,
                                                      autoflush=False,
                                                      bind=dbConnection.engine))

    def addBalance(self, balance):
        self._dbSession.execute(text(Queries.createBalance), balance)
        self._dbSession.commit()

    def addExpense(self, expense):
        result = self._dbSession.execute(text(Queries.insertExpense), {
            'expenseDate': expense['date'],
            'expenseDesc': expense['description'],
            'expenseAmount': expense['amount'],
            'expensePaidBy': expense['paidBy'],
            'expenseSplitBw': expense['splitbw'],
            'tripId': expense['tripId'],

        })
        self._dbSession.commit()
        return result.lastrowid

    def fetchExpForTrip(self, tripId):
        result = self._dbSession.execute(text(Queries.fetchExpensesFromTrip), {'tripId': tripId})
        keys = ['expenseId', 'date', 'expenseDesc', 'amount', 'paidBy', 'splitBetween', 'tripId']
        return [{keys[i]: value for i, value in enumerate(expense)} for expense in result.fetchall()]

    def fetchExpForTripJoined(self, tripId):
        result = self._dbSession.execute(text(Queries.fetchExpensesFromTripJoined), {'tripId': tripId})
        keys = ['expenseId', 'date', 'expenseDesc', 'expenseAmount', 'paidBy', 'splitBetween', 'tripId', 'userId',
                'amount', 'borrowedFrom']
        expenses = [{keys[i]: value for i, value in enumerate(expense)} for expense in result.fetchall()]

        combinedResult = {}
        for expense in expenses:
            combined_key = f"{expense['tripId']}_{expense['expenseId']}"
            if combined_key not in combinedResult:
                combinedResult[combined_key] = {
                    'expenseId': expense['expenseId'],
                    'date': expense['date'],
                    'expenseDesc': expense['expenseDesc'],
                    'amount': expense['expenseAmount'],
                    'paidBy': expense['paidBy'],
                    'tripId': expense['tripId'],
                    'splitBetween': {expense['userId']: expense['amount']}
                }
            else:
                combinedResult[combined_key]['splitBetween'][expense['userId']] = expense['amount']

        return list(combinedResult.values())

    def deleteExpenseFromTrip(self, expenseId):
        self._dbSession.execute(text(Queries.deleteExpense), {'expenseId': expenseId})
        self._dbSession.commit()
        return True

    def updateExpense(self, expenseId, tripData):
        splitList = tripData['splitbw']
        split_user_ids = [split['userId'] for split in splitList]
        updated_values = {
            'expenseDate': tripData['date'],
            'expenseDesc': tripData['description'],
            'expenseAmount': tripData['amount'],
            'expensePaidBy': tripData['paidBy'],
            'expenseSplitBw': str(split_user_ids),
            'expenseId': expenseId
        }
        self._dbSession.execute(text(Queries.updateExpense), updated_values)
        self._dbSession.commit()

        # Check if any row was updated
        rowCount = self._dbSession.rowcount
        return rowCount > 0

    def fetchBalances(self, tripId):
        result = self._dbSession.execute(text(Queries.fetchBalanceFromTrip), {'tripId': tripId})
        keys = ['tripId', 'userId', 'expenseId', 'amount', 'borrowedFrom']
        return [{keys[i]: value for i, value in enumerate(balance)} for balance in result.fetchall()]
