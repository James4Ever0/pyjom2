import contextlib
import beartype
from lock import get_filelock_from_path
from typing import Callable, TypeVar  # ,cast

T = TypeVar("T")


def contextify_db_factory_with_lock(func: Callable[[], T]) -> Callable[[], T]:
    @contextlib.contextmanager
    @beartype.beartype
    def context_func(db_path: str):
        with get_filelock_from_path(db_path):
            with func(db_path) as db:
                yield db

    # context_func = cast(Callable[[], T], context_func)
    return context_func
