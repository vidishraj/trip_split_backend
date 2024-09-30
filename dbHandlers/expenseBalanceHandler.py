from util.DBReset import DBReset
from util.queries import Queries
from util.logger import logging


class ExpenseBalanceHandler(DBReset):

    def __init__(self, dbConnection):
        super().__init__()
        self._dbConnection = dbConnection

    def addBalance(self, balance):
        self._dbConnection.commit()
        cursor = self._dbConnection.cursor()
        cursor.execute(Queries.createBalance, tuple(balance))
        self._dbConnection.commit()
        cursor.close()

    def addExpense(self, expense):
        self._dbConnection.commit()
        cursor = self._dbConnection.cursor()
        cursor.execute(Queries.insertExpense, expense)
        self._dbConnection.commit()
        lastId = cursor.lastrowid
        cursor.close()
        return lastId

    def fetchExpForTrip(self, tripId):
        self._dbConnection.commit()
        cursor = self._dbConnection.cursor()
        cursor.execute(Queries.fetchExpensesFromTrip, tuple([tripId]))
        expenses = cursor.fetchall()
        result = []
        keys = ['expenseId', 'date', 'expenseDesc', 'amount', 'paidBy', 'splitBetween', 'tripId']
        for expense in expenses:
            result.append({keys[i]: value for i, value in enumerate(expense)})
        cursor.close()
        return result

    def deleteExpenseFromTrip(self, expenseId):
        self._dbConnection.commit()
        cursor = self._dbConnection.cursor()
        cursor.execute(Queries.deleteExpense, tuple([expenseId]))
        self._dbConnection.commit()
        cursor.close()
        return True
