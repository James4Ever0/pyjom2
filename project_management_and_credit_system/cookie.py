import yt_dlp
from config import COOKIE_BROWSER

cookies = yt_dlp.cookies.extract_cookies_from_browser(COOKIE_BROWSER)
print(cookies._cookies['.bilibili.com']['/'].keys())
breakpoint()