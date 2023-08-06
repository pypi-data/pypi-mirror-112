import logging
from logging.handlers import RotatingFileHandler


def create_logger(path: str, level: int = logging.INFO) -> logging.Logger:
    """
    Creates a logger for a given file path
    Note: `path` should be `__file__` in most cases

    Args:
        path (str): the path of the file (common use is `__file__`)
        level (int): the level of message to use in the logger (see
            logging for constants)

    Returns:
        logging.Logger: The logger created for the given file
    """
    logger = logging.getLogger(path)
    log_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(filename)s:%(funcName)s(%(lineno)d)]: %(message)s"
    )

    my_handler = RotatingFileHandler(
        f"{path}.log",
        mode="a",
        maxBytes=5 * 1024 * 1024,
        backupCount=2,
        encoding=None,
        delay=0,
    )
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(level)

    logger.setLevel(level)
    logger.addHandler(my_handler)

    return logger
