import logging
import time
import urllib.parse

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from .action import Action
from ..exception import JaSeleniumError

class ComNaverLogin(Action):

    @staticmethod
    def params():
        return ["auth", "session"]

    def __init__(self, auth, session, sleep=3):
        self.logger = logging.getLogger('ja_selenium.ComNaverLogin')
        self.auth = auth
        self.session = session
        self.sleep = sleep

    def run(self):
        self.logger.debug("네이버 로그인을 실행합니다.")
        try:
            driver = self.controller.get_driver()
            driver.get('http://www.naver.com')
            driver.add_cookie({ "name": "NID_AUT", "value": self.auth, "domain": ".naver.com" })
            driver.add_cookie({ "name": "NID_SES", "value": self.session, "domain": ".naver.com" })
            time.sleep(self.sleep)
            driver.get('http://www.naver.com')
            time.sleep(self.sleep)
        except WebDriverException as e:
            raise JaSeleniumError(f'네이버 로그인 실패 - msg: {e.msg}')
