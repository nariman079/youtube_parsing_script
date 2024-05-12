"""
-- Main services --
"""
import os
import asyncio
import time
from datetime import datetime
from typing import List

from utils.pytube import YouTube
from utils.pytube.exceptions import AgeRestrictedError, VideoUnavailable
from services.youtube_services import YoutubeCsm, is_exists_file, is_new_video
from services.selenium_services import YoutubeSelenium
from base_datas import (BASE_DOWNLOAD_PATH, BASE_TXT_LIST_PATH,
                        BASE_URL_FILE)

def download_video_in_youtube(
    instalation_path: str = 'video/',
    video_url: str = '',
    id_: int = 0,
    all_video_count: int = 0) -> None:
    """
    Download video by video url
    """
    youtube = YouTube(video_url)
    full_path = BASE_DOWNLOAD_PATH + instalation_path

    if not os.path.isdir(full_path):
        os.makedirs(full_path, exist_ok=True)

    try:
        new_filename = f"{datetime.now().strftime(r'%d-%m-%Y %H:%M')}|{youtube.title}.mp4"
        if is_exists_file(new_filename, full_path):
            pass
        else:
            video_highest = youtube.streams.get_highest_resolution()
            if video := video_highest:
                video.download(output_path=full_path, filename=new_filename)
            print(f"✅ ({id_}/{all_video_count}) - {youtube.title} ")
    except AgeRestrictedError:
        print(f"🔞 ({id_}/{all_video_count}) - {youtube.title} ")
    except FileNotFoundError:
        print(f"⭕ ({id_}/{all_video_count}) - {youtube.title} ")
    except VideoUnavailable:
        print(f"❌ ({id_}/{all_video_count}) - {youtube.title} ")

def install_video_form_file(
        ursl_txt_file: str | None = BASE_URL_FILE,
        instalation_path: str = 'video'
        ) -> None:
    """
    Installation video from urls.txt
    """
    with open(f'{BASE_TXT_LIST_PATH}{ursl_txt_file}', 'r', encoding='utf-8') as file:
        all_urls: List[str] = file.readlines()
        for _, url in enumerate(all_urls):
            if len(url) > 10:
                download_video_in_youtube(
                    video_url=url, id_=_+1,
                    all_video_count=len(all_urls), 
                    instalation_path=instalation_path
                    )
                        

def check_channel_last_video(channel_url) -> None:
    """ Check youtube channel on new video"""
    i = 0

    while True:
        i += 1
        channel = YoutubeCsm(channel_url=channel_url)
        last_video = channel.get_last_video()
        if last_video:
            if is_new_video(channel.channel_name, video_id=last_video.video_id):
                path = f"channels/{channel.channel_name}/videos/"
                download_video_in_youtube(video_url=last_video.url, instalation_path=path, id_=1, all_video_count=1)
                time.sleep(60)

        print(f"Request {i}: Not new video")
        time.sleep(10)

def get_video_url_from_channel(channel_url, install_immediately: int = 0):
    """ Getting video urls from channel """
    selenium_action = YoutubeSelenium(channel_url=channel_url)
    asyncio.run(selenium_action.exeute())

    if install_immediately == 1:
        path = f"channels/{selenium_action.channel_name}/videos/"
        install_video_form_file(selenium_action.txt_file_name, instalation_path=path)
