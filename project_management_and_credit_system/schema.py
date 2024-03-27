import pydantic
from typing import Literal, List
import datetime
from util import strip_url

__all__ = ["VideoRegisterData", "ViewStatisticsArgs"]


class VideoRegisterData(pydantic.BaseModel):
    project_path: str
    video_path: str
    platform: str
    url: str
    @pydantic.validator("url")
    def validate_url(self, url):
        if not url.startswith("http"):
            raise ValueError("URL must start with http")
        url = strip_url(url)
        return url

class ViewStatisticsArgs(pydantic.BaseModel):
    platform: str
    show: List[str]
    sort: Literal["view_count", "trend_index"] = "view_count"


class VideoStatistics(pydantic.BaseModel):
    platform: str
    view_count: int
    url: str
    vid: str
    timestamp: datetime.datetime
