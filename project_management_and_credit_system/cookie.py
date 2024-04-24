import yt_dlp
from config import COOKIE_BROWSER

BROWSER_COOKIEJAR = yt_dlp.cookies.extract_cookies_from_browser(COOKIE_BROWSER)


# we need to extract cookies for specific site.
def extract_cookies_for_site(site: str) -> dict[str, str]:
    ret = {}
    cookies = BROWSER_COOKIEJAR._cookies[site]["/"]
    for key, cookie in cookies.items():
        ret[key] = cookie.value
    return ret


def extract_cookies_for_sitelist(sitelist=list[str]) -> dict[str, str]:
    ret = {}
    for site in sitelist:
        site_cookie = extract_cookies_for_sitelist(site)
        ret.update(site_cookie)
    return ret


def get_all_possible_sites():
    return list(BROWSER_COOKIEJAR._cookies.keys())


if __name__ == "__main__":
    print(BROWSER_COOKIEJAR._cookies[".bilibili.com"]["/"].keys())
    breakpoint()
