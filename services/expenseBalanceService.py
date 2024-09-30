from dbHandlers.expenseBalanceHandler import ExpenseBalanceHandler
from util.logger import logging


class ExpenseBalanceService:
    Handler: ExpenseBalanceHandler

    def __init__(self, exBlHandler: ExpenseBalanceHandler):
        self.Handler = exBlHandler

    def addExpenseForTrip(self, expense):
        """ First obj is to insert the expense, then individually call the balance table."""
        expenseId = None
        try:
            splitList: list = expense['splitbw']
            currencyRate = expense['currencyRate']
            paidBy = expense['paidBy']
            amount = expense['amount']
            description = expense['description']
            date = expense['date']
            tripId = expense['tripId']
            expenseId = self.Handler.addExpense((date, description, amount, paidBy['userId'], [split['userName'] for split
                                                                                               in splitList].__str__(), tripId))
            for split in splitList:
                if split['userId'] != paidBy['userId']:
                    self.Handler.addBalance((tripId, split['userId'], expenseId, 0, split['amount'], currencyRate,
                                             paidBy['userId']))
            return
        except Exception as ex:
            if expenseId is not None:
                self.deleteExpenseFromTrip(expenseId)
            logging.error("Error while adding expense", ex)
            return

    def fetchExpensesForTrip(self, tripId):
        return self.Handler.fetchExpForTrip(tripId)

    def deleteExpenseFromTrip(self, expenseId):
        return self.Handler.deleteExpenseFromTrip(expenseId)
