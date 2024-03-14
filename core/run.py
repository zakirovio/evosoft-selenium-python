from apps.elonmusk.scraper import main as elonmusk
from apps.nseindia.scraper import main as nseindia
from config import settings
from sys import argv


util, param = argv

if __name__ == '__main__':
    assert util == "run.py", settings.stream_logger.error(msg="UNKNOWN UTILITY")

    if param == "nseindia":
        settings.stream_logger.info(msg="NSEINDIA APP IS STARTING")
        nseindia()
        settings.stream_logger.info(msg="NSEINDIA APP IS COMPLETED")
    elif param == "elonmusk":
        settings.stream_logger.info(msg="ELONMUSK APP IS STARTING")
        elonmusk()
        settings.stream_logger.info(msg="ELONMUSK APP IS COMPLETED")
    else:
        settings.stream_logger.error(msg="UNKNOWN PARAMETER")
