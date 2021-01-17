from .config import config
import sys

_logger = config.logger


class LogColors:
    no_color = "\033[0m"
    red = "\033[91m"
    green = "\033[92m"
    cyan = "\033[96m"
    blue = "\033[94m"
    yellow = "\033[33m"
    bold = "\u001b[1m"

    error = red
    header = bold
    removed = red
    added = green


class Logger:
    @staticmethod
    def error(message: str, exit: bool = False):
        """Logs a message and prints is at red

        Args:
            message (str): The message to log
            exit (bool): If the program should exit after printing the error
        """
        _logger.debug(f"{LogColors.error}{message}{LogColors.no_color}")
        if exit:
            sys.exit(1)

    @staticmethod
    def warning(message: str, color: str = LogColors.yellow):
        """Prints a warning message

        Args:
            message (str): The warning message
            color (LogColors): Optional log color. Defaults to LogColors.yellow.
        """
        if color == LogColors.no_color:
            _logger.warning(message)
        else:
            _logger.warning(f"{color}{message}{LogColors.no_color}")

    @staticmethod
    def info(message: str, color: str = LogColors.no_color):
        """Print an information message that always is shown

        Args:
            message (str): The message to log
            color (LogColors): Optional color of the message
        """
        if color == LogColors.no_color:
            _logger.info(message)
        else:
            _logger.info(f"{color}{message}{LogColors.no_color}")

    @staticmethod
    def verbose(message: str, color: str = LogColors.no_color):
        """Log message if verbose has been set to true

        Args:
            message (str): The message to log
            color (LogColors): Optional color of the message
        """
        if config.verbose:
            if color == LogColors.no_color:
                _logger.info(message)
            else:
                _logger.info(f"{color}{message}{LogColors.no_color}")

    @staticmethod
    def debug(message: str, color: str = LogColors.no_color):
        """A debug message if --debug has been set to true

        Args:
            message (str): The message to log
            color (LogColors): Optional color of the message
        """
        if config.debug:
            if color == LogColors.no_color:
                _logger.debug(message)
            else:
                _logger.debug(f"{color}{message}{LogColors.no_color}")