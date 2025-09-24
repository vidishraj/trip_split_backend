import heapq
from collections import defaultdict

from dbHandlers.expenseBalanceHandler import ExpenseBalanceHandler
from util.logger import Logger

logging = Logger().get_logger()


class ExpenseBalanceService:
    Handler: ExpenseBalanceHandler

    def __init__(self, exBlHandler: ExpenseBalanceHandler):
        self.Handler = exBlHandler

    def fetchExpensesForTrip(self, tripId):
        return self.Handler.fetchExpForTripJoined(tripId)

    def fetchIndividualBalance(self, tripId):
        return self.Handler.fetchIndividualBalance(tripId)

    def addExpenseForTrip(self, expense):
        """
        First obj is to insert the expense, then individually call the balance table.
        Three cases to consider-: Person paying is involved in the split, the person paying is not involved in split
        ONLY the person paying is involved in split (self-expense)
        """
        expenseId = None
        try:
            splitList: list = expense['splitbw']
            paidBy = expense['paidBy']
            amount = expense['amount']
            tripId = expense['tripId']
            selfExpense = expense['selfExpense']
            expense['splitbw'] = [split['userId'] for split in expense['splitbw']].__str__()
            expenseId = self.Handler.addExpense(expense)
            personIncludedInSplit = False
            # Case 3

            # Case 1
            if not selfExpense:
                for split in splitList:
                    if split['userId'] != paidBy:
                        self.Handler.addBalance({
                            "tripId": tripId,
                            "userId": split['userId'],
                            "expenseId": expenseId,
                            "amount": -1 * split['amount'],
                            "borrowedFrom": paidBy,
                        })
                    else:
                        personIncludedInSplit = True
                        self.Handler.addBalance({
                            "tripId": tripId,
                            "userId": split['userId'],
                            "expenseId": expenseId,
                            "amount": amount - split['amount'],
                            "borrowedFrom": paidBy,
                        })

            # Case 2
            if not personIncludedInSplit:
                self.Handler.addBalance({
                    "tripId": tripId,
                    "userId": paidBy,
                    "expenseId": expenseId,
                    "amount": amount,
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

    # def fetchBalances(self, tripId):
    #     balances = self.Handler.fetchBalances(tripId)
    #     userBalance = {}
    #     for balance in balances:
    #         if userBalance.get(balance['userId']) is None:
    #             userBalance[balance['userId']] = {}
    #             userBalance[balance['userId']]['amount'] = balance['amount']
    #         else:
    #             userBalance[balance['userId']]['amount'] += balance['amount']
    #     for userId in list(userBalance.keys()):
    #         selfTransaction = self.Handler.fetchSelfTransactions(userId)
    #         if len(selfTransaction) > 0:
    #             amount = selfTransaction[0]['amount']
    #             userBalance[userId]['amount'] += (-1 * amount)
    #             userBalance[userId]['selfTransaction'] = amount
    #         else:
    #             userBalance[userId]['selfTransaction'] = 0
    #     return userBalance

    def fetchBalanceV2(self, tripId):
        # Fetch all Balances for a trip
        balances = self.Handler.fetchBalances(tripId)
        response = []
        # Create net user owed dict
        userOwedDict = defaultdict(int)
        for balance in balances:
            userOwedDict[balance['userId']] += balance['amount']

        # We will use two heaps. One heap for user who owe money and one for user who are owed money
        userIds = list(userOwedDict.keys())

        # max heap
        usersOwedMoney = [tuple([-1 * userOwedDict[userId], userId]) for userId in userIds if userOwedDict[userId] > 0]
        userOweMoney = [tuple([userOwedDict[userId], userId]) for userId in userIds if userOwedDict[userId] < 0]

        # Max Heap
        heapq.heapify(usersOwedMoney)
        # Min Heap
        heapq.heapify(userOweMoney)

        # We reduce till there people who need to pay people money (Negative values)
        while len(userOweMoney) > 0 and len(usersOwedMoney) > 0:
            # Our goal is to map transactions of max owed to max owe.
            highestOweMoney, userIdPayee = heapq.heappop(userOweMoney)
            highestOwedMoney, userIdPaidTo = heapq.heappop(usersOwedMoney)
            
            # Amount to transfer is the minimum of what debtor owes and what creditor is owed
            debtAmount = -1 * highestOweMoney  # Convert negative debt to positive amount
            creditAmount = -1 * highestOwedMoney  # Convert negative heap value to positive amount
            transferAmount = min(debtAmount, creditAmount)
            
            response.append({
                'from': userIdPayee,
                'to': userIdPaidTo,
                'amount': transferAmount
            })
            
            # Calculate remaining amounts
            remainingDebt = debtAmount - transferAmount
            remainingCredit = creditAmount - transferAmount
            
            # Add back remaining amounts if > threshold
            if remainingCredit > 0.01:
                # Creditor still owed money, add back to usersOwedMoney heap
                heapq.heappush(usersOwedMoney, tuple([-1 * remainingCredit, userIdPaidTo]))
            if remainingDebt > 0.01:
                # Debtor still owes money, add back to userOweMoney heap  
                heapq.heappush(userOweMoney, tuple([-1 * remainingDebt, userIdPayee]))

        return response
