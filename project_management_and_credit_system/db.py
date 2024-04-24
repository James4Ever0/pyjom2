import tinydb
from config import VIDEODB_PATH
from context import contextify_db_factory_with_lock


@contextify_db_factory_with_lock
def tinydb_context(db_path: str):
    return tinydb.TinyDB(db_path)


def videodb_context() -> tinydb.TinyDB:
    return tinydb_context(VIDEODB_PATH)
