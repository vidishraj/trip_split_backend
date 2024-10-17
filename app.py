from flask import Flask
from util.logger import Logger
from controllers import travelEP
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials


class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.logger = Logger().get_logger()
        CORS(self.app)
        # Init firebase
        self.logger.info("Setting up firebase admin creds")
        cred = credentials.Certificate("./serviceAccountKey.json")
        firebase_admin.initialize_app(cred)

        self.setup_routes()
        self.logger.info("Finished setting up routes...")

    def setup_routes(self):
        # Trip EPS
        self.app.add_url_rule('/createTrip', methods=['POST'], view_func=travelEP.createTrip)
        self.app.add_url_rule('/fetchTrips', methods=['GET'], view_func=travelEP.fetchTrips)
        # User based EPS
        self.app.add_url_rule('/createUser', methods=['POST'], view_func=travelEP.createUser)
        self.app.add_url_rule('/sendTripUserRequest', methods=['POST'], view_func=travelEP.setUserRequest)
        self.app.add_url_rule('/fetchTripRequestForTrip', methods=['GET'], view_func=travelEP.fetchTripRequestForTrip)
        self.app.add_url_rule('/registerResponseForTripRequest', methods=['POST'],
                              view_func=travelEP.registerRequestResponse)
        self.app.add_url_rule('/fetchUsersForTrip', methods=['GET'], view_func=travelEP.fetchUsersForTrip)
        self.app.add_url_rule('/deleteUser', methods=['GET'], view_func=travelEP.deleteUser)
        # Expense based EPS
        self.app.add_url_rule('/fetchExpensesForTrip', methods=['GET'], view_func=travelEP.fetchExpensesForATrip)
        self.app.add_url_rule('/addExpense', methods=['POST'], view_func=travelEP.addExpenseForTrip)
        self.app.add_url_rule('/editExpense', methods=['POST'], view_func=travelEP.editExpenseForTrip)
        self.app.add_url_rule('/deleteExpenses', methods=['GET'], view_func=travelEP.deleteExpenseForTrip)
        # Balance based EPS
        self.app.add_url_rule('/fetchBalances', methods=['GET'], view_func=travelEP.fetchBalancesForATrip)

    def run(self):
        self.logger.info("Starting Trip Split...")
        # self.app.run(host='0.0.0.0')
        self.app.run(debug=False, port=5000)


flaskappRunner = FlaskApp()
flask_app = flaskappRunner.app
flaskappRunner.run()
