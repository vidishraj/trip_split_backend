from dbHandlers.tripUserHandler import TripUserHandler


class TripUserService:
    Handler: TripUserHandler

    def __init__(self, tripUserHandler: TripUserHandler):
        self.Handler = tripUserHandler

    def createTrip(self, tripData):
        return self.Handler.insertTrip(tripData)

    def fetchTrip(self):
        return self.Handler.fetchAllTrips()

    def fetchUserForTrip(self, tripId):
        return self.Handler.fetchUsersForTrip(tripId)

    def addUserToTrip(self, user):
        return self.Handler.addUserToTrip(user)


