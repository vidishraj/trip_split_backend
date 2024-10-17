from flask import request, jsonify
from travelInstances import TravelInstance
from util.logger import Logger
from firebase_admin import auth

logging = Logger().get_logger()
tripUserHandler = TravelInstance.tripHandler
tripUserService = TravelInstance.tripUserService
expenseBalanceHandler = TravelInstance.expenseHandler
expenseBalanceService = TravelInstance.expenseBalanceService


def createTrip():
    logging.info("----New Sign up. Adding Use to DB-----")
    try:
        postedDate = request.get_json(force=True)
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            id_token = auth_header.split(' ')[1]
            decoded_token = auth.verify_id_token(id_token)
            user_email = decoded_token.get('email')
            logging.info(f"Fetched email. Adding user with email {user_email}")
            if tripUserHandler.checkDbConnection() and user_email:
                return jsonify(
                    {"Message": tripUserService.createTrip(postedDate['trip'], postedDate['currencies'], user_email)}), \
                    200
        else:
            return jsonify({"Error": "DB Connection Failed or Auth failed"}), 501
    except Exception as ex:
        logging.error(f"Error inserting user during sign up {ex}")
        return jsonify({"Error": f"Error inserting user during sign up {ex}"}), 500
    finally:
        logging.info("----Finished adding new user during sign up-----")


def fetchTrips():
    logging.info("---Fetching all trips for user---- ")
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            id_token = auth_header.split(' ')[1]
            decoded_token = auth.verify_id_token(id_token)
            user_email = decoded_token.get('email')
            if tripUserHandler.checkDbConnection() and user_email:
                return jsonify({"Message": tripUserService.fetchTrip(user_email)}), 200
        else:
            return jsonify({"Error": "DB Connection Failed or Auth failed."}), 501
    except Exception as ex:
        logging.error(f"Error fetching trips {ex}")
        return jsonify({"Error": f"Error fetching trips {ex}"}), 500
    finally:
        logging.info("----Finished fetching trips-----")


""" User EPs """


def createUser():
    try:
        postedDate = request.get_json(force=True)
        if tripUserHandler.checkDbConnection():
            logging.info("-----Creating New User-----")
            return jsonify({"Message": tripUserService.createUser(postedDate['userName'], postedDate['email'])}), 200
        else:
            return jsonify({"Error": "DB Connection Failed"}), 501
    except Exception as ex:
        logging.error(f"Error creating user {ex}")
        return jsonify({"Error": f"Error creating new user {ex}"}), 500
    finally:
        logging.info("----Finished creating new user-----")


def setUserRequest():
    postedData = request.get_json(force=True)
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            id_token = auth_header.split(' ')[1]
            decoded_token = auth.verify_id_token(id_token)
            user_email = decoded_token.get('email')
            tripId = postedData['tripId']
            if tripUserHandler.checkDbConnection():
                logging.info(f"-----Adding request for trip {tripId} {user_email}-----")
                return jsonify({"Message": tripUserService.addRequestForTrip(tripId, user_email)}), 200
        else:
            return jsonify({"Error": "DB Connection Failed"}), 501
    except Exception as ex:
        return jsonify({"Error": f"Error adding request for user to trip {ex}"}), 500
    finally:
        logging.info("----Finished adding request for user to trip-----")


def fetchTripRequestForTrip():
    tripId = request.args.get('trip')
    try:
        if tripUserHandler.checkDbConnection():
            logging.info("-----Fetching all trip requests for a trip-----")
            return jsonify({"Message": tripUserService.fetchTripRequestForTrip(tripId)}), 200
        else:
            return jsonify({"Error": "DB Connection Failed"}), 501
    except Exception as ex:
        return jsonify({"Error": f"Error fetching all trip requests for trip {ex}"}), 500
    finally:
        logging.info("----Finished fetching trip requests for trip-----")


def registerRequestResponse():
    postedData = request.get_json(force=True)
    try:
        if tripUserHandler.checkDbConnection():
            userId = postedData['userId']
            tripId = postedData['tripId']
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                id_token = auth_header.split(' ')[1]
                decoded_token = auth.verify_id_token(id_token)
                user_email = decoded_token.get('email')
                if tripUserService.checkIfcheckIfUserHasAuthority(user_email, tripId):
                    response = postedData['response']
                    logging.info("-----Registering response for trip request-----")
                    return jsonify(
                        {"Message": tripUserService.registerRequestResponse(userId, tripId, response)}), 200

            else:
                return jsonify({"Error": "User does not has Auth."}), 501
        else:
            return jsonify({"Error": "DB Connection Failed"}), 501
    except Exception as ex:
        return jsonify({"Error": f"Error registering response for trip request {ex}"}), 500
    finally:
        logging.info("----Finished registering response for trip request-----")


def fetchUsersForTrip():
    tripId = request.args.get('trip')
    try:
        if tripUserHandler.checkDbConnection():
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                id_token = auth_header.split(' ')[1]
                decoded_token = auth.verify_id_token(id_token)
                user_email = decoded_token.get('email')
                if tripUserService.checkIfUserHasAuthority(user_email, tripId):
                    logging.info("-----Fetching all users for a trip-----")
                    return jsonify({"Message": tripUserService.fetchUserForTrip(tripId)}), 200
                else:
                    return jsonify({"Error": "User does not has Auth."}), 501
        else:
            return jsonify({"Error": "DB Connection Failed"}), 501
    except Exception as ex:
        return jsonify({"Error": f"Error fetching all users for trip {ex}"}), 500
    finally:
        logging.info("----Finished fetching users for trip-----")


