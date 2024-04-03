import os, sys
import beartype
from urllib.parse import urlparse, parse_qs

INVISIBLE_CHARS = ['\ufeff','\u200c','\u200d']

def remove_invisible_chars(text: str):
    for invisible_char in INVISIBLE_CHARS:
        text = text.replace(invisible_char, '')
    return text

@beartype.beartype
def ensure_dir(dir_path: str):
    if os.path.exists(dir_path) is False:
        os.mkdir(dir_path)
    elif not os.path.isdir(dir_path):
        raise Exception(f"Path '{dir_path}' exists but is not a directory")


def execute_commands(commands: list[str]):
    for index, command in enumerate(commands):
        print(f"Executing command {index + 1} of {len(commands)}: {command}")
        exit_code = os.system(command)
        if exit_code != 0:
            raise Exception(f"Error executing command [{index + 1}]: {command}")


# to make sure our time is right, you must sync time before running it.
# this could be platform dependent.
def sync_time():
    if sys.platform == "win32":
        commands = ["w32tm /resync"]
    elif sys.platform == "darwin":
        commands = [
            "sudo systemsetup -setnetworktimeserver time.apple.com",
            "sudo systemsetup -setusingnetworktime on",
        ]
    elif sys.platform == "linux":
        commands = ["sudo timedatectl set-ntp true"]
    else:
        raise Exception("Unrecognized platform: {0}".format(sys.platform))
    execute_commands(commands)


# @beartype.beartype
# def split_url_components(url: str, spliter: str):
#     spliter = spliter.strip()
#     assert len(spliter) == 1, "Splitter must be a single character"

#     if spliter not in url:
#         url += spliter
#     else:
#         spliter_count = url.count(spliter)
#         assert (
#             spliter_count == 1
#         ), f"url can only contain one single spliter at most, but '{spliter}' is given as spliter and '{url}' is given as url, (count: {spliter_count})"

#     front, end = url.split(spliter)
#     return front, end


@beartype.beartype
def parse_url_with_anchor_and_query_params(url: str):
    parsed_url = urlparse(url)
    anchor = parsed_url.fragment
    query_params = parse_qs(parsed_url.query)
    # url, anchor = split_url_components(url,"#")
    # url, query = split_url_components(url,"?")
    return url, anchor, query_params

@beartype.beartype
def parse_url_with_query_params(url: str):
    url, _, query_params = parse_url_with_anchor_and_query_params(url)
    return url, query_params
@beartype.beartype
def strip_url(url:str):
    url, _, _ = parse_url_with_anchor_and_query_params(url)
    return url