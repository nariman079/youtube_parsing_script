"""
-- Test download file by parts --
"""
from pathlib import Path
import json

path = Path('.', '.data', 'channels_last_video.json')

json_data  = json.loads(path.read_text())
channel_name = '@pyjust'
video_id = 'efTxg'
is_new = False

if not json_data.get(channel_name):
    json_data[channel_name] = video_id
    is_new = True

if not json_data.get(channel_name) == video_id:
    json_data[channel_name] = video_id
    is_new = True

path.write_text(
    json.dumps(json_data),
    encoding='utf-8'
    )

print(json_data)
