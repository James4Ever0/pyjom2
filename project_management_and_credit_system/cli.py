# pyjom register_video --project_path jianying --video_path x.mp4 --platform douyin --url https://...

# pyjom view_statistics --platform douyin --show title,view_count,trend_index --sort trend_index

# so we have two switches.

# from typing import List
from schema import *
from config import *

import argparse
import requests

# Create the parser
parser = argparse.ArgumentParser(description='Command line program for registering video and viewing statistics')

# Subparsers for different commands
subparsers = parser.add_subparsers(dest='command', required=True)

# Subparser for 'register_video'
register_video_parser = subparsers.add_parser('register_video', help='Register a video')
register_video_parser.add_argument('--project_path', type=str, required=True, help='Path to the project')
register_video_parser.add_argument('--video_path', type=str, required=True, help='Path to the video file')
# register_video_parser.add_argument('--project_name', type=str, required=True, help='Name of the project')
register_video_parser.add_argument('--platform', type=str, required=True, help='Platform for the video')
register_video_parser.add_argument('--url', type=str, required=True, help='URL for the video')

# Subparser for 'view_statistics'
view_statistics_parser = subparsers.add_parser('view_statistics', help='View video statistics')
view_statistics_parser.add_argument('--platform', type=str, required=True, help='Platform for the statistics')
view_statistics_parser.add_argument('--show', type=str, nargs='+', required=True, help='Fields to show')
view_statistics_parser.add_argument('--sort', type=str, help='Field to sort by')

# Parse the arguments
args = parser.parse_args()

# Access the parsed arguments
if args.command == 'register_video':
    register_video_args = VideoRegisterData(**vars(args))
    print('Registering video with the following parameters:')
    print(register_video_args.dict())
    # make request
    reply = requests.post(f'{URL}/register/video', data=register_video_args.dict())
    data = reply.json()
elif args.command == 'view_statistics':
    view_statistics_args = ViewStatisticsArgs(**vars(args))
    print('Viewing statistics with the following parameters:')
    print(view_statistics_args.dict())
    reply=requests.get(f'{URL}/query/videos',params=dict(platform=view_statistics_args.platform))
    data=reply.json()