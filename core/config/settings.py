import logging.config
from pathlib import Path
from selenium.webdriver import ChromeOptions

BASE_DIR = Path(__file__).resolve().parent.parent  # core directory
MAX_RETRIES: int = 5
MAX_AWAIT_TIME: int = 5
NSEINDIA_FILE_PATH = f"{BASE_DIR}/data/nseindia.csv"
ELONMUSK_FILE_PATH = f"{BASE_DIR}/data/elonmusk.log"

api_link: str = "https://www.nseindia.com/api/market-data-pre-open?key={}"

options = ChromeOptions()

# Нужно максимально убрать видимость автоматизации; иначе возникает ERR_HTTP2_PROTOCOL_ERROR
options.add_argument('--ignore-ssl-errors')
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--ignore-certificate-errors')
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-extensions")
options.add_argument('--disable-blink-features=AutomationControlled')

# Logging config
LOGGING = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "[%(levelname)s]: %(asctime)s - %(name)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "filename": ELONMUSK_FILE_PATH
        }
    },
    "loggers": {
        "streamLogger": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": "no"
        }
    }
}

logging.config.dictConfig(LOGGING)
stream_logger = logging.getLogger("streamLogger")
