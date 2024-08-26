import logging


class Logger:
    def __init__(self, log_file=f"{__name__}.log"):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Create file handler which logs messages to a file
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)

        # Create formatter with the specified format
        formatter = logging.Formatter("%(asctime)s-%(levelname)s: %(message)s")
        fh.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(fh)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message, exc_info=True):
        self.logger.error(message, exc_info=exc_info)
