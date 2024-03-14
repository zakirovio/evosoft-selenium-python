import logging.config
from decouple import Config, RepositoryEnv
from pathlib import Path
from selenium.webdriver import ChromeOptions

BASE_DIR = Path(__file__).resolve().parent.parent  # core directory
WRITE_TO = False
MAX_RETRIES: int = 5
MAX_AWAIT_TIME: int = 5
MAX_VERIFY_TIME: int = 60

# dotenv
config = Config(RepositoryEnv(f"{BASE_DIR}/.env"))

# Proxies config
PROXY = True

PROXY_HOST = "38.170.243.135"
PROXY_PORT = 9240
PROXY_USER = config("PROXY_USERNAME")
PROXY_PASS = config("PROXY_PASSWORD")

requests_proxies = {
    "https": f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}",
}

# nseindia app
api_link: str = "https://www.nseindia.com/api/market-data-pre-open?key={}"
NSEINDIA_FILE_PATH = f"{BASE_DIR}/data/nseindia.csv"

# elonmusk app
ELONMUSK_FILE_PATH = f"{BASE_DIR}/data/elonmusk.log"
T_USERNAME = config("TWITTER_USERNAME")
T_PASSWORD = config("TWITTER_PASSWORD")

# Chrome driver config
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
options.add_argument("--disable-popup-blocking")

# Logging config
LOGGING = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "[%(levelname)s]: %(asctime)s - %(message)s"
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
        },
        "fileLogger": {
            "level": "DEBUG",
            "handlers": ["file"],
            "propagate": "no"

        }
    }
}

# Loggers
logging.config.dictConfig(LOGGING)

stream_logger = logging.getLogger("streamLogger")
file_logger = logging.getLogger("fileLogger")
