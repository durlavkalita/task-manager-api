import logging
from loguru import logger
import sys
import os

# Log file path
LOG_FILE = "logs/app.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Remove default handlers to avoid duplicate logs
logger.remove()

# Log format
LOG_FORMAT = "{time} | {level} | {message}"

# Add console logger
logger.add(sys.stdout, format=LOG_FORMAT, level="INFO")

# Add file logger
logger.add(LOG_FILE, format=LOG_FORMAT, level="INFO", rotation="10MB", compression="zip")

# Standard logging setup for dependencies
logging.basicConfig(level=logging.INFO)
logging.getLogger("uvicorn.access").handlers = [logging.StreamHandler(sys.stdout)]
