import strenum
from config import RECORD_URL
from enum import auto
from typing import Annotated
from beartype.vale import IsInstance

class VideoPlatform(strenum.StrEnum):
    youtube = auto()
    vimeo = auto()
    bilibili = auto()
    douyin = auto()
    tiktok = auto()
    @staticmethod
    def check_is_valid_video_platform(it:str):
        try:
            VideoPlatform(it)
            return True
        except ValueError:
            return False

VideoPlatformType = Annotated[str, lambda it: VideoPlatform.check_is_valid_video_platform(it)]

class RecordEndpoint(strenum.StrEnum):
    query_history_view_count = "/query/history_view_count"
    query_current_view_count = "/query/current_view_count"
    query_video_url = "/query/video_url"
    query_videos = "/query/videos"
    register_video = "/register/video"

    submit_video_statistics = "/submit/video_statistics"

    @property
    def url(self):
        return f"{RECORD_URL}{self}"
