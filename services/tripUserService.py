from dbHandlers.tripUserHandler import TripUserHandler


class TripUserService:
    Handler: TripUserHandler

    def __init__(self, tripUserHandler: TripUserHandler):
        self.Handler = tripUserHandler

    def createTrip(self, tripData, currencies):
        return self.Handler.insertTrip(tripData, ",".join(currencies))

    def fetchTrip(self):
        return self.Handler.fetchAllTrips()

    def fetchUserForTrip(self, tripId):
        self.Handler.checkIfUserHasExpenses('3')
        return self.Handler.fetchUsersForTrip(tripId)

    def addUserToTrip(self, user):
        return self.Handler.addUserToTrip(user)

    def deleteUser(self, user):
        if not self.Handler.checkIfUserHasExpenses(user):
            return self.Handler.deleteUser(user)
        return False
