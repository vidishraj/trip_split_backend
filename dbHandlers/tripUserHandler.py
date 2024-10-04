from util.DBReset import DBReset
from util.queries import Queries


class TripUserHandler(DBReset):

    def __init__(self, dbConnection):
        super().__init__()
        self._dbConnection = dbConnection

    def insertTrip(self, tripData, currencies):
        self._dbConnection.commit()
        cursor = self._dbConnection.cursor()
        cursor.execute(Queries.createTripQuery, tuple([tripData, currencies]))
        self._dbConnection.commit()
        cursor.close()
        return True

    def fetchAllTrips(self):
        self._dbConnection.commit()
        cursor = self._dbConnection.cursor()
        cursor.execute(Queries.fetchTripsQuery)
        trips = cursor.fetchall()
        result = []
        keys = ['tripId', 'tripTitle', 'currencies']
        for trip in trips:
            result.append({keys[i]: value for i, value in enumerate(trip)})
        cursor.close()
        return result

    def fetchUsersForTrip(self, tripId):
        self._dbConnection.commit()
        cursor = self._dbConnection.cursor()
        cursor.execute(Queries.fetchUsersForSpecificTrip, tuple([tripId]))
        users = cursor.fetchall()
        result = []
        keys = ['userId', 'userName', 'tripId']
        for user in users:
            result.append({keys[i]: value for i, value in enumerate(user)})
            result[-1]['deletable'] = not self.checkIfUserHasExpenses(str(user[0]))
        cursor.close()
        return result

    def addUserToTrip(self, user):
        self._dbConnection.commit()
        cursor = self._dbConnection.cursor()
        cursor.execute(Queries.createUser, tuple(user))
        self._dbConnection.commit()
        cursor.close()
        return True

    def checkIfUserHasExpenses(self, user):
        self._dbConnection.commit()
        cursor = self._dbConnection.cursor()
        cursor.execute(Queries.checkIfUserHasExpenses, (user, user))
        count = cursor.fetchall()[0][0]
        cursor.close()
        if count > 0:
            return True
        return False

    def deleteUser(self, user):
        self._dbConnection.commit()
        cursor = self._dbConnection.cursor()
        cursor.execute(Queries.deleteUser, tuple([user]))
        self._dbConnection.commit()
        cursor.close()
        return True
