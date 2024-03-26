import contextlib
import beartype
from lock import get_filelock_from_path

def contextify_db_with_lock(func):
    @contextlib.contextmanager
    @beartype.beartype
    def context_func(db_path:str):
        with get_filelock_from_path(db_path):
            yield func(db_path)
    return context_func