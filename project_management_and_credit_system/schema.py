import pydantic
from typing import Literal, List
import datetime


__all__ = ["VideoRegisterData", "ViewStatisticsArgs"]


class VideoRegisterData(pydantic.BaseModel):
    project_path: str
    video_path: str
    platform: str
    url: str


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
