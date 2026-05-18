from util.logger import Logger
from util.auth import require_auth, require_trip_auth
from flask import request, jsonify, g

# tripId extractors used with @require_trip_auth
_trip_from_arg = lambda r: r.args.get('trip')
_tripId_from_arg = lambda r: r.args.get('tripId')
_tripId_from_json = lambda r: (r.get_json(silent=True) or {}).get('tripId')
_tripId_from_json_body = lambda r: ((r.get_json(silent=True) or {}).get('body') or {}).get('tripId')


class TravelEP:

    def __init__(self, tripUserService, expenseBalanceService, notesService, individualSpendingService):
        self.logging = Logger().get_logger()
        self.tripUserService = tripUserService
        self.expenseBalanceService = expenseBalanceService
        self.notesService = notesService
        self.individualSpendingService = individualSpendingService

    """ Trip EPs """

    @require_auth
    def createTrip(self):
        try:
            payload = request.get_json()
            self.logging.info(f"Creating trip for {g.user_email}")
            if self.tripUserService.tripWithSameNameExists(g.user_email, payload['trip']):
                return jsonify({"Error": "Trip with this name already exists."}), 409
            return jsonify({"Message": self.tripUserService.createTrip(
                payload['trip'], payload['currencies'], g.user_email)}), 200
        except Exception as ex:
            self.logging.error(f"Error creating trip: {ex}")
            return jsonify({"Error": f"Error creating trip: {ex}"}), 500

    @require_auth
    @require_trip_auth(_tripId_from_arg)
    def deleteTrip(self):
        try:
            if self.tripUserService.tripHasExpenses(g.trip_id):
                return jsonify({"Error": "Trip has expenses attached. Cannot delete it."}), 409
            return jsonify({"Message": self.tripUserService.deleteTrip(g.trip_id)}), 200
        except Exception as ex:
            self.logging.error(f"Error deleting trip: {ex}")
            return jsonify({"Error": f"Error deleting trip: {ex}"}), 500

    @require_auth
    def fetchTrips(self):
        try:
            return jsonify({"Message": self.tripUserService.fetchTrip(g.user_email)}), 200
        except Exception as ex:
            self.logging.error(f"Error fetching trips: {ex}")
            return jsonify({"Error": f"Error fetching trips: {ex}"}), 500

    @require_auth
    @require_trip_auth(_tripId_from_json)
    def editTripTitle(self):
        try:
            payload = request.get_json()
            return jsonify({"Message": self.tripUserService.editTripTitle(
                payload['title'], g.trip_id)}), 200
        except Exception as ex:
            self.logging.error(f"Error updating title for trip: {ex}")
            return jsonify({"Error": f"Error updating title for trip: {ex}"}), 500

    """ User EPs """

    def createUser(self):
        # Signup endpoint — intentionally unauthenticated.
        try:
            payload = request.get_json(force=True)
            return jsonify({"Message": self.tripUserService.createUser(
                payload['userName'], payload['email'])}), 200
        except Exception as ex:
            self.logging.error(f"Error creating user: {ex}")
            return jsonify({"Error": f"Error creating new user: {ex}"}), 500

    @require_auth
    def setUserRequest(self):
        # Intentionally NOT @require_trip_auth — caller is requesting to join a trip
        # they don't yet belong to.
        try:
            payload = request.get_json(force=True)
            tripId = payload['tripId']
            if not self.tripUserService.tripIdExists(tripId):
                return jsonify({"Error": "Trip does not exist. Check id!"}), 404
            return jsonify({"Message": self.tripUserService.addRequestForTrip(
                tripId, g.user_email)}), 200
        except Exception as ex:
            self.logging.error(f"Error adding request for trip: {ex}")
            return jsonify({"Error": f"Error adding request for user to trip: {ex}"}), 500

    @require_auth
    @require_trip_auth(_trip_from_arg)
    def fetchTripRequestForTrip(self):
        try:
            return jsonify({"Message": self.tripUserService.fetchTripRequestForTrip(g.trip_id)}), 200
        except Exception as ex:
            self.logging.error(f"Error fetching trip requests: {ex}")
            return jsonify({"Error": f"Error fetching all trip requests for trip: {ex}"}), 500

    @require_auth
    @require_trip_auth(_tripId_from_json)
    def registerRequestResponse(self):
        try:
            payload = request.get_json(force=True)
            return jsonify({"Message": self.tripUserService.registerRequestResponse(
                payload['userId'], g.trip_id, payload['response'])}), 200
        except Exception as ex:
            self.logging.error(f"Error registering response: {ex}")
            return jsonify({"Error": f"Error registering response for trip request: {ex}"}), 500

    @require_auth
    @require_trip_auth(_trip_from_arg)
    def fetchUsersForTrip(self):
        try:
            return jsonify({"Message": self.tripUserService.fetchUserForTrip(g.trip_id)}), 200
        except Exception as ex:
            self.logging.error(f"Error fetching users for trip: {ex}")
            return jsonify({"Error": f"Error fetching all users for trip: {ex}"}), 500

    @require_auth
    @require_trip_auth(_tripId_from_arg)
    def deleteUser(self):
        try:
            userId = request.args.get('userId')
            return jsonify({"Message": self.tripUserService.deleteUser(userId)}), 200
        except Exception as ex:
            self.logging.error(f"Error deleting user: {ex}")
            return jsonify({"Error": f"Error deleting user: {ex}"}), 500

    """ Expense EPs """

    @require_auth
    @require_trip_auth(_trip_from_arg)
    def fetchExpensesForATrip(self):
        try:
            return jsonify({"Message": self.expenseBalanceService.fetchExpensesForTrip(g.trip_id)}), 200
        except Exception as ex:
            self.logging.error(f"Error fetching expenses: {ex}")
            return jsonify({"Error": f"Error fetching all expenses for trip: {ex}"}), 500

    @require_auth
    @require_trip_auth(_tripId_from_json)
    def addExpenseForTrip(self):
        try:
            payload = request.get_json()
            result = self.expenseBalanceService.addExpenseForTrip(payload)
            if not result:
                return jsonify({"Error": "Failed to add expense."}), 500
            return jsonify({"Message": result}), 200
        except Exception as ex:
            self.logging.error(f"Error adding expense: {ex}")
            return jsonify({"Error": f"Error adding expense for trip: {ex}"}), 500

    @require_auth
    @require_trip_auth(_tripId_from_json_body)
    def editExpenseForTrip(self):
        try:
            payload = request.get_json()
            return jsonify({"Message": self.expenseBalanceService.editExpenseForTrip(
                payload['expenseId'], payload['body'])}), 200
        except Exception as ex:
            self.logging.error(f"Error updating expense: {ex}")
            return jsonify({"Error": f"Error updating expense for trip: {ex}"}), 500

    @require_auth
    @require_trip_auth(_tripId_from_arg)
    def deleteExpenseForTrip(self):
        try:
            expenseId = request.args.get('expenseId')
            return jsonify({"Message": self.expenseBalanceService.deleteExpenseFromTrip(expenseId)}), 200
        except Exception as ex:
            self.logging.error(f"Error deleting expense: {ex}")
            return jsonify({"Error": f"Error deleting expense for trip: {ex}"}), 500

    """ Balance EPs """

    @require_auth
    @require_trip_auth(_trip_from_arg)
    def fetchBalancesForATrip(self):
        try:
            return jsonify({"Message": self.expenseBalanceService.fetchBalanceV2(g.trip_id)}), 200
        except Exception as ex:
            self.logging.error(f"Error fetching balances: {ex}")
            return jsonify({"Error": f"Error fetching balances for trip: {ex}"}), 500

    @require_auth
    @require_trip_auth(_trip_from_arg)
    def fetchIndividualBalance(self):
        try:
            return jsonify({"Message": self.expenseBalanceService.fetchIndividualBalance(g.trip_id)}), 200
        except Exception as ex:
            self.logging.error(f"Error fetching individual balance: {ex}")
            return jsonify({"Error": f"Error fetching individual balances for trip: {ex}"}), 500

    @require_auth
    @require_trip_auth(_tripId_from_arg)
    def fetchIndividualSpending(self):
        try:
            return jsonify({"Message": self.individualSpendingService.fetchIndividualSpending(g.trip_id)}), 200
        except Exception as ex:
            self.logging.error(f"Error fetching individual spending: {ex}")
            return jsonify({"Error": f"Error fetching individual spending for trip: {ex}"}), 500

    """ Notes EPs """

    @require_auth
    @require_trip_auth(_tripId_from_arg)
    def fetchNotesForATrip(self):
        try:
            page = request.args.get('page')
            if not page:
                return jsonify({"Error": "Missing page."}), 400
            return jsonify({"Message": self.notesService.fetchNotesForATrip(g.trip_id, int(page))}), 200
        except Exception as ex:
            self.logging.error(f"Error fetching notes: {ex}")
            return jsonify({"Error": f"Error fetching notes for trip: {ex}"}), 500

    @require_auth
    @require_trip_auth(_tripId_from_json)
    def createNote(self):
        try:
            payload = request.get_json()
            payload['userId'] = self.tripUserService.fetchUserIDFromEmail(g.user_email)
            return jsonify({"Message": self.notesService.createNote(payload)}), 200
        except Exception as ex:
            self.logging.error(f"Error creating note: {ex}")
            return jsonify({"Error": f"Error creating notes for trip: {ex}"}), 500

    @require_auth
    @require_trip_auth(_tripId_from_json)
    def editNote(self):
        try:
            payload = request.get_json()
            payload['userId'] = self.tripUserService.fetchUserIDFromEmail(g.user_email)
            return jsonify({"Message": self.notesService.editNote(payload)}), 200
        except Exception as ex:
            self.logging.error(f"Error editing note: {ex}")
            return jsonify({"Error": f"Error editing notes for trip: {ex}"}), 500

    @require_auth
    @require_trip_auth(_tripId_from_arg)
    def deleteNote(self):
        try:
            noteId = request.args.get('noteId')
            if not noteId:
                return jsonify({"Error": "Missing noteId."}), 400
            userId = self.tripUserService.fetchUserIDFromEmail(g.user_email)
            return jsonify({"Message": self.notesService.deleteNote(userId, g.trip_id, noteId)}), 200
        except Exception as ex:
            self.logging.error(f"Error deleting note: {ex}")
            return jsonify({"Error": f"Error deleting notes for trip: {ex}"}), 500
