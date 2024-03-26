import strenum
from config import RECORD_URL


class RecordEndpoint(strenum.StrEnum):
    query_history_view_count = "/query/history_view_count"
    query_current_view_count = "/query/current_view_count"
    query_video_url = "/query/video_url"
    query_videos = "/query/videos"
    register_video = "/register/video"

    @property
    def url(self):
        return f"{RECORD_URL}{self}"
