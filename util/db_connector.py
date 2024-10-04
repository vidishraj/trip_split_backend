from mysql.connector import pooling, Error
from util.logger import Logger  # Import the existing logger


class DBConnector:
    def __init__(self, host, user, password, pool_name="mypool", pool_size=5):
        self.host = host
        self.user = user
        self.password = password
        self.pool_name = pool_name
        self.pool_size = pool_size
        self.connection_pool = None
        self.logger = Logger().get_logger()  # Use the shared logger

        self._create_connection_pool()

    def _create_connection_pool(self):
        try:
            self.connection_pool = pooling.MySQLConnectionPool(
                pool_name=self.pool_name,
                pool_size=self.pool_size,
                host=self.host,
                user=self.user,
                password=self.password
            )
            self.logger.info(f"Connection pool '{self.pool_name}' created with {self.pool_size} connections.")
        except Error as e:
            self.logger.error(f"Error creating connection pool: {e}")

    def get_connection(self):
        try:
            connection = self.connection_pool.get_connection()
            self.logger.debug("Connection obtained from pool.")
            return connection
        except Error as e:
            self.logger.error(f"Error getting connection from pool: {e}")
            return None

    def execute_query(self, query, params=None):
        connection = self.get_connection()
        cursor = None
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, params)
                result = cursor.fetchall()
                connection.commit()
                self.logger.debug(f"Query executed: {query}")
                return result
            except Error as e:
                self.logger.error(f"Error executing query: {e}")
                return None
            finally:
                cursor.close()
                connection.close()
                self.logger.debug("Connection returned to pool.")
        else:
            self.logger.error("Failed to execute query: Connection is not available.")
            return None

    def close_pool(self):
        try:
            self.connection_pool.close()
            self.logger.info("Connection pool closed.")
        except Error as e:
            self.logger.error(f"Error closing connection pool: {e}")


db_connector = DBConnector(
    host="",
    user="",
    password="",
    pool_size=10
)
