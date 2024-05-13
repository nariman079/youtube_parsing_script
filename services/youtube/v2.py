"""
-- Youtube services V1 --
"""
from pathlib import Path
import json

from base_datas import base_json_file

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