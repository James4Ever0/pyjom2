import pydantic
from typing import Literal, List, Optional
import datetime

from util import strip_url
from util import enums

__all__ = ["VideoRegisterData", "ViewStatisticsArgs"]


class VideoPlatformInfo(pydantic.BaseModel):
    platform: enums.VideoPlatform


class UrlInfoOptional(pydantic.BaseModel):
    url: Optional[str]

    @pydantic.validator("url")
    def validate_url(cls, url):
        if url is None:
            return
        if not url.startswith("http"):
            raise ValueError("URL must start with http")
        url = strip_url(url)
        return url


class UrlInfo(UrlInfoOptional):
    url: str


class VideoWebLocation(VideoPlatformInfo, UrlInfo): ...


class VideoRegisterData(VideoWebLocation):
    project_path: Optional[str]
    video_path: Optional[str]


# TODO: calculate daily video view count change as trend index
class ViewStatisticsArgs(VideoPlatformInfo):
    show: List[str]
    sort: Literal["view_count", "trend_index"] = "view_count"


class VideoStatistics(VideoPlatformInfo):
    view_count: int
    vid: str


class VideoFullStatistics(VideoStatistics, UrlInfo):
    timestamp: datetime.datetime
