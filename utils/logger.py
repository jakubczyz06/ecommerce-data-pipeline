# Imports
import logging
import sys
from utils.paths import LOGS_DIR



# Configuration of the logger
def get_logger(module: str) -> logging.Logger:
    logger = logging.getLogger(module)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    log_file = LOGS_DIR / f"{module}.log"

    file_handler = logging.FileHandler(
        log_file,
        mode = "a",
        encoding = "utf-8",
    )

    stream_handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt = "%Y-%m-%d %H:%M",
    )

    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger