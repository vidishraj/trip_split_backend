from util.logger import Logger
from flask import request, jsonify
from firebase_admin import auth


class TravelEP:

    def __init__(self, tripUserService, expenseBalanceService):
        self.logging = Logger().get_logger()
        self.tripUserService = tripUserService
        self.expenseBalanceService = expenseBalanceService

    def createTrip(self):
        self.logging.info("----New Sign up. Adding Use to DB-----")
        try:
            postedDate = request.get_json(force=True)
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                id_token = auth_header.split(' ')[1]
                decoded_token = auth.verify_id_token(id_token)
                user_email = decoded_token.get('email')
                self.logging.info(f"Fetched email. Adding user with email {user_email}")
                if self.tripUserService.tripWithSameNameExists(user_email, postedDate['trip']):
                    return jsonify({"Error": " Invalid trip name"}), 401
                if user_email:
                    return jsonify(
                        {"Message": self.tripUserService.createTrip(postedDate['trip'], postedDate['currencies'],
                                                                    user_email)}), \
                        200
            else:
                return jsonify({"Error": " Auth failed"}), 501
        except Exception as ex:
            self.logging.error(f"Error inserting user during sign up {ex}")
            return jsonify({"Error": f"Error inserting user during sign up {ex}"}), 500
        finally:
            self.logging.info("----Finished adding new user during sign up-----")

    def fetchTrips(self):
        self.logging.info("---Fetching all trips for user---- ")
        try:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                id_token = auth_header.split(' ')[1]
                decoded_token = auth.verify_id_token(id_token)
                user_email = decoded_token.get('email')
                if user_email:
                    return jsonify({"Message": self.tripUserService.fetchTrip(user_email)}), 200
            else:
                return jsonify({"Error": "DB Connection Failed or Auth failed."}), 501
        except Exception as ex:
            self.logging.error(f"Error fetching trips {ex}")
            return jsonify({"Error": f"Error fetching trips {ex}"}), 500
        finally:
            self.logging.info("----Finished fetching trips-----")

    # Edit trip title
    def editTripTitle(self):
        postedData = request.get_json()
        try:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                id_token = auth_header.split(' ')[1]
                decoded_token = auth.verify_id_token(id_token)
                user_email = decoded_token.get('email')
                if self.tripUserService.checkIfUserHasAuthority(user_email, postedData['tripId']):
                    self.logging.info("-----Updating title for a trip-----")
                    return jsonify({"Message": self.tripUserService.editTripTitle(postedData['title'],
                                                                                  postedData['tripId'])}), 200
                else:
                    return jsonify({"Error": "User does not has Auth."}), 501

        except Exception as ex:
            return jsonify({"Error": f"Error updating title for trip {ex}"}), 500
        finally:
            self.logging.info("----Finished updating title for trip-----")

    """ User EPs """

    def createUser(self):
        try:
            postedDate = request.get_json(force=True)
            self.logging.info("-----Creating New User-----")
            return jsonify(
                {"Message": self.tripUserService.createUser(postedDate['userName'], postedDate['email'])}), 200
        except Exception as ex:
            self.logging.error(f"Error creating user {ex}")
            return jsonify({"Error": f"Error creating new user {ex}"}), 500
        finally:
            self.logging.info("----Finished creating new user-----")

    def setUserRequest(self):
        postedData = request.get_json(force=True)
        try:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                id_token = auth_header.split(' ')[1]
                decoded_token = auth.verify_id_token(id_token)
                user_email = decoded_token.get('email')
                tripId = postedData['tripId']
                self.logging.info(f"-----Adding request for trip {tripId} {user_email}-----")
                return jsonify({"Message": self.tripUserService.addRequestForTrip(tripId, user_email)}), 200

        except Exception as ex:
            return jsonify({"Error": f"Error adding request for user to trip {ex}"}), 500
        finally:
            self.logging.info("----Finished adding request for user to trip-----")

    def fetchTripRequestForTrip(self):
        tripId = request.args.get('trip')
        try:
            self.logging.info("-----Fetching all trip requests for a trip-----")
            return jsonify({"Message": self.tripUserService.fetchTripRequestForTrip(tripId)}), 200
        except Exception as ex:
            return jsonify({"Error": f"Error fetching all trip requests for trip {ex}"}), 500
        finally:
            self.logging.info("----Finished fetching trip requests for trip-----")

    def registerRequestResponse(self):
        postedData = request.get_json(force=True)
        try:
            userId = postedData['userId']
            tripId = postedData['tripId']
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                id_token = auth_header.split(' ')[1]
                decoded_token = auth.verify_id_token(id_token)
                user_email = decoded_token.get('email')
                if self.tripUserService.checkIfUserHasAuthority(user_email, tripId):
                    response = postedData['response']
                    self.logging.info("-----Registering response for trip request-----")
                    return jsonify(
                        {"Message": self.tripUserService.registerRequestResponse(userId, tripId, response)}), 200
                else:
                    return jsonify({"Error": "User does not has Auth."}), 501
        except Exception as ex:
            return jsonify({"Error": f"Error registering response for trip request {ex}"}), 500
        finally:
            self.logging.info("----Finished registering response for trip request-----")

    def fetchUsersForTrip(self):
        tripId = request.args.get('trip')
        try:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                id_token = auth_header.split(' ')[1]
                decoded_token = auth.verify_id_token(id_token)
                user_email = decoded_token.get('email')
                if self.tripUserService.checkIfUserHasAuthority(user_email, tripId):
                    self.logging.info("-----Fetching all users for a trip-----")
                    return jsonify({"Message": self.tripUserService.fetchUserForTrip(tripId)}), 200
                else:
                    return jsonify({"Error": "User does not has Auth."}), 501
        except Exception as ex:
            return jsonify({"Error": f"Error fetching all users for trip {ex}"}), 500
        finally:
            self.logging.info("----Finished fetching users for trip-----")

    def deleteUser(self):
        userId = request.args.get('userId')
        tripId = request.args.get('tripId')
        try:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                id_token = auth_header.split(' ')[1]
                decoded_token = auth.verify_id_token(id_token)
                user_email = decoded_token.get('email')
                if self.tripUserService.checkIfUserHasAuthority(user_email, tripId):
                    self.logging.info("-----Deleting user-----")
                    return jsonify({"Message": self.tripUserService.deleteUser(userId)}), 200
                else:
                    return jsonify({"Error": "User does not has Auth."}), 501
        except Exception as ex:
            return jsonify({"Error": f"Error deleting user {ex}"}), 500
        finally:
            self.logging.info("----Finished deleting user-----")

    # Can add another one to edit the userName

    """EXPENSE EPS"""

    # Fetch expense for a trip
    def fetchExpensesForATrip(self):
        tripId = request.args.get('trip')
        try:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                id_token = auth_header.split(' ')[1]
                decoded_token = auth.verify_id_token(id_token)
                user_email = decoded_token.get('email')
                if self.tripUserService.checkIfUserHasAuthority(user_email, tripId):
                    self.logging.info("-----Fetching all expenses for a trip-----")
                    return jsonify({"Message": self.expenseBalanceService.fetchExpensesForTrip(tripId)}), 200
                else:
                    return jsonify({"Error": "User does not has Auth."}), 501

        except Exception as ex:
            return jsonify({"Error": f"Error fetching all expenses for trip {ex}"}), 500
        finally:
            self.logging.info("----Finished fetching expenses for trip-----")

    # Add expense for a trip
    def addExpenseForTrip(self):
        postedData = request.get_json()
        try:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                id_token = auth_header.split(' ')[1]
                decoded_token = auth.verify_id_token(id_token)
                user_email = decoded_token.get('email')
                if self.tripUserService.checkIfUserHasAuthority(user_email, postedData['tripId']):
                    self.logging.info("-----Adding expense for a trip-----")
                    return jsonify({"Message": self.expenseBalanceService.addExpenseForTrip(postedData)}), 200
                else:
                    return jsonify({"Error": "User does not has Auth."}), 501

        except Exception as ex:
            return jsonify({"Error": f"Error adding expense for trip {ex}"}), 500
        finally:
            self.logging.info("----Finished adding expense for trip-----")

    # Edit expense for a trip
    def editExpenseForTrip(self):
        postedData = request.get_json()
        try:

            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                id_token = auth_header.split(' ')[1]
                decoded_token = auth.verify_id_token(id_token)
                user_email = decoded_token.get('email')
                if self.tripUserService.checkIfUserHasAuthority(user_email, postedData['body']['tripId']):
                    self.logging.info("-----Updating expense for a trip-----")
                    return jsonify({"Message": self.expenseBalanceService.editExpenseForTrip(postedData['expenseId'],
                                                                                             postedData['body'])}), 200
                else:
                    return jsonify({"Error": "User does not has Auth."}), 501

        except Exception as ex:
            return jsonify({"Error": f"Error updating expense for trip {ex}"}), 500
        finally:
            self.logging.info("----Finished updating expense for trip-----")

    # Delete expense for a trip
    def deleteExpenseForTrip(self):
        expenseId = request.args.get('expenseId')
        tripId = request.args.get('tripId')
        try:

            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                id_token = auth_header.split(' ')[1]
                decoded_token = auth.verify_id_token(id_token)
                user_email = decoded_token.get('email')
                if self.tripUserService.checkIfUserHasAuthority(user_email, tripId):
                    self.logging.info("-----Deleting expense for a trip-----")
                    return jsonify({"Message": self.expenseBalanceService.deleteExpenseFromTrip(expenseId)}), 200
                else:
                    return jsonify({"Error": "User does not has Auth."}), 501

        except Exception as ex:
            return jsonify({"Error": f"Error deleting expense for trip {ex}"}), 500
        finally:
            self.logging.info("----Finished deleting expense for trip-----")

    """ Balances EP """

    def fetchBalancesForATrip(self):
        tripId = request.args.get('trip')
        try:

            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                id_token = auth_header.split(' ')[1]
                decoded_token = auth.verify_id_token(id_token)
                user_email = decoded_token.get('email')
                if self.tripUserService.checkIfUserHasAuthority(user_email, tripId):
                    self.logging.info("-----Fetching balance for trip-----")
                    return jsonify({"Message": self.expenseBalanceService.fetchBalances(tripId)}), 200
                else:
                    return jsonify({"Error": "User does not has Auth."}), 501

        except Exception as ex:
            return jsonify({"Error": f"Error fetching balances for trip{ex}"}), 500
        finally:
            self.logging.info("----Finished fetching balances for trip-----")
