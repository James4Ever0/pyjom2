# syntax:

# pyjom register_video --project_root jianying --video x.mp4 --project_name x --hosted_platform douyin --hosted_url https://...

# pyjom project_root_alias --project_root ... --alias jianying

# pyjom view_statistics --hosted_platform douyin --show_columns project_root,project_name,hosted_platform

# monitor via hosted url.

# first let's define the database schema.
from schema import VideoRegisterData, VideoStatistics
import fastapi
import uvicorn
from typing import Optional, Literal
import tsdb
import db
from config import HOST_ADDRESS, RECORD_PORT
from enums import RecordEndpoint
import util

app = fastapi.FastAPI(
    title="Video Monitor API",
    description="API for managing and querying video data",
    version="1.0",
)


@app.get(RecordEndpoint.query_current_view_count)
def query_current_view_count(url: str):
    # Add your implementation here
    return {"data": "Current view count"}


@app.get(RecordEndpoint.query_history_view_count)
def query_history_view_count(url: str):
    # Add your implementation here
    return {"data": "History view count"}


@app.get(RecordEndpoint.query_video_url)
def query_video_url(projectPath: Optional[str], videoPath: Optional[str]):
    # Add your implementation here
    return {"data": "Video URL"}


@app.get(RecordEndpoint.query_videos)
def query_videos(
    platform: Optional[str],
    type: Literal["latest", "trending", "popular", "random"],  # currently not used.
    limit: int = 20,
):
    data = []
    with db.videodb_context() as vdb:
        candidates = vdb.search(cond=db.tinydb.Query().platform == platform)[:limit]
        for it in candidates:
            url= it["url"]
            vid = util.get_vid_from_url_and_platform(url, platform)
            data.append(vid)
    # Add your implementation here
    return {"status": "success", "data": data}


def register_video_to_database(video_data: VideoRegisterData):
    data = video_data.dict()
    # video url as unique
    with db.videodb_context() as vdb:
        vdb.upsert(data, cond=db.tinydb.Query().url == video_data.url)


# you should start here
@app.post(RecordEndpoint.register_video)
def register_video(video_data: VideoRegisterData):
    # Add your implementation here
    success = False
    success = register_video_to_database(video_data)
    return {"success": success}


@app.post(RecordEndpoint.submit_video_statistics)
def submit_video_statistics(video_statistics: VideoStatistics):
    success = False
    success = tsdb.write_video_statistics_to_tsdb(video_statistics)
    return {"success": success}


if __name__ == "__main__":
    uvicorn.run(app, host=HOST_ADDRESS, port=RECORD_PORT)
