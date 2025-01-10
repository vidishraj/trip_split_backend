import os

from flask import Flask

from controllers.travelEP import TravelEP
from dbHandlers.expenseBalanceHandler import ExpenseBalanceHandler
from dbHandlers.tripUserHandler import TripUserHandler
from services.expenseBalanceService import ExpenseBalanceService
from services.tripUserService import TripUserService
from util.logger import Logger
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials
import models
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import OperationalError

import logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect


class FlaskApp(Flask):
    db: SQLAlchemy
    logger: logging.Logger

    def __init__(self, import_name: str):
        load_dotenv()
        super().__init__(import_name)
        self.app = Flask(__name__)
        self.logger = Logger().get_logger()
        CORS(self.app)
        self._setup_config()
        self._setup_database()
        self._setup_instances()
        # Init firebase
        self.logger.info("Setting up firebase admin creds")
        cred = credentials.Certificate("./serviceAccountKey.json")
        firebase_admin.initialize_app(cred)

        self.setup_routes()
        self.logger.info("Finished setting up routes...")

    def _setup_config(self):
        """Set up configuration."""
        self.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.config['SQLALCHEMY_POOL_RECYCLE'] = 300

    def _setup_instances(self):
        """Initialize application instances."""
        with self.app_context():
            tripUserHandler = TripUserHandler(self.db)
            expenseBalanceHandler = ExpenseBalanceHandler(self.db)
            tripUserService = TripUserService(tripUserHandler)
            expenseBalanceService = ExpenseBalanceService(expenseBalanceHandler)
            self.travelEP = TravelEP(tripUserService, expenseBalanceService)

    def _setup_database(self):
        """Set up database connection and create tables."""
        # Connect to the database server
        dbUrl = str(self.config['SQLALCHEMY_DATABASE_URI']).replace(
            self.config["SQLALCHEMY_DATABASE_URI"].split("/")[-1], '')
        engine = create_engine(dbUrl, echo=False)

        # Extract schema name from the DATABASE_URL
        schema_name = self.config["SQLALCHEMY_DATABASE_URI"].split("/")[-1]

        try:
            with engine.connect() as connection:
                # Check if the schema exists
                result = connection.execute(
                    text(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = :schema"),
                    {"schema": schema_name}
                ).fetchone()

                # Create the schema if it doesn't exist
                if not result:
                    self.logger.info(f"Schema '{schema_name}' does not exist. Creating schema.")
                    connection.execute(text(f"CREATE SCHEMA {schema_name}"))
                else:
                    self.logger.info(f"Schema '{schema_name}' already exists.")
        except OperationalError as e:
            self.logger.error("Database connection error: " + str(e))
            raise
        self.db = SQLAlchemy(self, model_class=models.Base)
        with self.app_context():
            self.logger.info("Creating database tables if not exist.")
            inspector = inspect(self.db.engine)

            existing_tables_before = inspector.get_table_names()
            self.db.create_all()
            existing_tables_after = inspector.get_table_names()
            new_tables = set(existing_tables_after) - set(existing_tables_before)
            if new_tables:
                self.logger.info(f"New tables created: {new_tables}")
            else:
                self.logger.info("No new tables created.")

    def setup_routes(self):
        # Trip EPS
        self.app.add_url_rule('/createTrip', methods=['POST'], view_func=self.travelEP.createTrip)
        self.app.add_url_rule('/fetchTrips', methods=['GET'], view_func=self.travelEP.fetchTrips)
        # User based EPS
        self.app.add_url_rule('/createUser', methods=['POST'], view_func=self.travelEP.createUser)
        self.app.add_url_rule('/sendTripUserRequest', methods=['POST'], view_func=self.travelEP.setUserRequest)
        self.app.add_url_rule('/fetchTripRequestForTrip', methods=['GET'], view_func=self.travelEP.fetchTripRequestForTrip)
        self.app.add_url_rule('/registerResponseForTripRequest', methods=['POST'],
                              view_func=self.travelEP.registerRequestResponse)
        self.app.add_url_rule('/fetchUsersForTrip', methods=['GET'], view_func=self.travelEP.fetchUsersForTrip)
        self.app.add_url_rule('/deleteUser', methods=['GET'], view_func=self.travelEP.deleteUser)
        # Expense based EPS
        self.app.add_url_rule('/fetchExpensesForTrip', methods=['GET'], view_func=self.travelEP.fetchExpensesForATrip)
        self.app.add_url_rule('/addExpense', methods=['POST'], view_func=self.travelEP.addExpenseForTrip)
        self.app.add_url_rule('/editExpense', methods=['POST'], view_func=self.travelEP.editExpenseForTrip)
        self.app.add_url_rule('/deleteExpenses', methods=['GET'], view_func=self.travelEP.deleteExpenseForTrip)
        # Balance based EPS
        self.app.add_url_rule('/fetchBalances', methods=['GET'], view_func=self.travelEP.fetchBalancesForATrip)

    def run_app(self):
        self.logger.info("Starting Trip Split...")
        # self.app.run(host='0.0.0.0')
        self.app.run(debug=False, port=5500)


flaskappRunner = FlaskApp(__name__)
flask_app = flaskappRunner.app
#flaskappRunner.run_app()
