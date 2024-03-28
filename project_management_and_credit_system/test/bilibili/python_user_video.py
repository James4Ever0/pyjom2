import requests

url = "https://api.bilibili.com/x/space/wbi/arc/search"
params = {
    "dm_cover_img_str": "CE",
    "dm_img_inter": '{"ds":[],"wh":[0,0,0],"of":[0,0,0]}',
    "dm_img_list": "[]",
    "dm_img_str": "JH",
    "keyword": "",
    "mid": "85300402",
    "order": "pubdate",
    "order_avoided": "true",
    "platform": "web",
    "pn": "1",
    "ps": "30",
    "tid": "0",
    "web_location": "1550101",
    "wts": "1711632784",
    "w_rid": "62687906147f3e4777403d8c7247136f",
}
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}
ret = requests.get(url, params=params, headers=headers)
print(ret.json())