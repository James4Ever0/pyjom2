# fetch viewcount data from internet.
from enums import RecordEndpoint, VideoPlatform

import bilibili

viewcount_getters = {VideoPlatform.bilibili: bilibili.bilibili_get_viewcount}
user_video_getters = {VideoPlatform.bilibili: bilibili.bilibili_get_all_videos_from_uid}

if __name__ == "__main__":
    # ensure singleton, then checkout.
    # print(bilibili_get_viewcount("BV1GK4y1V7HP"))
    uids = [
        85300402,
        # i guess you add these invisible chars yourself.
        # 1946720965,
    ]
    for uid in uids:
        bilibili.bilibili_get_all_videos_from_uid(uid)
    # ...
