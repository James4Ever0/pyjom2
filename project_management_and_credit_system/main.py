# syntax:

# pyjom register_video --project_root jianying --video x.mp4 --project_name x --hosted_platform douyin --hosted_url https://...

# pyjom project_root_alias --project_root ... --alias jianying

# pyjom view_statistics --hosted_platform douyin --show_columns project_root,project_name,hosted_platform

# monitor via hosted url.

# first let's define the database schema.

from schema import VideoRegisterData
import fastapi
import uvicorn
import tinydb
import filelock
import contextlib
from typing import Optional, Literal
from config import VIDEODB_PATH

def get_lock_path(path:str):
    lock_path = ...
    return lock_path

def tinydb_context(db_path:str):
  lock_path=get_lock_path(db_path)
  with filelock.FileLock(lock_path):
    db=tinydb.TinyDB(db_path)
    yield db
from config import *

def videodb_context():
  yield tinydb_context(VIDEODB_PATH)
  
app = fastapi.FastAPI(
    title="Video Monitor API",
    description="API for managing and querying video data",
    version="1.0"
)

@app.get('/query/current_view_count')
def query_current_view_count(url:str):
    # Add your implementation here
    return {"data": "Current view count"}

@app.get('/query/history_view_count')
def query_history_view_count(url:str):
    # Add your implementation here
    return {"data": "History view count"}

@app.get('/query/video_url')
def query_video_url(projectPath:Optional[str], videoPath:Optional[str]):
    # Add your implementation here
    return {"data": "Video URL"}

@app.get('/query/videos')
def query_popular_video(platform:Optional[str], type:Literal['latest','trending','popular','random'], limit:int=20):
    # Add your implementation here
    return {"data": "Videos"}

def register_video_to_database(video_data:VideoRegisterData):
  data=video_data.to_dict()
  # video url as unique
  with videodb_context() as db:
    db.upsert()

# you should start here
@app.post('/register/video')
def register_video(video_data: VideoRegisterData):
    # Add your implementation here
    success=False
    success=register_video_to_database(video_data)
    return {"success":success}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
