from dbHandlers.tripUserHandler import TripUserHandler

import random
import string


class TripUserService:
    Handler: TripUserHandler

    def __init__(self, tripUserHandler: TripUserHandler):
        self.Handler = tripUserHandler

    def createTrip(self, tripData, currencies, email):
        newGeneratedId = self.generate_unique_id()
        while self.tripIdExists(newGeneratedId):
            newGeneratedId = self.generate_unique_id()
        userId = self.fetchUserIDFromEmail(email)
        return self.Handler.insertTrip(tripData, ",".join(currencies), newGeneratedId, userId)

    def fetchTrip(self, userEmail):
        userId = self.fetchUserIDFromEmail(userEmail)
        return self.Handler.fetchAllTrips(userId)

    def editTripTitle(self, title, tripId):
        return self.Handler.editTripTitle(title, tripId)

    def createUser(self, userName: str, email: str):
        return self.Handler.createUser(userName, email)

    def addRequestForTrip(self, tripId, email):
        userId = self.fetchUserIDFromEmail(email)
        # User is already added to trip ignore request.
        if not self.checkIfUserHasAuthority(email, tripId):
            return self.Handler.addRequestForTrip(tripId, userId)
        return False

    def fetchTripRequestForTrip(self, tripId):
        return self.Handler.fetchTripRequestForTrip(tripId)

    def registerRequestResponse(self, userId, tripId, response):
        if self.requestExists(userId, tripId):
            if response:
                self.Handler.connectUserToTrip(userId, tripId)
            self.Handler.deleteRequest(userId, tripId)
            return True
        else:
            return False

    def fetchUserForTrip(self, tripId):
        return self.Handler.fetchUsersForTrip(tripId)

    def deleteUser(self, user):
        if not self.Handler.checkIfUserHasExpenses(user):
            return self.Handler.deleteUser(user)
        return False

    def tripIdExists(self, generatedId: str):
        return self.Handler.checkIfTripIdExists(generatedId)

    def fetchUserIDFromEmail(self, email):
        return self.Handler.fetchIdFromEmail(email)

    def checkIfUserHasAuthority(self, email, tripId):
        userId = self.fetchUserIDFromEmail(email)
        return self.Handler.userHasAuthority(userId, tripId)

    def requestExists(self, userId, tripId):
        return self.Handler.requestExists(userId, tripId)

    def tripWithSameNameExists(self, tripTitle, userEmail):
        return self.Handler.tripWithSameNameExists(tripTitle, userEmail)

    def tripHasExpenses(self, tripId):
        if self.Handler.tripHasExpenses(tripId):
            return True
        return False

    def deleteTrip(self, tripId):
        return self.Handler.deleteTrip(tripId)

    @staticmethod
    def generate_unique_id(length=6):
        characters = string.ascii_letters + string.digits
        unique_id = ''.join(random.choices(characters, k=length))
        return unique_id
