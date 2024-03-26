import os
from util import ensure_dir
import pytz

SCRIPT_BASEDIR = os.path.dirname(__file__)

HOST_ADDRESS = "localhost"
RECORD_PORT = 8042
RECORD_URL = f"http://{HOST_ADDRESS}:{RECORD_PORT}"


DB_DIR = os.path.join(SCRIPT_BASEDIR, "db")
ensure_dir(DB_DIR)

VIDEODB_PATH = os.path.join(DB_DIR, "video_db.json")

TSDB_DIR = os.path.join(SCRIPT_BASEDIR, "tsdb")
ensure_dir(TSDB_DIR)

TSDB_RETENTION_HOURS = 1024

TIMEZONE_STR = "Asia/Shanghai"
TIMEZONE = pytz.timezone(TIMEZONE_STR)
