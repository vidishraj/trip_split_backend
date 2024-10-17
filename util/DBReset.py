import mysql.connector
from util.db_connector import db_connector
from util.logger import Logger

logging = Logger().get_logger()


class DBReset:
    _dbConnection: mysql.connector.connection.MySQLConnection | None
    _tryCount: int = 0

    def __init__(self):
        self._dbConnection = None
        self._tryCount = 0
        self.max_retries = 2

    def checkDbConnection(self):
        try:
            if self._dbConnection.is_connected():
                logging.info("Connected to db")
                return True
            else:
                logging.error("Connection was dropped, new connection retrieved")
                self._dbConnection = db_connector.get_connection()
                # Will manage connection if required in the future
                return False
        except Exception as ex:
            logging.error(f"Error while checking db connection status {ex}")
            self._dbConnection = db_connector.get_connection()
            return False
