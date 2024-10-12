from dbHandlers.expenseBalanceHandler import ExpenseBalanceHandler
from util.logger import Logger

logging = Logger().get_logger()


class ExpenseBalanceService:
    Handler: ExpenseBalanceHandler

    def __init__(self, exBlHandler: ExpenseBalanceHandler):
        self.Handler = exBlHandler

    def addExpenseForTrip(self, expense):
        """ First obj is to insert the expense, then individually call the balance table."""
        expenseId = None
        try:
            splitList: list = expense['splitbw']
            paidBy = expense['paidBy']
            amount = expense['amount']
            description = expense['description']
            date = expense['date']
            tripId = expense['tripId']
            expenseId = self.Handler.addExpense((date, description, amount, paidBy, [split['userId'] for split
                                                                                     in splitList].__str__(), tripId))
            for split in splitList:
                if split['userId'] != paidBy:
                    self.Handler.addBalance((tripId, split['userId'], expenseId, -1 * split['amount'],
                                             paidBy))
                else:
                    self.Handler.addBalance((tripId, split['userId'], expenseId, amount - split['amount'],
                                             paidBy))
            return True
        except Exception as ex:
            if expenseId is not None:
                self.deleteExpenseFromTrip(expenseId)
            logging.error("Error while adding expense", ex)
            return False

    def editExpenseForTrip(self, expenseId, editData):
        return self.Handler.updateExpense(expenseId, editData)

    def fetchExpensesForTrip(self, tripId):
        return self.Handler.fetchExpForTripJoined(tripId)

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
