from services.expenseBalanceService import ExpenseBalanceService
from services.tripUserService import TripUserService
from dbHandlers.expenseBalanceHandler import ExpenseBalanceHandler
from dbHandlers.tripUserHandler import TripUserHandler
from util.db_connector import db_connector



class TravelInstance:
    if db_connector is not None:

        transactionConnectionInstance = db_connector.get_connection()
        transactionConnectionInstance2 = db_connector.get_connection()

        tripHandler = TripUserHandler(transactionConnectionInstance)
        expenseHandler = ExpenseBalanceHandler(transactionConnectionInstance2)

        tripUserService = TripUserService(tripHandler)
        expenseBalanceService = ExpenseBalanceService(expenseHandler)

    else:
        transactionConnectionInstance = None
        transactionConnectionInstance2 = None
        tripHandler = None
        expenseHandler = None
        tripUserService = None
        expenseBalanceService = None
