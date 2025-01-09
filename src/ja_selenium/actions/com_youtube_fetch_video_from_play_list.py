import logging
import urllib.parse

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from .action import Action
from ..exception import JaSeleniumError

class ComYoutubeFetchVideoFromPlayList(Action):

    @staticmethod
    def params():
        return ["state_key"]

    def __init__(self, state_key):
        self.logger = logging.getLogger('ja_selenium.ComYoutubeFetchVideoFromPlayList')
        self.state_key = state_key

    def run(self):
        try:
            driver = self.controller.get_driver()
            xs = driver.find_elements(By.CSS_SELECTOR, "div ytd-playlist-video-renderer")
            xs = [ self.search_video(x) for x in xs ]
            self.controller.set_state(self.state_key, xs)
        except WebDriverException as e:
            raise JaSeleniumError(f'유튜브 재생목록 가져오기 실패 - msg: {e.msg}')

    def search_video(self, parent_el):
        el = parent_el.find_element(By.CSS_SELECTOR, "a[id=video-title]")
        url = el.get_attribute('href')
        return { 'url': url, 'title': el.text, 'v': self.parse_v(url),}

    def parse_v(self, url):
        parsed_url = urllib.parse.urlparse(url)
        parsed_qs = urllib.parse.parse_qs(parsed_url.query)
        return parsed_qs['v']
