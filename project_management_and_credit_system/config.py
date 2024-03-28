import os
from util import ensure_dir
import pytz

SCRIPT_BASEDIR = os.path.dirname(__file__)

HOST_ADDRESS = "localhost"
RECORD_PORT = 8042
RECORD_URL = f"http://{HOST_ADDRESS}:{RECORD_PORT}"


DATA_DIR =  os.path.join(SCRIPT_BASEDIR, "data")
ensure_dir(DATA_DIR)

DB_DIR = os.path.join(DATA_DIR, "db")
ensure_dir(DB_DIR)

VIDEODB_PATH = os.path.join(DB_DIR, "video_db.json")

TSDB_DIR = os.path.join(DATA_DIR, "tsdb")
ensure_dir(TSDB_DIR)

TSDB_RETENTION_HOURS = 1024

TIMEZONE_STR = "Asia/Shanghai"
TIMEZONE = pytz.timezone(TIMEZONE_STR)

SYNC_SLEEP_INTERVAL = 2
CHECKOUT_INTERVAL = 20 # do not lower this parameter unless you have cracked bilibili algorithm, or use browser request instead.

COOKIE_BROWSER = "firefox"

