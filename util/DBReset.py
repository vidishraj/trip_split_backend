import mysql.connector
from util.db_connector import db_connector

class DBReset:
    _dbConnection: mysql.connector.connection.MySQLConnection
    _tryCount: int = 0

    def __init__(self):
        self._dbConnection = None
        self._tryCount = 0
        self.max_retries = 2

    def checkDbConnection(self):
        try:
            if self._dbConnection.is_connected():
                return True
            else:
                self._dbConnection= db_connector.get_connection()
                # Will manage connection if required in the future
                return False
        except:
            self._dbConnection= db_connector.get_connection()
            return False
