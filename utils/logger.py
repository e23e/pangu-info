import logging
import os





LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

def get_logger():
    format = "%(asctime)s - %(levelname)s - %(filename)s - %(message)s"
    logging.basicConfig(format=format)
    logger = logging.getLogger("Pangu Info")
    logger.setLevel(LOG_LEVEL)
    return logger
