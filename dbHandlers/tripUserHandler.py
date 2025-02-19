from sqlalchemy import func

from models import Trip, UserTrip, User, TripRequest, Expense
from mysql.connector import Error
from util.logger import Logger

from flask import g


class TripUserHandler:
    @property
    def _dbConnection(self):
        return g.db

    def __init__(self):
        super().__init__()
        self.logging = Logger().get_logger()

    def insertTrip(self, tripData, currencies, generatedId, userId):
        try:
            trip = Trip(
                tripTitle=tripData,
                currencies=currencies,
                tripIdShared=generatedId
            )
            self._dbConnection.session.add(trip)
            self.connectUserToTrip(userId, generatedId)
            self._dbConnection.session.commit()
            return True
        except Error as e:
            self._dbConnection.session.rollback()
            self.logging.error(f"Error inserting trip: {e}")
            return False

    def connectUserToTrip(self, userId, tripId):
        try:
            userTrip = UserTrip(
                userId=userId,
                tripId=tripId
            )
            self._dbConnection.session.add(userTrip)
            # Not sure if this is okay, check later
            self._dbConnection.session.commit()
        except Error as e:
            self._dbConnection.session.rollback()
            self.logging.error(f"Error connecting user to trip: {e}")

    def fetchIdFromEmail(self, email):
        try:
            user = self._dbConnection.session.query(User).filter_by(email=email).first()
            return user.userId if user else None
        except Error as e:
            self.logging.error(f"Error fetching user ID from email: {e}")
            return None

    def createUser(self, userName, email):
        try:
            user = User(
                userName=userName,
                email=email
            )
            self._dbConnection.session.add(user)
            self._dbConnection.session.commit()
            return True
        except Error as e:
            self._dbConnection.session.rollback()
            self.logging.error(f"Error creating user: {e}")
            return False

    def editTripTitle(self, title, tripId):
        try:
            # Fetch the expense to update
            trip = self._dbConnection.session.query(Trip).filter_by(tripIdShared=tripId).first()

            if not trip:
                # If no expense found, return False
                return False
            trip.tripTitle = title
            self._dbConnection.session.commit()
            return True
        except Error as e:
            self._dbConnection.session.rollback()
            self.logging.error(f"Error updating trip title: {e}")
            return False

    def checkIfTripIdExists(self, generatedId: str):
        try:
            count = self._dbConnection.session.query(self._dbConnection.func.count(Trip.tripIdShared)). \
                filter_by(tripIdShared=generatedId).scalar()
            return count > 0
        except Error as e:
            self.logging.error(f"Error checking if trip ID exists: {e}")
            return False

    def requestExists(self, userId, tripId):
        try:
            count = self._dbConnection.session.query(self._dbConnection.func.count(TripRequest.tripId)). \
                filter_by(tripId=tripId).filter_by(userId=userId).scalar()
            return count > 0
        except Error as e:
            self.logging.error(f"Error checking if request exists: {e}")
            return False

    def fetchAllTrips(self, userId):
        try:
            trips = (
                self._dbConnection.session.query(Trip.tripIdShared, Trip.tripTitle, Trip.currencies)
                .join(UserTrip, Trip.tripIdShared == UserTrip.tripId)
                .filter(UserTrip.userId == userId)
                .all()
            )
            return [
                {
                    'tripIdShared': trip.tripIdShared,
                    'tripTitle': trip.tripTitle,
                    'currencies': trip.currencies,
                }
                for trip in trips
            ]
        except Error as e:
            self.logging.error(f"Error fetching all trips: {e}")
            return []

    def fetchUsersForTrip(self, tripId):
        try:
            users = (
                self._dbConnection.session.query(User.userId, User.userName, UserTrip.tripId, User.email)
                .join(UserTrip, User.userId == UserTrip.userId)
                .filter(UserTrip.tripId == tripId)
                .all()
            )
            return [
                {
                    'userId': user.userId,
                    'userName': user.userName,
                    'tripId': user.tripId,
                    'email': user.email,
                    'deletable': not self.checkIfUserHasExpenses(str(user.userId)),
                }
                for user in users
            ]
        except Error as e:
            self.logging.error(f"Error fetching users for trip: {e}")
            return []

    def userHasAuthority(self, userId, tripId):
        try:
            count = self._dbConnection.session.query(self._dbConnection.func.count(UserTrip.tripId)). \
                filter_by(tripId=tripId).filter_by(userId=userId).scalar()
            return count > 0
        except Error as e:
            self.logging.error(f"Error checking user authority: {e}")
            return False

    def fetchTripRequestForTrip(self, tripId):
        try:
            users = (
                self._dbConnection.session.query(User.userId, User.userName, User.email)
                .join(TripRequest, TripRequest.userId == User.userId)
                .filter(TripRequest.tripId == tripId)
                .all()
            )
            return [
                {
                    'userId': user.userId,
                    'userName': user.userName,
                    'email': user.email,
                    'deletable': not self.checkIfUserHasExpenses(str(user.userId)),
                }
                for user in users
            ]
        except Error as e:
            self.logging.error(f"Error fetching trip request for trip: {e}")
            return []

    def addRequestForTrip(self, tripId, userId):
        try:
            request = TripRequest(
                userId=userId,
                tripId=tripId
            )
            self._dbConnection.session.add(request)
            self._dbConnection.session.commit()
            return True
        except Error as e:
            self._dbConnection.session.rollback()
            self.logging.error(f"Error adding request for trip: {e}")
            return False

    def deleteRequest(self, userId, tripId):
        try:
            self._dbConnection.session.query(TripRequest).filter(
                TripRequest.userId == userId,
                TripRequest.tripId == tripId
            ).delete()

            # Commit the transaction
            self._dbConnection.session.commit()
            return True
        except Error as e:
            self._dbConnection.session.rollback()
            self.logging.error(f"Error deleting request: {e}")
            return False

    def checkIfUserHasExpenses(self, user):
        try:
            count = (
                self._dbConnection.session.query(func.count())
                .filter(
                    self._dbConnection.or_(
                        func.json_contains(Expense.expenseSplitBw, f'"{user}"', '$'),
                        Expense.expensePaidBy == user
                    )
                )
                .scalar()
            )
            return count > 0
        except Error as e:
            self.logging.error(f"Error checking if user has expenses: {e}")
            return False

    def tripWithSameNameExists(self, userEmail, tripTitle):
        try:
            # Fetch userId of the user
            user = self._dbConnection.session.query(User).filter_by(email=userEmail).first()
            if user is not None:
                userId = user.userId
                # Fetch tripIds with same name
                trips = self._dbConnection.session.query(Trip.tripIdShared).filter_by(tripTitle=tripTitle).all()
                tripIdList = [trip[0] for trip in trips]

                # Fetch userTrips
                userTrips = self._dbConnection.session.query(UserTrip.tripId).filter_by(userId=userId).all()

                for trip in userTrips:
                    if trip.tripId in tripIdList:
                        return True
            return False
        except Error as e:
            self.logging.error(f"Error checking if user has expenses: {e}")
            return False

    def deleteUser(self, user):
        try:
            self._dbConnection.session.query(User).filter(
                User.userId == user
            ).delete()
            self._dbConnection.session.commit()
            return True
        except Error as e:
            self._dbConnection.session.rollback()
            self.logging.error(f"Error deleting user: {e}")
            return False

    def deleteTrip(self, tripId):
        try:
            self._dbConnection.session.query(Trip).filter(
                Trip.tripIdShared == tripId
            ).delete()
            self._dbConnection.session.commit()
            return True
        except Error as e:
            self._dbConnection.session.rollback()
            self.logging.error(f"Error deleting trip: {e}")
            return False

    def tripHasExpenses(self, tripId):
        try:
            count = self._dbConnection.session.query(self._dbConnection.func.count(Expense.tripId)). \
                filter_by(tripId=tripId).scalar()
            return count > 0
        except Error as e:
            self._dbConnection.session.rollback()
            self.logging.error(f"Error checking if trip has expenses: {e}")
            # Prevent deletion on error if trip exists
            return True
