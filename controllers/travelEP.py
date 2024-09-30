from flask import request, jsonify
from travelInstances import TravelInstance
from util.logger import logging

tripUserHandler = TravelInstance.tripHandler
tripUserService = TravelInstance.tripUserService
expenseBalanceHandler = TravelInstance.expenseHandler
expenseBalanceService = TravelInstance.expenseBalanceService


def createTrip():
    try:
        postedDate = request.get_json(force=True)
        if tripUserHandler.checkDbConnection():
            logging.info("-----Creating New Trip-----")
            return jsonify({"Message": tripUserService.createTrip(postedDate['trip'])}), 200
        else:
            return jsonify({"Error": "DB Connection Failed"}), 501
    except Exception as ex:
        return jsonify({"Error": f"Error inserting new trip {ex}"}), 500
    finally:
        logging.info("----Finished inserting new trip-----")


def fetchTrips():
    try:
        if tripUserHandler.checkDbConnection():
            logging.info("-----Fetching all trips-----")
            return jsonify({"Message": tripUserService.fetchTrip()}), 200
        else:
            return jsonify({"Error": "DB Connection Failed"}), 501
    except Exception as ex:
        return jsonify({"Error": f"Error fetching all trips{ex}"}), 500
    finally:
        logging.info("----Finished fetching all trip-----")


""" User EPs """


def fetchUsersForTrip():
    tripId = request.args.get('trip')
    try:
        if tripUserHandler.checkDbConnection():
            logging.info("-----Fetching all users for a trip-----")
            return jsonify({"Message": tripUserService.fetchUserForTrip(tripId)}), 200
        else:
            return jsonify({"Error": "DB Connection Failed"}), 501
    except Exception as ex:
        return jsonify({"Error": f"Error fetching all users for trip{ex}"}), 500
    finally:
        logging.info("----Finished fetching users for trip-----")


def addUserToTrip():
    postedData = request.get_json(force=True)
    try:
        if tripUserHandler.checkDbConnection():
            logging.info("-----Adding users to trip-----")
            return jsonify({"Message": tripUserService.addUserToTrip(postedData['user'])}), 200
        else:
            return jsonify({"Error": "DB Connection Failed"}), 501
    except Exception as ex:
        return jsonify({"Error": f"Error adding user to trip{ex}"}), 500
    finally:
        logging.info("----Finished adding user to trip-----")


# Can add another one to edit the userName

"""EXPENSE EPS"""


# Fetch expense for a trip
def fetchExpensesForATrip():
    tripId = request.args.get('trip')
    try:
        if tripUserHandler.checkDbConnection():
            logging.info("-----Fetching all expenses for a trip-----")
            return jsonify({"Message": expenseBalanceService.fetchExpensesForTrip(tripId)}), 200
        else:
            return jsonify({"Error": "DB Connection Failed"}), 501
    except Exception as ex:
        return jsonify({"Error": f"Error fetching all expenses for trip{ex}"}), 500
    finally:
        logging.info("----Finished fetching expenses for trip-----")


# Delete expense for a trip
def deleteExpenseForTrip():
    expenseId = request.form.get('expenseId')
    try:
        if tripUserHandler.checkDbConnection():
            logging.info("-----Deleting expense for a trip-----")
            return jsonify({"Message": expenseBalanceService.deleteExpenseFromTrip(expenseId)}), 200
        else:
            return jsonify({"Error": "DB Connection Failed"}), 501
    except Exception as ex:
        return jsonify({"Error": f"Error fetching all expenses for trip{ex}"}), 500
    finally:
        logging.info("----Finished fetching expenses for trip-----")


# Add expense for a trip
def addExpenseForTrip():
    postedData = request.get_json()
    try:
        if tripUserHandler.checkDbConnection():
            logging.info("-----Adding expense for a trip-----")
            return jsonify({"Message": expenseBalanceService.addExpenseForTrip(postedData)}), 200
        else:
            return jsonify({"Error": "DB Connection Failed"}), 501
    except Exception as ex:
        return jsonify({"Error": f"Error adding expense for trip {ex}"}), 500
    finally:
        logging.info("----Finished adding expense for trip-----")


# Edit expense for a trip


""" Balances EP """


def fetchBalancesForATrip():
    tripId = request.form.get('trip')
    try:
        if tripUserHandler.checkDbConnection():
            logging.info("-----Fetching all users for a trip-----")
            return jsonify({"Message":"Expense added successfully"}), 200
        else:
            return jsonify({"Error": "DB Connection Failed"}), 501
    except Exception as ex:
        return jsonify({"Error": f"Error fetching all users for trip{ex}"}), 500
    finally:
        logging.info("----Finished fetching users for trip-----")
