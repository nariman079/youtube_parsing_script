"""
-- Selenim worker --
"""
import os
import time
import asyncio
import pandas
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import FirefoxOptions, FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager


from services.youtube.v1 import YoutubeCsm
from base_dataclasses import YouTubeVideo
from base_datas import BASE_CSV_LIST_PATH, BASE_TXT_LIST_PATH


def create_video_obj(current_html_element: WebElement) -> YouTubeVideo:
    """
    Create video object with type YouTubeVideo 
    """
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
        self.channel_name = "channel"

        self.options = FirefoxOptions()
        self.options.add_argument("--headless")
        self.driver = webdriver.Firefox(
            service=FirefoxService(
                executable_path=GeckoDriverManager().install()
            ),
            options=self.options,
        )
        self.driver.get(self.channel_url)
        self.wait()
        time.sleep(self.wait_second)

    def wait(self):
        """ Function for waiting download page """
        self.driver.implicitly_wait(time_to_wait=self.implicitly_wait_second)

    def _scroll_down(self):
        """ Scroll down in html """
        html = self.driver.find_element(By.TAG_NAME, "html")
        print('Search all videos')
        for _ in range(250):
            self.wait()
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
        channel_name = await self.get_channel_name

        if not os.path.isdir(BASE_CSV_LIST_PATH):
            os.mkdir(BASE_CSV_LIST_PATH)

        file_name = f"{channel_name}.csv"
        file_path: Path = Path(".", BASE_CSV_LIST_PATH, file_name)

        mapping_data = [{'id': i.video_id, 'url': i.url} for i in self.videos]
        data_frame = pandas.DataFrame(mapping_data)
        data_frame.to_csv(file_path)

        self.csv_file_name = file_name

        print(file_path, " ✅")

    async def _create_txt_file(self) -> None:
        """ Create txt file for urls """
        channel_name = await self.get_channel_name

        if not os.path.isdir(BASE_TXT_LIST_PATH):
            os.mkdir(BASE_TXT_LIST_PATH)

        file_name = f"{channel_name}.txt"
        file_path = Path(BASE_TXT_LIST_PATH, file_name)
        url_list = list(map(lambda video: video.url, self.videos))
        file_path.write_text('\n'.join(url_list), encoding='utf-8')

        self.txt_file_name = file_name

        print(file_path, " ✅")

    async def exeute(self):
        """ Run methods"""
        self.get_channel_name = asyncio.create_task(self._get_channel_name())

        self._scroll_down()
        self.wait()
        self._get_all_videos()

        create_txt_file = asyncio.create_task(self._create_txt_file())
        create_exel_file = asyncio.create_task(self._create_csv_file())
        print("Create txt and csv files")
        await create_txt_file
        await create_exel_file
