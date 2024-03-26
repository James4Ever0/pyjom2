import beartype
import os
import filelock

@beartype.beartype
def get_lock_path_from_path(path:str):
    dirpath, basepath = os.path.split(path)
    lock_path = os.path.join(dirpath, f".{basepath}.lock")
    return lock_path

@beartype.beartype
def get_filelock_from_path(path:str):
    lock_path = get_lock_path_from_path(path)
    return filelock.FileLock(lock_path)