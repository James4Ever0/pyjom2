# fetch viewcount data from internet.
from enums import RecordEndpoint, VideoPlatform
import requests
from typing import Union, Coroutine
import beartype
import time
from config import CHECKOUT_INTERVAL
import bilibili_api
import rich
import random
import wbi
from constants import DEFAULT_UI


async def bilibili_user_get_videos(
    self,
    tid: int = 0,
    pn: int = 1,
    ps: int = 30,
    keyword: str = "",
    order: bilibili_api.user.VideoOrder = bilibili_api.user.VideoOrder.PUBDATE,
) -> dict:
    api = bilibili_api.user.API["info"]["video"]
    # api['wbi']=True
    # api['no_csrf']=True
    dm_rand = "ABCDEFGHIJK"

    params = {
        "mid": self._User__uid,
        "ps": ps,
        "tid": tid,
        "pn": pn,
        "platform": "web",
        "keyword": keyword,
        "web_location": "1550101",
        "order": order.value,
        # -352 https://github.com/Nemo2011/bilibili-api/issues/595
        "order_avoided": "true",
        # "wts": str(int(time.time())),
        # "w_rid": "57dd8639eb4e4ebbde126f049fdf2156",
    }
    params.update(
        {
            "dm_img_list": "[]",  # 鼠标/键盘操作记录
            "dm_img_str": "".join(random.sample(dm_rand, 2)),
            "dm_cover_img_str": "".join(random.sample(dm_rand, 2)),
            "dm_img_inter": '{"ds":[],"wh":[0,0,0],"of":[0,0,0]}',
            # "dm_img_list": '[{"x":2423,"y":2648,"z":0,"timestamp":6,"k":102,"type":0},{"x":2532,"y":2761,"z":28,"timestamp":93,"k":126,"type":0},{"x":2824,"y":3050,"z":214,"timestamp":225,"k":83,"type":0}]',
            # "dm_img_str": "V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ",
            # "dm_cover_img_str": "QU5HTEUgKE5WSURJQSwgTlZJRElBIEdlRm9yY2UgR1RYIDEwNjAgNkdCICgweDAwMDAxQjgzKSBEaXJlY3QzRDExIHZzXzVfMCBwc181XzAsIEQzRDExKUdvb2dsZSBJbmMuIChOVklESU",
            # "dm_img_inter": '{"ds":[{"t":0,"c":"","p":[12,4,4],"s":[34,3852,412]}],"wh":[3315,2605,75],"of":[171,342,171]}',
        }
    )
    params = wbi.modify_params(params)
    headers = DEFAULT_UI.copy()
    # headers.update(
    #     {
    #         "origin": "https://space.bilibili.com",
    #         "referer": f"https://space.bilibili.com/{self._User__uid}/video?tid=0&pn={pn}&keyword=&order=pubdate",
    #         "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    #         "sec-ch-ua-mobile": "?0",
    #         "sec-ch-ua-platform": '"Windows"',
    #         "sec-fetch-dest": "empty",
    #         "sec-fetch-mode": "cors",
    #         "sec-fetch-site": "same-site",
    #     }
    # )
    return (
        await bilibili_api.user.Api(
            **api,
            credential=self.credential,
            headers=headers,
        )
        .update_params(**params)
        .result
    )


bilibili_api.user.User.get_videos = bilibili_user_get_videos


def sync_and_sleep(coroutine: Coroutine):
    ret = bilibili_api.sync(coroutine)
    time.sleep(CHECKOUT_INTERVAL)
    return ret


@beartype.beartype
def bilibili_get_viewcount(vid: str):
    v = bilibili_api.video.Video(vid)
    info = sync_and_sleep(v.get_info())
    # rich.print(info)
    viewcount = info["stat"]["view"]
    # let's forget about the publish date. it is only valuable to bilibili internal algorithms.
    # pubdate = info['pubdate']
    return viewcount


# need cookies
@beartype.beartype
def bilibili_get_all_videos_from_uid(uid: Union[str, int]):
    uid = int(uid)
    # cred = bilibili_api.Credential.from_cookies(cookies)

    user = bilibili_api.user.User(uid)
    page_num = 1
    ret = {}
    while True:
        rich.print(f"page #{page_num}")
        videos = sync_and_sleep(
            user.get_videos(pn=page_num)
        )  # will disconnect on second request.
        ret.update(videos)
        rich.print(videos)
        if videos:
            page_num += 1
        else:
            # no more videos.
            break
    return ret


viewcount_getters = {VideoPlatform.bilibili: bilibili_get_viewcount}
if __name__ == "__main__":
    # ensure singleton, then checkout.
    # print(bilibili_get_viewcount("BV1GK4y1V7HP"))
    uids = [85300402]
    for uid in uids:
        bilibili_get_all_videos_from_uid(uid)
