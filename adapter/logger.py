import logging
import os

logging.basicConfig(
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO
)

class LogFilter(logging.Filter):
    def filter(self, record):
        return os.getenv("DEBUG_DATA_FLOW") is not None

logger = logging.getLogger()
logger.addFilter(LogFilter())