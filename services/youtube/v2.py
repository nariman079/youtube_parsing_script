"""
-- Youtube services V1 --
"""
from pathlib import Path
import json
import os

from base_datas import base_json_file
from utils.pytube.__main__ import YouTube

def is_exists_file(file_name: str, path: Path) -> bool:
    """
    If file is exists in path, then True 

    :param str file_name
    :param Path path
    """
    files = list(filter(lambda x: x.is_file(), path.iterdir()))
    is_exists = bool(list(filter(lambda x: file_name in x.name, files)))

    return is_exists


def is_new_video(channel_name: str, video_id: str) -> bool:
    """
    Video is last video of channel?
    """
    is_new = False

    json_data = json.loads(
        base_json_file.read_text(encoding='utf-8'),
        )

    if not json_data.get(channel_name):
        json_data[channel_name] = video_id
        is_new = True

    if not json_data.get(channel_name) == video_id:
        json_data[channel_name] = video_id
        is_new = True

    base_json_file.write_text(
        json.dumps(json_data),
        encoding='utf-8'
        )

    return is_new

class DownloadVideo:
    """
    Download video
    """
    def __init__(self) -> None:
        self.video = YouTube(
            input('Ender video url: ') or
            'https://www.youtube.com/watch?v=N3onZdIIPh0'
            )
        self.path = Path('.', 'downloads')

    def _check_is_exists_file(self) -> None:
        """
        Checking is exists file in path
        """
        if not os.path.isdir(self.path):
            os.makedirs(self.path, exist_ok=True)

        self.is_exists = is_exists_file(
            self.video.title,
            self.path
        )

    def _setting_download_video(self) -> None:
        """
        Settigns download video format
        """
        while True:
            try:
                self.type = int(input("Type:\n1. Video\n2. Audio\nEnter variant (1 or 2) [default: 1]: ") or  1)
                if self.type in [1, 2]:
                    break
                else:
                    raise TypeError()
            except TypeError:
                print("Enter correct value!\n")
            except ValueError:
                print("Enter correct value!\n")

    def _check_video_type(self) -> None:
        """
        Check video type
        """
        while True:
            try:
                if self.type == 1:
                    self.video_quality = int(input('Quality:\n1. 1080p\n2. 720p\nEnter variant (1 or 2) [default: 2]: ') or 2)
                if self.type in [1, 2]:
                    break
                else:
                    raise TypeError()
            except TypeError:
                print("Enter correct value!\n")
            except ValueError:
                print("Enter correct value!\n")
        
    def _generate_filters(self)-> None:
        """
        Generate filters for search in Youtube
        """
        self.filter_kwargs = dict()
        if self.type == 2:
            self.filter_kwargs['only_audio'] = True
            self.path = self.path / Path('audios')
        elif self.type == 1:
            self.filter_kwargs['resolution'] = '1080p' if self.video_quality == 1 else '720p'
            self.path = self.path / Path('videos')
        print(self.filter_kwargs)
        if not os.path.isdir(self.path):
                os.makedirs(self.path, exist_ok=True)

    def _download_file(self) -> None:
        """
        download file
        """
        print("Instalation file")
        if video_for_download := self.video.streams.filter(**self.filter_kwargs).first():
            video_for_download.download(output_path=self.path)

    def execute(self) -> None:
        """
        Run command
        """
        self._check_is_exists_file()
        if not self.is_exists:
            self._setting_download_video()
            self._check_video_type()
            self._generate_filters()
            self._download_file()
