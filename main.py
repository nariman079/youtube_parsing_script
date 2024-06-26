"""
This is docstring
"""
from services.main_services import (install_video_form_file,
                                check_channel_last_video,
                                download_video_in_youtube,
                                get_video_url_from_channel,
                                )
from services.youtube.v2 import DownloadVideo


while True:
    try:
        method = int(input('Actions:\n'
                           '1. Track channel on new video\n' 
                           '2. Download video using urls.txt or you file\n' 
                           '3. Get all video urls from channel\n'
                           '4. Download video from url\n'
                           '5. Download video or audio file form url\n'
                           'Ender download method (1, 2, 3, 4 or 5 ): '))

        if method in [1,2,3,4, 5]:
            break
    except TypeError:
        print("\nEnter correnct value\n")
        continue
    except ValueError:
        print("\nEnter correnct value\n")


match method:
    case 1:
        channel_url = input("Enter channel url:") or 'https://www.youtube.com/@eminem/videos'
        check_channel_last_video(channel_url=channel_url)
    case 2:
        txt_file = input("Enter txt filename:") or '@eminem.txt'
        install_video_form_file(txt_file)
    case 3:
        channel_url = input('Enter channel url:') or 'https://www.youtube.com/@eminem/videos'

        install_immediately = int(input("Install immediately? (1. Yes or 0. No)\nEnter variant: "))

        if install_immediately in [1,0]:
            get_video_url_from_channel(
                channel_url=channel_url,
                install_immediately=install_immediately
                )

        print('Enter correct value')



    case 4:
        # ✅
        video_url = input("Enter video url:") or 'https://www.youtube.com/watch?v=rR3PcMB1bNw'
        download_video_in_youtube(video_url=video_url, id_=1, all_video_count=1)
    case _:
        DownloadVideo().execute()