"""
-- Youtube services V1 --
"""
from pathlib import Path
import json
import os
import shutil

import ffmpeg
from utils.pytube.__main__ import YouTube
from utils.pytube.exceptions import AgeRestrictedError, VideoUnavailable, RegexMatchError
from utils.pytube.query import StreamQuery

from base_datas import base_json_file
from services.youtube.v1 import strip_video_title
from utils.pytube.request import stream
from utils.pytube.streams import Stream


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

def generate_resolition(streams: StreamQuery):
    """ Generate resolition list """
    current_steams = streams.filter(only_video=True)
    resolution_list = { i.resolution for i in current_steams }

    resolution_dict = {}

    for i, v in enumerate(sorted(resolution_list)):
        resolution_dict[i] = v

    return resolution_list, resolution_dict

class DownloadVideo:
    """
    Download video
    """
    def __init__(self) -> None:
        while True:
            try:
                self.video = YouTube(
                    input('Ender video url: ') or
                    'https://www.youtube.com/watch?v=N3onZdIIPh0'
                    )
                break
            except RegexMatchError:
                print("Enter correct url")

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
           
            self.resolition_dict = generate_resolition(self.video.streams)[1]

            resolution = generate_resolition(self.video.streams)
            resolutions = "\n".join([f"{i}. {v}" for i, v in enumerate(sorted(resolution[0]))])
            if self.type == 1:
                self.video_quality = int(input(f'Quality:\n{resolutions}\nEnter variant [default: 0]: ') or 0)
                if self.video_quality in range(0, len(resolutions)):
                    break
                else:
                    print("")
            else:
                break            
            
        
    def _generate_filters(self)-> None:
        """
        Generate filters for search in Youtube
        """
        self.filter_kwargs = dict()
        if self.type == 2:
            self.filter_kwargs['only_audio'] = True
            self.path = self.path / Path('audios')
        elif self.type == 1:
            self.filter_kwargs['resolution'] = self.resolition_dict[self.video_quality]
            self.path = self.path / Path('videos')
        if not os.path.isdir(self.path):
                os.makedirs(self.path, exist_ok=True)

    def _download_file(self) -> None:
        """
        Download file
        """
        try:
            file_name = strip_video_title(
                f"{self.video.title}.mp3" if self.filter_kwargs.get('only_audio') else f"{self.video.title}.mp4"
                )
            if self.type == 1:   
                hd_video = self.video.streams.filter(**self.filter_kwargs).first()
                audio = self.video.streams.filter(only_audio=True).first()

                formatting_path = Path('.', 'formatting')

                hd_video_name = strip_video_title(self.video.title) + f"_{self.filter_kwargs['resolution']}.mp4"
                audio_name = strip_video_title(self.video.title) + "_audio.mp4"

                print(hd_video, audio)
                if hd_video and audio:

                    print("Video instalation")
                    hd_video.download(
                        output_path=formatting_path,
                        filename=hd_video_name)
                    
                    print("Audio instalation")
                    audio.download(
                        output_path=formatting_path,
                        filename=audio_name)

                    print("Converting and saving a file")
                    ffmpeg.output(
                        ffmpeg.input(formatting_path / audio_name),
                        ffmpeg.input(formatting_path / hd_video_name),
                        f'{self.path / hd_video_name}'
                    ).run()
                    print(f"✅ -  {self.video.title} ")
                    shutil.rmtree(formatting_path)
                    
            else:
                video_for_download = self.video.streams.filter(**self.filter_kwargs).last()
                if video_for_download:
                    video_for_download.download(output_path=self.path, filename=file_name)
                    print(f"✅ -  {self.video.title} ")
        except AgeRestrictedError:
            print(f"🔞 - {self.video.title} ")
        except FileNotFoundError:
            print(f"❌ - {self.video.title} ")
        except VideoUnavailable:
            print(f"❌ - {self.video.title} ")

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
    