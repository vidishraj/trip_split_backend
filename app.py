from flask import Flask
from util.logger import Logger
from controllers import travelEP
from flask_cors import CORS


class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.logger = Logger().get_logger()

    def setup_routes(self):
        self.app.add_url_rule('/createTrip', methods=['POST'], view_func=travelEP.createTrip)
        self.app.add_url_rule('/fetchTrips', methods=['GET'], view_func=travelEP.fetchTrips)
        self.app.add_url_rule('/createUser', methods=['POST'], view_func=travelEP.addUserToTrip)
        self.app.add_url_rule('/fetchUsersForTrip', methods=['GET'], view_func=travelEP.fetchUsersForTrip)
        self.app.add_url_rule('/deleteUser', methods=['GET'], view_func=travelEP.deleteUser)
        self.app.add_url_rule('/fetchExpensesForTrip', methods=['GET'], view_func=travelEP.fetchExpensesForATrip)
        self.app.add_url_rule('/addExpense', methods=['POST'], view_func=travelEP.addExpenseForTrip)
        self.app.add_url_rule('/editExpense', methods=['POST'], view_func=travelEP.editExpenseForTrip)
        self.app.add_url_rule('/deleteExpenses', methods=['GET'], view_func=travelEP.deleteExpenseForTrip)
        self.app.add_url_rule('/fetchBalances', methods=['GET'], view_func=travelEP.fetchBalancesForATrip)

    def run(self):
        self.setup_routes()
        self.logger.info("Starting Trip Split...")
        CORS(self.app)
        self.app.run(debug=False, port=5000)


flask_app = FlaskApp()
flask_app.run()
