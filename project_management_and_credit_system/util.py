import os,sys
import beartype

@beartype.beartype
def ensure_dir(dir_path:str):
    if os.path.exists(dir_path) is False:
        os.mkdir(dir_path)
    elif not os.path.isdir(dir_path):
        raise Exception(f"Path '{dir_path}' exists but is not a directory")


def execute_commands(commands:list[str]):
    for index, command in enumerate(commands):
        print(f"Executing command {index + 1} of {len(commands)}: {command}")
        exit_code = os.system(command)
        if exit_code != 0:
            raise Exception(f"Error executing command [{index + 1}]: {command}")

# to make sure our time is right, you must sync time before running it.
# this could be platform dependent.
def sync_time():
    if sys.platform == "win32":
        commands = ['w32tm /resync']
    elif sys.platform == "darwin":
        commands = ['sudo systemsetup -setnetworktimeserver time.apple.com', 'sudo systemsetup -setusingnetworktime on']
    elif sys.platform == "linux":
        commands = ['sudo timedatectl set-ntp true']
    else:
        raise Exception("Unrecognized platform: {0}".format(sys.platform))
    execute_commands(commands)


@beartype.beartype
def strip_query_params(url: str):
    url = url.split("?")[0]
    url = url.split("#")[0]
    return url