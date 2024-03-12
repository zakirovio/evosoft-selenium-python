from apps.nseindia.scraper import main as nseindia
from config import settings
from sys import argv


util, command, param = argv

if __name__ == '__main__':
    assert util == "run.py"
    assert command == "start"

    if param == "nseindia":
        settings.stream_logger.info(msg="NSEINDIA APP IS STARTING")
        nseindia()
        settings.stream_logger.info(msg="NSEINDIA APP IS COMPLETED")
