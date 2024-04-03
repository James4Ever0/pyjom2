# you need to be careful about the user agent, for bilibili.
# you need real user agent.
import fake_useragent

DEFAULT_USER_AGENT = {
    # "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0",
    "user-agent": fake_useragent.UserAgent(os='linux').firefox
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    # "accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
}
