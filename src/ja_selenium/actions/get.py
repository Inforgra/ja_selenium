import logging
import time

from selenium.common.exceptions import WebDriverException

from ..exception import JaSeleniumError
from .action import Action

class Get(Action):

    @staticmethod
    def params():
        return ["url", "sleep"]

    def __init__(self, url, sleep=2):
        self.logger = logging.getLogger('ja_selenium.Get')
        self.url = url
        self.sleep = sleep

    def run(self):
        self.logger.debug(f'Action Get - url: {self.url}')
        try:
            driver = self.get_driver()
            driver.get(self.url)
            time.sleep(self.sleep)
        except WebDriverException as e:
            raise JaSeleniumError(f'웹 페이지 요청 실패 - url: {self.url}, msg: {e.msg}')
