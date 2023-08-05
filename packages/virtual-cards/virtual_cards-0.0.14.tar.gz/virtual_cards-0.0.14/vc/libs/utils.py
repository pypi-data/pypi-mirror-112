import logging
from logging.handlers import TimedRotatingFileHandler


def set_config(logger, filename: str = None):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.DEBUG)
    # FileHandler

    fh = logging.StreamHandler()
    if filename:
        fh = TimedRotatingFileHandler(filename, when="W0", backupCount=2)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
