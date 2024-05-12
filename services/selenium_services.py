"""
-- Selenim worker --
"""
import os
import time
import asyncio

import pandas
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from services.youtube_services import YoutubeCsm
from base_dataclasses import YouTubeVideo
from base_datas import BASE_CSV_LIST_PATH, BASE_TXT_LIST_PATH

def create_video_obj(current_html_element: WebElement) -> YouTubeVideo:
    thumbnail = current_html_element.find_element(
        By.ID, 'thumbnail'
        ).find_element(
        By.TAG_NAME, 'img'
        ).get_attribute('src') or ""
    title = current_html_element.find_element(By.ID, 'video-title').text
    url = current_html_element.find_element(
        By.ID, 'thumbnail'
        ).find_element(By.TAG_NAME, 'a').get_attribute('href') or ""
    length_text = current_html_element.find_element(
        By.ID, 'overlays'
        ).find_element(
        By.CLASS_NAME, 'badge-shape-wiz__text'
        ).text
    video_id = url.split('v=')[1]

    return YouTubeVideo(
        video_id=video_id,
        tumbnail_url=thumbnail,
        url=url,
        title=title,
        description="",
        length_text=length_text,
    )

class YoutubeSelenium:
    """ Actions with Youtube and selenium """

    wait_second = 2
    implicitly_wait_second = 10

    def __init__(self, channel_url: str) -> None:
        self.channel_url = channel_url
        self.html_elements = []
        self.videos = []

        self.get_channel_name = None
        self.txt_file_name = None
        self.csv_file_name = None
        self.channel_name = None
        self.options = Options()
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.options
            )
        self.driver.get(self.channel_url)
        self.wait()
        time.sleep(self.wait_second)

    def wait(self):
        """ Function for waiting download page """
        self.driver.implicitly_wait(time_to_wait=self.implicitly_wait_second)

   

    def _scroll_down(self):
        """ Scroll down in html """
        for _ in range(100):
            self.wait()
            html = self.driver.find_element(By.TAG_NAME, "html")
            print(f"Page down {_}")
            html.send_keys(Keys.END)
            self.wait()

    def _get_all_videos(self):
        """Get all videos"""
        self.html_elements = self.driver.find_elements(By.ID, 'dismissible')
        self.videos = list(map(create_video_obj, self.html_elements))

    async def _get_channel_name(self) -> str:
        """ Get channel name for naming file """
        self.channel_name = YoutubeCsm(self.channel_url).channel_name
        return self.channel_name

    async def _create_csv_file(self):
        """ Create csv file for urls """
        mapping_data = [{'id':i.video_id, 'url':i.url } for i in self.videos]
        data_frame = pandas.DataFrame(mapping_data)
        channel_name = await self.get_channel_name
        file_name = channel_name + ".csv"

        if not os.path.isdir(BASE_CSV_LIST_PATH):
            os.mkdir(BASE_CSV_LIST_PATH)

        data_frame.to_csv(BASE_CSV_LIST_PATH + file_name)
        self.csv_file_name = file_name

        print(BASE_CSV_LIST_PATH + file_name + " ✅")

    async def _create_txt_file(self) -> None:
        """ Create txt file for urls """
        channel_name = await self.get_channel_name
        file_name = channel_name + ".txt"

        if not os.path.isdir(BASE_TXT_LIST_PATH):
            os.mkdir(BASE_TXT_LIST_PATH)

        with open(BASE_TXT_LIST_PATH + file_name, 'w+', encoding='utf-8') as file:
            url_list = [video.url+"\n" for video in self.videos]
            file.writelines(url_list)

            self.txt_file_name = file_name

            print(BASE_TXT_LIST_PATH + file_name + " ✅")

    async def exeute(self):
        """ Run methods"""
        self.get_channel_name = asyncio.create_task(self._get_channel_name())

        self._scroll_down()
        self.wait()
        self._get_all_videos()

        create_txt_file = asyncio.create_task(self._create_txt_file())
        create_exel_file = asyncio.create_task(self._create_csv_file())

        await create_txt_file
        await create_exel_file
        