from schema import VideoStatistics
import os
from dirutil import ensure_dir
import beartype
import datetime

# call the retention mechanism when opening database context
# import schedule # use double schedulers to collect tsdb paths, register/cancel retention tasks and perform retention
import tinyflux
from context import contextify_db_factory_with_lock
from config import TSDB_DIR, TSDB_RETENTION_HOURS, TIMEZONE
from util import *
from enums import VideoPlatform

# to rebuild the retention policy:
# https://tinyflux.readthedocs.io/en/latest/removing-data.html


@contextify_db_factory_with_lock
def tsdb_context(db_path: str) -> tinyflux.TinyFlux:
    ret = tinyflux.TinyFlux(db_path)
    perform_retention(ret, TSDB_RETENTION_HOURS)
    return ret


@beartype.beartype
def get_tsdb_path_from_vid_and_platform(vid: str, platform: VideoPlatform):
    platform_dir = os.path.join(TSDB_DIR, platform)
    ensure_dir(platform_dir)

    tsdb_path = os.path.join(platform_dir, f"{vid}.csv")
    return tsdb_path


@beartype.beartype
def write_video_statistics_to_tsdb(video_statistics: VideoStatistics):
    # 构建TSDB的写入语句
    # vid = get_vid_from_url_and_platform(video_statistics.url, video_statistics.platform)
    vid = video_statistics.vid
    url = get_url_from_vid_and_platform(vid, video_statistics.platform)
    tsdb_path = get_tsdb_path_from_vid_and_platform(
        video_statistics.vid, video_statistics.platform
    )

    with tsdb_context(tsdb_path) as tsdb:
        point = tinyflux.Point(
            measurement="video_statistics",
            time=datetime.datetime.now(TIMEZONE),
            tags={
                "platform": video_statistics.platform,
                "vid": vid,
                "url": url,
            },
            fields={"view_count": video_statistics.view_count},
        )
        tsdb.insert(point)
    return True  # marking success.


@beartype.beartype
def perform_retention(tsdb: tinyflux.TinyFlux, retention_period_in_hours: int):
    # 删除过期数据
    time_query = tinyflux.TimeQuery()
    t = datetime.datetime.now(TIMEZONE) - datetime.timedelta(
        hours=retention_period_in_hours
    )
    tsdb.remove(time_query < t)
    # you may close the database handle outside this function.


if os.environ.get("SYNC_TIME", None):
    sync_time()
