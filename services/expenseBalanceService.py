from dbHandlers.expenseBalanceHandler import ExpenseBalanceHandler
from util.logger import Logger

logging = Logger().get_logger()


class ExpenseBalanceService:
    Handler: ExpenseBalanceHandler

    def __init__(self, exBlHandler: ExpenseBalanceHandler):
        self.Handler = exBlHandler

    def fetchExpensesForTrip(self, tripId):
        return self.Handler.fetchExpForTripJoined(tripId)

    def addExpenseForTrip(self, expense):
        """ First obj is to insert the expense, then individually call the balance table."""
        expenseId = None
        try:
            splitList: list = expense['splitbw']
            paidBy = expense['paidBy']
            amount = expense['amount']
            tripId = expense['tripId']
            expense['splitbw'] = [split['userId'] for split in expense['splitbw']].__str__()
            expenseId = self.Handler.addExpense(expense)
            for split in splitList:
                if split['userId'] != paidBy:
                    self.Handler.addBalance({
                        "tripId": tripId,
                        "userId": split['userId'],
                        "expenseId": expenseId,
                        "amount": amount,
                        "borrowedFrom": paidBy,
                    })
                else:
                    self.Handler.addBalance({
                            "tripId": tripId,
                            "userId": split['userId'],
                            "expenseId": expenseId,
                            "amount": amount - split['amount'],
                            "borrowedFrom": paidBy,
                        })
            return True
        except Exception as ex:
            if expenseId is not None:
                self.deleteExpenseFromTrip(expenseId)
            logging.error(f"Error while adding expense {ex}")
            return False

    def editExpenseForTrip(self, expenseId, editData):
        return self.Handler.updateExpense(expenseId, editData)

    def deleteExpenseFromTrip(self, expenseId):
        return self.Handler.deleteExpenseFromTrip(expenseId)

    def fetchBalances(self, tripId):
        balances = self.Handler.fetchBalances(tripId)
        userBalance = {}
        for balance in balances:
            if userBalance.get(balance['userId']) is None:
                userBalance[balance['userId']] = balance['amount']
            else:
                userBalance[balance['userId']] += balance['amount']
        return userBalance
