"""
This is docstring
"""
from services.main_services import (install_video_form_file,
                                check_channel_last_video,
                                download_video_in_youtube,
                                get_video_url_from_channel)

while True:
    try:
        method = int(input('Actions:\n'
                           '1. Automatic download\n' 
                           '2. Upload using urls.txt\n' 
                           '3. Get urls\n'
                           '4. Download video from url\nEnder download method (1,2,3 or 4):'))
        if method in [1,2,3,4]:
            break
    except TypeError as errors:
        print("Enter correnct value")
        continue

match method:
    case 1:
        channel_url = input("Enter channel url:") or 'https://www.youtube.com/@operativnik444/videos'
        check_channel_last_video(channel_url=channel_url)
    case 2:
        txt_file = input("Enter txt filename:") or '@eminem.txt'
        install_video_form_file(txt_file)
    case 3:
        channel_url = input('Enter channel url:') or 'https://www.youtube.com/@eminem/videos'
        try:
            while True:
                install_immediately = int(input("Install immediately? (1-True or 0-False): "))

                if install_immediately in [1,0]:
                    get_video_url_from_channel(
                        channel_url=channel_url,
                        install_immediately=install_immediately
                        )
                    break
                print('Enter correct value')

        except TypeError:
            print("Enter correct value")

    case 4:
        video_url = input("Enter video url:") or 'https://www.youtube.com/watch?v=rR3PcMB1bNw'
        download_video_in_youtube(video_url=video_url, id_=1, all_video_count=1)
    case _:
        pass
