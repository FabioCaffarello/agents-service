import os
from logger.log import setup_logging


LOG_VEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
log = setup_logging(__file__, log_level=LOG_VEVEL)


def main():
    log.info("Running agents-service!")
