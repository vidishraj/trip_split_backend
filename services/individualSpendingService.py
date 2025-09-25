from dbHandlers.individualSpendingHandler import IndividualSpendingHandler
from util.logger import Logger

logging = Logger().get_logger()


class IndividualSpendingService:
    def __init__(self, handler: IndividualSpendingHandler):
        self.handler = handler

    def fetchIndividualSpending(self, tripId):
        """
        Get individual spending breakdown for a trip.
        Shows how much each person actually spent (paid out of pocket).
        """
        try:
            result = self.handler.fetchIndividualSpending(tripId)
            logging.info(f"Retrieved individual spending for trip {tripId}")
            return result
        except Exception as e:
            logging.error(f"Error fetching individual spending for trip {tripId}: {e}")
            raise e