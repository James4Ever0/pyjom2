# this shall be a strong proof that bilibili is using tls fingerprinting.

curl -o python_user_video.json 'https://api.bilibili.com/x/space/wbi/arc/search?dm_cover_img_str=CE&dm_img_inter=%7B%22ds%22%3A%5B%5D%2C%22wh%22%3A%5B0%2C0%2C0%5D%2C%22of%22%3A%5B0%2C0%2C0%5D%7D&dm_img_list=%5B%5D&dm_img_str=JH&keyword=&mid=85300402&order=pubdate&order_avoided=true&platform=web&pn=1&ps=30&tid=0&web_location=1550101&wts=1711632784&w_rid=62687906147f3e4777403d8c7247136f' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36' #\