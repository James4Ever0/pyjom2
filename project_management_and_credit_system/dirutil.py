import beartype, os


@beartype.beartype
def ensure_dir(dir_path: str):
    if os.path.exists(dir_path) is False:
        os.mkdir(dir_path)
    elif not os.path.isdir(dir_path):
        raise Exception(f"Path '{dir_path}' exists but is not a directory")
