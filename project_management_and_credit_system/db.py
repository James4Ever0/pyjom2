import tinydb
from config import VIDEODB_PATH
from context import contextify_with_lockpath

@contextify_with_lockpath
def tinydb_context(db_path: str):
    return tinydb.TinyDB(db_path)

def videodb_context():
  return tinydb_context(VIDEODB_PATH)