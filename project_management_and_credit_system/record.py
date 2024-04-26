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
import functools

app = fastapi.FastAPI(
    title="Video Monitor API",
    description="API for managing and querying video data",
    version="1.0",
)

def query_current_view_count(vid: str, platform: str, diff:bool=False):
    # get latest view count with measurement timestamp
    datalist = query_history_view_count(vid, platform, diff)

    return datalist[-1]  # last to be latest or first?

def query_history_view_count(vid: str, platform: str, diff:bool=False):
    # get a list of view counts
    datalist = tsdb.query_view_count_list_by_vid_and_platform(vid, platform)
    if diff:
        datalist = tsdb.differentiate_data_by_key_and_timestamp_key(datalist, key='view_count')
    return datalist

@app.get(RecordEndpoint.query_current_view_count)(query_current_view_count)
@app.get(RecordEndpoint.query_history_view_count)(query_history_view_count)

@app.get(RecordEndpoint.query_video_url)
def query_video_url(projectPath: Optional[str], videoPath: Optional[str]):
    conditions = []
    query = db.tinydb.Query()
    if projectPath is not None:
        conditions.append(query.project_path == projectPath)
    if videoPath is not None:
        conditions.append(query.video_path == videoPath)
    if conditions == []:
        raise fastapi.HTTPException(
            status_code=400,
            detail="No condition was specified while querying video url",
        )
    with db.videodb_context() as vdb:
        cond = functools.reduce(lambda x, y: x & y, conditions)
        candidates = vdb.search(cond=cond)
        info = "Not found"
        url = "unknown"
        if len(candidates) == 1:
            info = "Found"
            url = candidates[0]["url"]
        ret = dict(info=info, url=url)
        return ret


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
            url = it["url"]
            vid = util.get_vid_from_url_and_platform(url, platform)
            data.append(vid)
    # Add your implementation here
    return {"status": "success", "data": data, "stats": candidates}


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
