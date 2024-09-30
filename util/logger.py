import logging


class Logger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Console handler for logging
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # Formatter for the logs
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        # Add handler to the logger
        self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger
