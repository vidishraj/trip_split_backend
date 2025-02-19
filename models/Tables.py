from datetime import datetime
from models.Base import Base
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, create_engine, Boolean


class User(Base):
    __tablename__ = 'users'

    userId = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    userName = Column(String(100), nullable=False, unique=True)
    email = Column(String(250), nullable=False, unique=True)

    def __repr__(self):
        return f"<User {self.userName}>"


class Trip(Base):
    __tablename__ = 'trips'

    tripIdShared = Column(String(6), primary_key=True)
    tripTitle = Column(String(150), nullable=False)
    currencies = Column(String(500), nullable=False)

    def __repr__(self):
        return f"<Trip {self.tripTitle}>"


class Expense(Base):
    __tablename__ = 'expenses'

    expenseId = Column(Integer, primary_key=True, autoincrement=True)
    expenseDate = Column(DateTime, nullable=False, default=datetime.utcnow)
    expenseDesc = Column(String(350), nullable=False)
    expenseAmount = Column(Float, nullable=False)
    expensePaidBy = Column(Integer, ForeignKey('users.userId', ondelete='CASCADE'), nullable=False)
    expenseSplitBw = Column(String(2000), nullable=False)
    tripId = Column(String(6), ForeignKey('trips.tripIdShared', ondelete='CASCADE'), nullable=False)
    expenseSelf = Column(Boolean, nullable=False, default=0)

    def __repr__(self):
        return f"<Expense {self.expenseDesc}>"


class Balance(Base):
    __tablename__ = 'Balance'

    balanceId = Column(Integer, primary_key=True, autoincrement=True)
    tripId = Column(String(6), ForeignKey('trips.tripIdShared', ondelete='CASCADE'), primary_key=True)
    userId = Column(Integer, ForeignKey('users.userId'), primary_key=True)
    expenseId = Column(Integer, ForeignKey('expenses.expenseId', ondelete='CASCADE'), primary_key=True)
    amount = Column(Float, nullable=False)
    borrowedFrom = Column(Integer, ForeignKey('users.userId'), nullable=True)

    def __repr__(self):
        return f"<Balance tripId={self.tripId} userId={self.userId} expenseId={self.expenseId}>"


class TripRequest(Base):
    __tablename__ = 'tripRequest'

    tripId = Column(String(6), ForeignKey('trips.tripIdShared', ondelete='CASCADE'), primary_key=True)
    userId = Column(Integer, ForeignKey('users.userId', ondelete='CASCADE'), primary_key=True)

    def __repr__(self):
        return f"<TripRequest tripId={self.tripId} userId={self.userId}>"


class UserTrip(Base):
    __tablename__ = 'userTrips'

    userId = Column(Integer, ForeignKey('users.userId', ondelete='CASCADE'), primary_key=True)
    tripId = Column(String(6), ForeignKey('trips.tripIdShared', ondelete='CASCADE'), primary_key=True)

    def __repr__(self):
        return f"<UserTrip userId={self.userId} tripId={self.tripId}>"
