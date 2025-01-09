from sqlalchemy import text
from util.queries import Queries
from mysql.connector import Error
from util.logger import Logger
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, scoped_session


class TripUserHandler:

    def __init__(self, dbConnection: SQLAlchemy):
        super().__init__()
        self._dbConnection = scoped_session(sessionmaker(autocommit=False,
                                                         autoflush=False,
                                                         bind=dbConnection.engine))
        self.logging = Logger().get_logger()

    def insertTrip(self, tripData, currencies, generatedId, userId):
        try:
            self._dbConnection.execute(text(Queries.createTripQuery), {
                'tripTitle': tripData,
                'currencies': currencies,
                'tripIdShared': generatedId
            })
            self.connectUserToTrip(userId, generatedId)
            self._dbConnection.commit()
        except Error as e:
            self._dbConnection.rollback()
            self.logging.error(f"Error inserting trip: {e}")
            return False
        finally:
            self._dbConnection.close()
        return True

    def connectUserToTrip(self, userId, tripId):
        try:
            self._dbConnection.execute(text(Queries.connectUserToTrip), {
                'userId': userId,
                'tripId': tripId
            })
            self._dbConnection.commit()
        except Error as e:
            self._dbConnection.rollback()
            self.logging.error(f"Error connecting user to trip: {e}")
        finally:
            self._dbConnection.close()

    def fetchIdFromEmail(self, email):
        try:
            result = self._dbConnection.execute(text(
                "SELECT userId FROM `travelSchema_v2`.`users` WHERE `email` = :email "), {'email': email})
            user = result.fetchone()
            return user[0] if user else None
        except Error as e:
            self.logging.error(f"Error fetching user ID from email: {e}")
            return None
        finally:
            self._dbConnection.close()

    def createUser(self, userName, email):
        try:
            self._dbConnection.execute(text(Queries.createUser), {
                'userName': userName,
                'email': email
            })
            self._dbConnection.commit()
        except Error as e:
            self._dbConnection.rollback()
            self.logging.error(f"Error creating user: {e}")
            return False
        finally:
            self._dbConnection.close()
        return True

    def checkIfTripIdExists(self, generatedId: str):
        try:
            result = self._dbConnection.execute(text(Queries.checkIfIdExists), {
                'tripIdShared': generatedId
            })
            count = result.fetchone()[0]
            return count > 0
        except Error as e:
            self.logging.error(f"Error checking if trip ID exists: {e}")
            return False
        finally:
            self._dbConnection.close()

    def requestExists(self, userId, tripId):
        try:
            result = self._dbConnection.execute(text(Queries.checkIfRequestsExists), {
                'userId': userId,
                'tripId': tripId
            })
            count = result.fetchone()[0]
            return count > 0
        except Error as e:
            self.logging.error(f"Error checking if request exists: {e}")
            return False
        finally:
            self._dbConnection.close()

    def fetchAllTrips(self, userEmail):
        try:
            result = self._dbConnection.execute(text(Queries.fetchTripsQuery), {'email': userEmail})
            trips = result.fetchall()
            keys = ['tripIdShared', 'tripTitle', 'currencies']
            return [{keys[i]: value for i, value in enumerate(trip)} for trip in trips]
        except Error as e:
            self.logging.error(f"Error fetching all trips: {e}")
            return []
        finally:
            self._dbConnection.close()

    def fetchUsersForTrip(self, tripId):
        try:
            result = self._dbConnection.execute(text(Queries.fetchUsersForSpecificTrip), {
                'tripId': tripId
            })
            users = result.fetchall()
            keys = ['userId', 'userName', 'tripId', 'email']
            return [
                {**{keys[i]: value for i, value in enumerate(user)},
                 'deletable': not self.checkIfUserHasExpenses(str(user[0]))}
                for user in users
            ]
        except Error as e:
            self.logging.error(f"Error fetching users for trip: {e}")
            return []
        finally:
            self._dbConnection.close()

    def userHasAuthority(self, userId, tripId):
        try:
            result = self._dbConnection.execute(text(Queries.checkIfUserHasAuth), {
                'userId': userId,
                'tripId': tripId
            })
            count = result.fetchone()[0]
            return count > 0
        except Error as e:
            self.logging.error(f"Error checking user authority: {e}")
            return False
        finally:
            self._dbConnection.close()

    def fetchTripRequestForTrip(self, tripId):
        try:
            result = self._dbConnection.execute(text(Queries.fetchTripRequestForTrip), {
                'tripId': tripId
            })
            users = result.fetchall()
            keys = ['userId', 'userName', 'email']
            return [
                {**{keys[i]: value for i, value in enumerate(user)},
                 'deletable': not self.checkIfUserHasExpenses(str(user[0]))}
                for user in users
            ]
        except Error as e:
            self.logging.error(f"Error fetching trip request for trip: {e}")
            return []
        finally:
            self._dbConnection.close()

    def addRequestForTrip(self, tripId, userId):
        try:
            self._dbConnection.execute(text(Queries.registerUserRequest), {
                'userId': userId,
                'tripId': tripId
            })
            self._dbConnection.commit()
        except Error as e:
            self._dbConnection.rollback()
            self.logging.error(f"Error adding request for trip: {e}")
            return False
        finally:
            self._dbConnection.close()
        return True

    def deleteRequest(self, userId, tripId):
        try:
            self._dbConnection.execute(text(Queries.deleteRequest), {
                'userId': userId,
                'tripId': tripId
            })
            self._dbConnection.commit()
        except Error as e:
            self._dbConnection.rollback()
            self.logging.error(f"Error deleting request: {e}")
            return False
        finally:
            self._dbConnection.close()
        return True

    def checkIfUserHasExpenses(self, user):
        try:
            result = self._dbConnection.execute(text(Queries.checkIfUserHasExpenses), {
                'userId': user
            })
            count = result.fetchone()[0]
            return count > 0
        except Error as e:
            self.logging.error(f"Error checking if user has expenses: {e}")
            return False
        finally:
            self._dbConnection.close()

    def deleteUser(self, user):
        try:
            self._dbConnection.execute(text(Queries.deleteUser), {
                'userId': user
            })
            self._dbConnection.commit()
        except Error as e:
            self._dbConnection.rollback()
            self.logging.error(f"Error deleting user: {e}")
            return False
        finally:
            self._dbConnection.close()
        return True
