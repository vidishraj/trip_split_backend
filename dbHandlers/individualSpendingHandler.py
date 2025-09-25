from sqlalchemy import func
from models import Expense
from flask import g
from collections import defaultdict


class IndividualSpendingHandler:
    @property
    def _dbSession(self):
        return g.db

    def __init__(self):
        super().__init__()

    def fetchIndividualSpending(self, tripId):
        """
        Fetch how much each user actually spent (paid) for a trip.
        This shows actual money spent by each person, which should sum to total trip cost.
        """
        # Get all expenses for this trip
        expenses = self._dbSession.session.query(Expense).filter_by(tripId=tripId).all()
        
        # Calculate total spent by each user
        user_spending = defaultdict(float)
        total_trip_cost = 0
        
        for expense in expenses:
            # Add the amount this person paid
            user_spending[expense.expensePaidBy] += expense.expenseAmount
            total_trip_cost += expense.expenseAmount
        
        # Convert to regular dict and ensure all amounts are floats
        spending_dict = {}
        for user_id, amount in user_spending.items():
            spending_dict[user_id] = float(amount)
        
        return {
            'individualSpending': spending_dict,
            'totalTripCost': float(total_trip_cost),
            'verification': {
                'spendingSum': float(sum(spending_dict.values())),
                'matches': abs(sum(spending_dict.values()) - total_trip_cost) < 0.01
            }
        }