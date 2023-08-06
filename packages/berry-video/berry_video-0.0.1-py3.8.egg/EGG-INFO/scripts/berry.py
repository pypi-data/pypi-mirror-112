#!/home/erick-menezes/.virtualenvs/raspy/bin/python
import glob
import logging
import os
import requests
import subprocess
import sys


from berry_video import list_files, auto_start, set_update, Player


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

ARGS_VIDEO = ["--no-osd", "-local"]
BASE_URL = "https://drive.google.com/u/0/uc?id={}&export=download"


def get_video(path):
    files = list_files(path)
    return next(filter(lambda x: x["mimeType"] == "video/mp4", files), None)

def download_file(file, path):
        url_download = BASE_URL.format(file["id"])
        r = requests.get(url_download)
        file_path = os.path.join(path, file["name"])
        with open(file_path, 'wb') as fd:
            fd.write(r.content)

def update_video(path):
    local_videos = glob.glob(os.path.join(path, "*.mp4"))
    video = get_video(path)
    video_path = os.path.join(path, video["name"])
    if video_path not in local_videos:
        download_file(video, path)
        try:
            args = ARGS_VIDEO
            if "loop" in video_path:
                args.append("--loop")
            Player(video_path, args)#, "--loop"
        finally:
            if len(local_videos) > 0:
                command = ["rm"]
                command.extend(local_videos)
                subprocess.Popen(command)
        

def start(path):
    local_videos = glob.glob(os.path.join(path, "*.mp4"))
    if len(local_videos) > 0:
        video_path = os.path.join(path, local_videos[0])
        args = ARGS_VIDEO
        if "loop" in video_path:
            args.append("--loop")
        return Player(video_path, args), #"--loop"
    else:
        video = get_video(path)
        download_file(video, path)
        video_path = os.path.join(path, video["name"])
        args = ARGS_VIDEO
        if "loop" in video_path:
            args.append("--loop")
        return Player(video_path, args), #"--loop"


if __name__ == "__main__":
    command = sys.argv[1]
    file_path = os.path.abspath(__file__)
    auto_start(file_path)
    path = os.path.dirname(file_path)
    if command == "storage" or command == "secret":
        id = sys.argv[2].replace("https://drive.google.com/file/d/","").replace("/view?usp=sharing","")
        data_file = { "id": id, "name": "{}.json".format(command) } 
        download_file(data_file, path)
        list_files(path)
    elif command == "start":
        start(path)
    elif command == "update":
        update_video(path)
    elif command == "minutes":
        set_update(file_path, sys.argv[2])
