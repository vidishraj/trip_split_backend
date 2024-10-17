from util.DBReset import DBReset
from util.queries import Queries
from mysql.connector import Error
from util.logger import Logger


class TripUserHandler(DBReset):

    def __init__(self, dbConnection):
        super().__init__()
        self._dbConnection = dbConnection
        self.logging = Logger().get_logger()

    def insertTrip(self, tripData, currencies, generatedId, userId):
        self._dbConnection.commit()
        cursor = self._dbConnection.cursor()
        cursor.execute(Queries.createTripQuery, tuple([tripData, currencies, generatedId]))
        self.connectUserToTrip(userId, generatedId)
        self._dbConnection.commit()
        cursor.close()
        return True

    def connectUserToTrip(self, userId, tripId):
        self._dbConnection.commit()
        cursor = self._dbConnection.cursor()
        cursor.execute(Queries.connectUserToTrip, tuple([userId, tripId]))
        return

    def fetchIdFromEmail(self, email):
        self._dbConnection.commit()
        cursor = self._dbConnection.cursor()
        cursor.execute(Queries.fetchIdForEmail, tuple([email]))
        users = cursor.fetchall()
        return users[0][0]

    def createUser(self, userName, email):
        self._dbConnection.commit()
        cursor = self._dbConnection.cursor()
        cursor.execute(Queries.createUser, tuple([userName, email]))
        self._dbConnection.commit()
        cursor.close()
        return True

    def checkIfTripIdExists(self, generatedId: str):
        try:
            cursor = self._dbConnection.cursor()
            cursor.execute(Queries.checkIfIdExists, (generatedId,))
            result = cursor.fetchone()
            return result[0] > 0
        except Error as e:
            self.logging.error(f"Error while checking ID existence: {e}")
            return False

    def requestExists(self, userId, tripId):
        try:
            cursor = self._dbConnection.cursor()
            cursor.execute(Queries.checkIfRequestsExists, (userId, tripId))
            result = cursor.fetchone()
            return result[0] > 0
        except Error as e:
            self.logging.error(f"Error while checking request existence: {e}")
            return False

    def fetchAllTrips(self, userEmail):
        self._dbConnection.commit()
        cursor = self._dbConnection.cursor()
        cursor.execute(Queries.fetchTripsQuery, tuple([userEmail]))
        trips = cursor.fetchall()
        result = []
        keys = ['tripIdShared', 'tripTitle', 'currencies']
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
        keys = ['userId', 'userName', 'tripId', 'email']
        for user in users:
            result.append({keys[i]: value for i, value in enumerate(user)})
            result[-1]['deletable'] = not self.checkIfUserHasExpenses(str(user[0]))
        cursor.close()
        return result

    def userHasAuthority(self, userId, tripId):
        try:
            cursor = self._dbConnection.cursor()
            cursor.execute(Queries.checkIfUserHasAuth, tuple([userId, tripId]))
            result = cursor.fetchone()
            return result[0] > 0
        except Error as e:
            self.logging.error(f"Error while checking ID existence: {e}")
            return False

    def fetchTripRequestForTrip(self, tripId):
        self._dbConnection.commit()
        cursor = self._dbConnection.cursor()
        cursor.execute(Queries.fetchTripRequestForTrip, tuple([tripId]))
        users = cursor.fetchall()
        result = []
        keys = ['userId', 'userName', 'email']
        for user in users:
            result.append({keys[i]: value for i, value in enumerate(user)})
            result[-1]['deletable'] = not self.checkIfUserHasExpenses(str(user[0]))
        cursor.close()
        return result


    def addRequestForTrip(self, tripId, userId):
        self._dbConnection.commit()
        cursor = self._dbConnection.cursor()
        cursor.execute(Queries.registerUserRequest, tuple([userId, tripId]))
        self._dbConnection.commit()
        cursor.close()
        return True

    def deleteRequest(self, userId, tripId):
        self._dbConnection.commit()
        cursor = self._dbConnection.cursor()
        cursor.execute(Queries.deleteRequest, tuple([userId, tripId]))
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
