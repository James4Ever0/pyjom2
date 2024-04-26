# create some daily jobs for us.

# fetch for existing video ids -> check viewcounts -> submit to tsdb

# as for those wondering how to get the video ids, there are plenty good videos posted daily, and they are just a few. it is something to be researched later on.

# if you import many videos to this database, you would inevitably remove most of them. so let's not worry about that and focus on something rather 'trivial'.

# for better orchestration, you would like to use other alternatives

# ref:
# https://github.com/PrefectHQ/prefect/issues?q=retention

import checkout
# import db, tsdb
import enums, schema
import schedule
import requests
from typing import Callable, List
import time
from config import VIDEO_CHECKOUT_TASK_INTERVAL, TASK_MAIN_LOOP_INTERVAL
import util


def register_tasks(tasks: List[Callable[[], None]]):
    for it in tasks:
        schedule.every(VIDEO_CHECKOUT_TASK_INTERVAL).minutes.run(it)


def run_pending_tasks():
    while True:
        schedule.run_pending()
        time.sleep(TASK_MAIN_LOOP_INTERVAL)


def main():
    tasks = [lambda: video_checkout_task(enums.VideoPlatform.bilibili)]
    register_tasks(tasks)
    run_pending_tasks()


def checkout_video_viewcount_and_submit_by_vid(vid: int, platform: enums.VideoPlatform):
    view_count = checkout.viewcount_getters[platform](vid)
    # now add this measurement to tsdb.
    video_statistics = schema.VideoStatistics(
        platform=platform, view_count=view_count, vid=vid
    )
    submit_response = requests.post(
        enums.RecordEndpoint.submit_video_statistics.url,
        json=video_statistics.dict(),
    )  # assert success.
    submit_success = submit_response.json()["success"]


def video_checkout_task(platform: enums.VideoPlatform):
    all_video_ids = []
    response = requests.get(
        enums.RecordEndpoint.query_videos.url,
        params=dict(platform=platform, type="random", limit=None),
    )

    all_video_ids = response.json()["data"]
    print(f"Checking out {len(all_video_ids)} videos")
    for vid in all_video_ids:
        checkout_video_viewcount_and_submit_by_vid(vid, platform)


def bilibili_add_all_videos_of_user_to_db(uid: str):
    vids = checkout.user_video_getters[enums.VideoPlatform.bilibili](uid)
    bilibili_add_videos_to_db_by_vids(vids)


def bilibili_add_videos_to_db_by_vids(vids: List[str]):
    urls = []
    for it in vids:
        url = util.get_url_from_vid_and_platform(it, enums.VideoPlatform.bilibili)
        urls.append(url)
    add_videos_to_db_by_urls(urls)


def add_videos_to_db_by_urls(urls: List[str], platform: enums.VideoPlatform):
    for it in urls:
        reply = requests.post(
            enums.RecordEndpoint.register_video.url,
            data=schema.VideoRegisterData(url=it, platform=platform),
        )  # TODO: log unsuccessful tasks


if __name__ == "__main__":
    # main() # mainloop
    video_checkout_task(enums.VideoPlatform.bilibili)  # only run once
