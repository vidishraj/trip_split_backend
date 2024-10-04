from util.DBReset import DBReset
from util.queries import Queries


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

    def fetchExpForTripJoined(self, tripId):
        self._dbConnection.commit()
        cursor = self._dbConnection.cursor()
        cursor.execute(Queries.fetchExpensesFromTripJoined, tuple([tripId]))
        expenses = cursor.fetchall()
        result = []
        keys = ['expenseId', 'date', 'expenseDesc', 'expenseAmount', 'paidBy', 'splitBetween', 'tripId', 'userId',
                'amount','borrowedFrom']
        for expense in expenses:
            result.append({keys[i]: value for i, value in enumerate(expense)})
        cursor.close()
        combinedResult = {}
        for expense in result:
            if combinedResult.get(f"{expense['tripId']}_{expense['expenseId']}") is None:
                combinedResult[f"{expense['tripId']}_{expense['expenseId']}"] = {
                    'expenseId': expense['expenseId'],
                    'date': expense['date'],
                    'expenseDesc': expense['expenseDesc'],
                    'amount': expense['expenseAmount'],
                    'paidBy': expense['paidBy'],
                    'tripId': expense['tripId'],
                    'splitBetween': {
                        expense['userId']: expense['amount']
                    },
                }
            else:
                combinedResult[f"{expense['tripId']}_{expense['expenseId']}"]['splitBetween'][expense['userId']] = \
                    expense['amount']
        return list(combinedResult.values())

    def deleteExpenseFromTrip(self, expenseId):
        self._dbConnection.commit()
        cursor = self._dbConnection.cursor()
        cursor.execute(Queries.deleteExpense, tuple([expenseId]))
        self._dbConnection.commit()
        cursor.close()
        return True

    def updateExpense(self, expenseId, tripData):
        self._dbConnection.commit()
        cursor = self._dbConnection.cursor()
        splitList: list = tripData['splitbw']
        cursor.execute(Queries.updateExpense, tuple([tripData['date'], tripData['description'], tripData['amount'],
                                                     tripData['paidBy'],
                                                     [split['userId'] for split in splitList].__str__(), expenseId]))
        rowCount = cursor.rowcount
        self._dbConnection.commit()
        cursor.close()
        if rowCount > 0:
            return True
        return False

    def fetchBalances(self, tripId):
        self._dbConnection.commit()
        cursor = self._dbConnection.cursor()
        cursor.execute(Queries.fetchBalanceFromTrip, tuple([tripId]))
        balances = cursor.fetchall()
        result = []
        keys = ['tripId', 'userId', 'expenseId', 'amount', 'borrowedFrom']
        for balance in balances:
            result.append({keys[i]: value for i, value in enumerate(balance)})
        cursor.close()
        return result
