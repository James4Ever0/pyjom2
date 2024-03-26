from schema import VideoStatistics
import os
from util import ensure_dir
import beartype
import datetime
import schedule
import tinyflux
from context import contextify_db_with_lock
from config import TSDB_DIR, TSDB_RETENTION_HOURS, TIMEZONE
from util import sync_time, strip_query_params

# to rebuild the retention policy:
# https://tinyflux.readthedocs.io/en/latest/removing-data.html


@contextify_db_with_lock
def tsdb_context(db_path: str):
    ret = tinyflux.TinyFlux(db_path)
    return ret


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
def get_tsdb_path_from_vid_and_platform(vid:str, platform:str):
    platform_dir = os.path.join(TSDB_DIR,platform)
    ensure_dir(platform_dir)

    tsdb_path = os.path.join(platform_dir, f"{vid}.csv")
    return tsdb_path

@beartype.beartype
def write_video_statistics_to_tsdb(video_statistics: VideoStatistics):
    # 构建TSDB的写入语句
    vid = get_vid_from_url_and_platform(video_statistics.url, video_statistics.platform)
    tsdb_path = get_tsdb_path_from_vid_and_platform(vid, video_statistics.platform)

    with tsdb_context(tsdb_path) as tsdb:
        point = tinyflux.Point(
            measurement="video_statistics",
            time=datetime.datetime.now(TIMEZONE),
            tags={
                "platform": video_statistics.platform,
                "vid": vid,
                "url": video_statistics.url,
            },
            fields={"view_count": video_statistics.view_count},
        )
        tsdb.insert(point)

@beartype.beartype
def perform_retention(tsdb:tinyflux.TinyFlux, retention_period_in_hours:int):
    # 删除过期数据
    time_query = tinyflux.TimeQuery()
    t = datetime.datetime.now(TIMEZONE) - datetime.timedelta(hours=retention_period_in_hours)
    tsdb.remove(time_query < t)
    # you may close the database handle outside this function.

sync_time()