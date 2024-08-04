
import logging
import re

def is_regex(pattern: str):
    try:
        re.compile(pattern)
        return True
    except re.error:
        return False
    
class CustomFormatter(logging.Formatter):
    grey = "\x1b[30m"
    blue = "\x1b[36m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    COLORS = {
        logging.DEBUG: grey,
        logging.INFO: blue,
        logging.WARNING: yellow,
        logging.ERROR: red,
        logging.CRITICAL: bold_red
    }

    def format(self, record):
        log_fmt = f"{self.COLORS[record.levelno]}[%(asctime)s]: %(message)s {self.reset}"
        formatter = logging.Formatter(log_fmt, "%d.%m.%Y %H:%M:%S")
        return formatter.format(record)