def deleteUser():
    userId = request.args.get('userId')
    tripId = request.args.get('tripId')
    try:
        if tripUserHandler.checkDbConnection():
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                id_token = auth_header.split(' ')[1]
                decoded_token = auth.verify_id_token(id_token)
                user_email = decoded_token.get('email')
                if tripUserService.checkIfUserHasAuthority(user_email, tripId):
                    logging.info("-----Deleting user-----")
                    return jsonify({"Message": tripUserService.deleteUser(userId)}), 200
                else:
                    return jsonify({"Error": "User does not has Auth."}), 501
        else:
            return jsonify({"Error": "DB Connection Failed"}), 501
    except Exception as ex:
        return jsonify({"Error": f"Error deleting user {ex}"}), 500
    finally:
        logging.info("----Finished deleting user-----")


# Can add another one to edit the userName

"""EXPENSE EPS"""


# Fetch expense for a trip
def fetchExpensesForATrip():
    tripId = request.args.get('trip')
    try:
        if tripUserHandler.checkDbConnection():
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                id_token = auth_header.split(' ')[1]
                decoded_token = auth.verify_id_token(id_token)
                user_email = decoded_token.get('email')
                if tripUserService.checkIfUserHasAuthority(user_email, tripId):
                    logging.info("-----Fetching all expenses for a trip-----")
                    return jsonify({"Message": expenseBalanceService.fetchExpensesForTrip(tripId)}), 200
                else:
                    return jsonify({"Error": "User does not has Auth."}), 501
        else:
            return jsonify({"Error": "DB Connection Failed"}), 501
    except Exception as ex:
        return jsonify({"Error": f"Error fetching all expenses for trip {ex}"}), 500
    finally:
        logging.info("----Finished fetching expenses for trip-----")


# Add expense for a trip
def addExpenseForTrip():
    postedData = request.get_json()
    try:
        if tripUserHandler.checkDbConnection():
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                id_token = auth_header.split(' ')[1]
                decoded_token = auth.verify_id_token(id_token)
                user_email = decoded_token.get('email')
                if tripUserService.checkIfUserHasAuthority(user_email, postedData['tripId']):
                    logging.info("-----Adding expense for a trip-----")
                    return jsonify({"Message": expenseBalanceService.addExpenseForTrip(postedData)}), 200
                else:
                    return jsonify({"Error": "User does not has Auth."}), 501
        else:
            return jsonify({"Error": "DB Connection Failed"}), 501
    except Exception as ex:
        return jsonify({"Error": f"Error adding expense for trip {ex}"}), 500
    finally:
        logging.info("----Finished adding expense for trip-----")


# Edit expense for a trip
def editExpenseForTrip():
    postedData = request.get_json()
    try:
        if tripUserHandler.checkDbConnection():
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                id_token = auth_header.split(' ')[1]
                decoded_token = auth.verify_id_token(id_token)
                user_email = decoded_token.get('email')
                if tripUserService.checkIfUserHasAuthority(user_email, postedData['tripId']):
                    logging.info("-----Updating expense for a trip-----")
                    return jsonify({"Message": expenseBalanceService.editExpenseForTrip(postedData['expenseId'],
                                                                                        postedData['body'])}), 200
                else:
                    return jsonify({"Error": "User does not has Auth."}), 501
        else:
            return jsonify({"Error": "DB Connection Failed"}), 501
    except Exception as ex:
        return jsonify({"Error": f"Error updating expense for trip {ex}"}), 500
    finally:
        logging.info("----Finished updating expense for trip-----")


# Delete expense for a trip
def deleteExpenseForTrip():
    expenseId = request.args.get('expenseId')
    tripId = request.args.get('tripId')
    try:
        if tripUserHandler.checkDbConnection():
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                id_token = auth_header.split(' ')[1]
                decoded_token = auth.verify_id_token(id_token)
                user_email = decoded_token.get('email')
                if tripUserService.checkIfUserHasAuthority(user_email, tripId):
                    logging.info("-----Deleting expense for a trip-----")
                    return jsonify({"Message": expenseBalanceService.deleteExpenseFromTrip(expenseId)}), 200
                else:
                    return jsonify({"Error": "User does not has Auth."}), 501
        else:
            return jsonify({"Error": "DB Connection Failed"}), 501
    except Exception as ex:
        return jsonify({"Error": f"Error deleting expense for trip {ex}"}), 500
    finally:
        logging.info("----Finished deleting expense for trip-----")


""" Balances EP """


def fetchBalancesForATrip():
    tripId = request.args.get('trip')
    try:
        if tripUserHandler.checkDbConnection():
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                id_token = auth_header.split(' ')[1]
                decoded_token = auth.verify_id_token(id_token)
                user_email = decoded_token.get('email')
                if tripUserService.checkIfUserHasAuthority(user_email, tripId):
                    logging.info("-----Fetching balance for trip-----")
                    return jsonify({"Message": expenseBalanceService.fetchBalances(tripId)}), 200
                else:
                    return jsonify({"Error": "User does not has Auth."}), 501
        else:
            return jsonify({"Error": "DB Connection Failed"}), 501
    except Exception as ex:
        return jsonify({"Error": f"Error fetching balances for trip{ex}"}), 500
    finally:
        logging.info("----Finished fetching balances for trip-----")
