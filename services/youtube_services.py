"""
-- Youtube services --
"""
import json
import os

from typing import List, Dict
from requests import get

from base_dataclasses import YouTubeVideo
from base_datas import (BASE_JSON_FILE,
                        BASE_VIDEO_BLOCK_TITLES)


def is_exists_file(full_file_name: str, path: str) -> bool:
    """
    If file is exists in path, then True 

    :param str full_file_name
    :param path
    """
    split_symbol = '|'
    file_name = full_file_name.split(split_symbol)[1] if split_symbol in full_file_name else None
    onlyfiles = list()
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            if split_symbol in full_file_name:
                onlyfiles.append(f.split(split_symbol)[1])
    return file_name in onlyfiles


def is_new_video(channel_name: str, video_id: str) -> bool:
    """
    Video is last video of channel?
    """
    is_new = False
    with open(BASE_JSON_FILE, 'r', encoding='utf-8') as file:
        json_data  = json.load(file)

        if not json_data.get(channel_name):
            json_data[channel_name] = video_id
            is_new = True

        if not json_data.get(channel_name) == video_id:
            json_data[channel_name] = video_id
            is_new = True

    with open(BASE_JSON_FILE, 'w', encoding='utf-8') as file:
        json.dump(json_data, file)

    return is_new

def is_video_block(value: dict) -> bool:
    """
    Search blocks with video
    """
    tab_render = value.get('tabRenderer')
    if tab_render:
        return tab_render['title'] in BASE_VIDEO_BLOCK_TITLES
    return False

def get_video_obj(video_data: dict | None) -> YouTubeVideo | None:
    """
    Getting video object
    """
    if video_data:
        video_render = video_data['richItemRenderer']['content']['videoRenderer']
        video_id: str = video_render['videoId']
        title: str = video_render['title']['runs'][0]['text']
        description: str =  video_render[
            'descriptionSnippet'][
            'runs'
                ][0][
            'text'] if video_render.get('descriptionSnippet') else ''
        length_text: str = video_render['lengthText']['simpleText']
        thumbnail_url: str = video_render['thumbnail']['thumbnails'][0]['url']
        url = "https://www.youtube.com/watch?v=" + video_id

        video = YouTubeVideo(
            video_id=video_id,
            title=title,
            description=description,
            length_text=length_text,
            url=url,
            tumbnail_url=thumbnail_url
        )
        return video
    else:
        return None



class YoutubeCsm:
    """ 
    Actions with Youtube 

    :param str channel_url
    """

    def __init__(self, channel_url: str):
        self.channel_url = channel_url
        self._parse_channel_information()

    @property
    def channel_name(self) -> str:
        """
        Get channel name
        """
        return self.channel_url.strip('https://').split('/')[1]

    def _parse_channel_information(self) -> None:
        """
        Get and parse channel information
        """
        response = get(url=self.channel_url, timeout=30)
        html_parts: List[str] = response.text.split('var ytInitialData =')
        channel_json: str = html_parts[1].split(';</script><script nonce=')[0]
        self.data = json.loads(channel_json)
        print(response.status_code)
        if not self.data:
            raise ValueError("Data not found!")

        self.tab_list: List[Dict] = self.data[
            'contents'][
            'twoColumnBrowseResultsRenderer'][
            'tabs']

        self.video_block: List[Dict] = list(filter(is_video_block, self.tab_list))

    def _get_all_video_json(self) -> List[Dict]:
        try:
            _video_list: List[Dict] = self.video_block[0][
                'tabRenderer'][
                'content'][
                'richGridRenderer'][
                'contents']
        except IndexError:
            _video_list = []
        return _video_list

    def get_all_video(self) -> List[YouTubeVideo | None] | None:
        """
        Generate YouTubeVideo list
        """
        all_video = self._get_all_video_json()
        if all_video:
            return list(map(get_video_obj, all_video))

    def get_last_video(self) -> YouTubeVideo | None:
        """
        Get last video from channel
        """
        try:
            last_video = self._get_all_video_json()[0]
        except IndexError:
            last_video = None

        return get_video_obj(last_video)
