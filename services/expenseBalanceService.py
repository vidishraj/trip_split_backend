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
        Fixed expense creation with proper data preservation and balance logic.
        
        Balance Logic:
        - For each user in split: they owe their split amount (negative balance)
        - For the payer: they are owed their contribution (positive balance) 
        - Sum of all balances per expense should equal zero
        """
        expenseId = None
        try:
            splitList: list = expense['splitbw']
            paidBy = expense['paidBy']
            totalAmount = expense['amount']
            tripId = expense['tripId']
            selfExpense = expense['selfExpense']
            
            # CRITICAL FIX: Preserve full split data with amounts
            # Store as JSON with user IDs and amounts
            expense['splitbw'] = self._format_split_data(splitList)
            
            # Add expense to database
            expenseId = self.Handler.addExpense(expense)
            
            # Only create balance records for non-self expenses
            if not selfExpense:
                self._create_balance_records(splitList, paidBy, totalAmount, tripId, expenseId)
                
            # Validate balance integrity
            if not self._validate_balance_sum(expenseId):
                logging.warning(f"Balance validation failed for expense {expenseId}")
            
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
    
    def _format_split_data(self, splitList):
        """
        Format split data preserving both user IDs and amounts.
        
        Input: [{'userId': 35, 'amount': 100}, {'userId': 37, 'amount': 200}]
        Output: JSON string with full data preserved
        """
        import json
        
        # Ensure we preserve the complete split information
        formatted_data = []
        for split in splitList:
            formatted_data.append({
                'userId': split['userId'],
                'amount': float(split['amount'])  # Ensure proper float conversion
            })
        
        return json.dumps(formatted_data)
    
    def _create_balance_records(self, splitList, paidBy, totalAmount, tripId, expenseId):
        """
        Create balance records with correct accounting logic.
        
        Correct Balance Semantics:
        - Each user who owes money gets a negative balance (-amount they owe)
        - The payer gets positive balance for money they're owed
        - Sum of all balances = 0 (double-entry accounting)
        """
        total_owed_to_payer = 0
        
        # Create balance records for each person in the split
        for split in splitList:
            user_id = split['userId']
            user_amount = split['amount']
            
            if user_id != paidBy:
                # User owes money (negative balance)
                self.Handler.addBalance({
                    "tripId": tripId,
                    "userId": user_id,
                    "expenseId": expenseId,
                    "amount": -1 * user_amount,  # Negative = owes money
                    "borrowedFrom": paidBy,
                })
                total_owed_to_payer += user_amount
        
        # Create balance record for payer if they are owed money
        payer_split = next((s for s in splitList if s['userId'] == paidBy), None)
        if payer_split:
            # Payer is in the split - they are owed (total - their share)
            payer_owed = totalAmount - payer_split['amount']
            if payer_owed > 0:
                self.Handler.addBalance({
                    "tripId": tripId,
                    "userId": paidBy,
                    "expenseId": expenseId,
                    "amount": payer_owed,  # Positive = owed money
                    "borrowedFrom": paidBy,
                })
        else:
            # Payer not in split - they are owed the full amount
            self.Handler.addBalance({
                "tripId": tripId,
                "userId": paidBy,
                "expenseId": expenseId,
                "amount": totalAmount,  # Positive = owed money
                "borrowedFrom": paidBy,
            })
    
    def _validate_balance_sum(self, expenseId):
        """
        Validate that all balance records for an expense sum to zero.
        This ensures proper double-entry accounting.
        """
        try:
            balances = self.Handler.fetchBalancesByExpense(expenseId)
            total_balance = sum(balance['amount'] for balance in balances)
            
            # Allow small floating point differences
            is_valid = abs(total_balance) < 0.01
            
            if not is_valid:
                logging.warning(f"Balance sum validation failed for expense {expenseId}: sum = {total_balance}")
            
            return is_valid
            
        except Exception as e:
            logging.error(f"Error validating balance sum for expense {expenseId}: {e}")
            return False
