from functools import reduce
from hashlib import md5
import urllib.parse
import time
import requests

from constants import DEFAULT_USER_AGENT

mixinKeyEncTab = [
    46,
    47,
    18,
    2,
    53,
    8,
    23,
    32,
    15,
    50,
    10,
    31,
    58,
    3,
    45,
    35,
    27,
    43,
    5,
    49,
    33,
    9,
    42,
    19,
    29,
    28,
    14,
    39,
    12,
    38,
    41,
    13,
    37,
    48,
    7,
    16,
    24,
    55,
    40,
    61,
    26,
    17,
    0,
    1,
    60,
    51,
    30,
    4,
    22,
    25,
    54,
    21,
    56,
    59,
    6,
    63,
    57,
    62,
    11,
    36,
    20,
    34,
    44,
    52,
]


def getMixinKey(orig: str):
    "对 imgKey 和 subKey 进行字符顺序打乱编码"
    return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, "")[:32]


def encWbi(params: dict, img_key: str, sub_key: str):
    "为请求参数进行 wbi 签名"
    mixin_key = getMixinKey(img_key + sub_key)
    curr_time = round(time.time())
    params["wts"] = curr_time  # 添加 wts 字段
    params["web_location"] = "1550101"
    params = dict(sorted(params.items()))  # 按照 key 重排参数
    # 过滤 value 中的 "!'()*" 字符
    params = {
        k: "".join(filter(lambda chr: chr not in "!'()*", str(v)))
        for k, v in params.items()
    }

    query = urllib.parse.urlencode(params)  # 序列化参数
    # print(params)
    # print()
    # print(query)

    # breakpoint()
    wbi_sign = md5((query + mixin_key).encode()).hexdigest()  # 计算 w_rid
    params["w_rid"] = wbi_sign
    return params


def getWbiKeys(headers=DEFAULT_USER_AGENT):  # -> tuple[str, str]
    "获取最新的 img_key 和 sub_key"
    resp = requests.get("https://api.bilibili.com/x/web-interface/nav", headers=headers)
    resp.raise_for_status()
    json_content = resp.json()
    img_url: str = json_content["data"]["wbi_img"]["img_url"]
    sub_url: str = json_content["data"]["wbi_img"]["sub_url"]
    img_key = img_url.rsplit("/", 1)[1].split(".")[0]
    sub_key = sub_url.rsplit("/", 1)[1].split(".")[0]
    return img_key, sub_key


def modify_params(params: dict):
    img_key, sub_key = getWbiKeys()
    return encWbi(params, img_key, sub_key)


def get_query(params: dict):
    params = modify_params(params)
    return urllib.parse.urlencode(params)


if __name__ == "__main__":
    # img_key, sub_key = getWbiKeys()

    # signed_params = encWbi(
    #     params={
    #         'foo': '114',
    #         'bar': '514',
    #         'baz': 1919810
    #     },
    #     img_key=img_key,
    #     sub_key=sub_key
    # )
    # query = urllib.parse.urlencode(signed_params)
    # print(signed_params)
    # print(query)

    img_key, sub_key = getWbiKeys()
    mixin_key = getMixinKey(img_key + sub_key)
    print(mixin_key)
    query = "dm_cover_img_str=QU5HTEUgKE5WSURJQSwgTlZJRElBIEdlRm9yY2UgR1RYIDEwNjAgNkdCICgweDAwMDAxQjgzKSBEaXJlY3QzRDExIHZzXzVfMCBwc181XzAsIEQzRDExKUdvb2dsZSBJbmMuIChOVklESU&dm_img_inter=%7B%22ds%22%3A%5B%5D%2C%22wh%22%3A%5B1931%2C-73%2C57%5D%2C%22of%22%3A%5B326%2C652%2C326%5D%7D&dm_img_list=%5B%5D&dm_img_str=V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ&mid=1946720965&platform=web&token=&web_location=1550101&wts=1711569552"
    # valid found on breakpoint
    # dm_cover_img_str=QU5HTEUgKE5WSURJQSwgTlZJRElBIEdlRm9yY2UgR1RYIDEwNjAgNkdCICgweDAwMDAxQjgzKSBEaXJlY3QzRDExIHZzXzVfMCBwc181XzAsIEQzRDExKUdvb2dsZSBJbmMuIChOVklESU&dm_img_inter=%7B%22ds%22%3A%5B%7B%22t%22%3A2%2C%22c%22%3A%22Y2xlYXJmaXggZy1zZWFyY2ggc2VhcmNoLWNvbnRhaW5lcg%22%2C%22p%22%3A%5B1305%2C13%2C710%5D%2C%22s%22%3A%5B424%2C886%2C1264%5D%7D%2C%7B%22t%22%3A2%2C%22c%22%3A%22d3JhcHBlcg%22%2C%22p%22%3A%5B918%2C90%2C1386%5D%2C%22s%22%3A%5B331%2C4310%2C3714%5D%7D%5D%2C%22wh%22%3A%5B2195%2C205%2C107%5D%2C%22of%22%3A%5B348%2C696%2C348%5D%7D&dm_img_list=%5B%5D&dm_img_str=V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ&keyword=&mid=1946720965&order=pubdate&order_avoided=true&platform=web&pn=4&ps=30&tid=0&web_location=1550101&wts=1711576569
    # valid keys:
    # dm_cover_img_str,dm_img_inter,dm_img_list,dm_img_str,keyword,mid,order,order_avoided,platform,pn,ps,tid,web_location,wts
    wbi_sign = md5((query + mixin_key).encode()).hexdigest()
    print(wbi_sign)
