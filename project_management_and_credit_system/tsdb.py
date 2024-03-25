from schema import VideoStatistics
import os, sys
import beartype, pytz
import datetime
import tinyflux

# to rebuild the retention policy:
# https://tinyflux.readthedocs.io/en/latest/removing-data.html

shanghai = pytz.timezone("Asia/Shanghai")


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

def get_tinyflux(db_path: str):
    ret = tinyflux.TinyFlux(db_path)
    return ret


tsdb_dir = os.path.join(os.path.dirname(__file__), "tsdb")
ts_retention = 1024  # in hours, 42 days

if os.path.exists(tsdb_dir) is False:
    os.mkdir(tsdb_dir)


@beartype.beartype
def strip_query_params(url: str):
    url = url.split("?")[0]
    url = url.split("#")[0]
    return url


@beartype.beartype
def get_vid_from_url_and_platform(url: str, platform: str):
    url = strip_query_params(url)
    if platform == "youtube":
        return url.split("v=")[1]
    elif platform == "bilibili":
        return url.split("/")[-1]
    else:
        raise ValueError("Unsupported platform")


@beartype.beartype
def write_video_statistics_to_tsdb(video_statistics: VideoStatistics):
    # 构建TSDB的写入语句
    vid = get_vid_from_url_and_platform(video_statistics.url, video_statistics.platform)
    platform_dir = os.path.join(tsdb_dir, video_statistics.platform)
    db_path = os.path.join(platform_dir, f"{vid}.csv")

    tsdb = get_tinyflux(db_path)
    point = tinyflux.Point(
        measurement="video_statistics",
        time=datetime.datetime.now(shanghai),
        tags={
            "platform": video_statistics.platform,
            "vid": vid,
            "url": video_statistics.url,
        },
        fields={"view_count": video_statistics.view_count},
    )
    tsdb.insert(point)
