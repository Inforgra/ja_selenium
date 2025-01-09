import logging
import time
import urllib.parse

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from .action import Action
from ..exception import JaSeleniumError

class ComNaverStockWriteDiscuss(Action):

    def __init__(self):
        self.logger = logging.getLogger('ja_selenium.ComNaverStockwriteDiscuss')

    def run(self):
        try:
            driver = self.controller.get_driver()
            for (date, _, stockcode, url) in self.controller.get_state('stockcode_list'):
                (title, content) = random.choice(self.controller.get_state('discusses'))
                content = content.replace("[URL]", url)
                self.write_discuss(stockcode, title, content)
                time.sleep(60)
        except WebDriverException as e:
            raise JaSeleniumError(f'네이버 증권 토론장 게시글 삭제 실패 - msg: {e.msg}')

    def write_discuss(stockcode, title, content):
        self.logger.debug("네이버 증권 토론장에 글을 작성합니다.")
        self.logger.debug(f"stockcode: {stockcode}")
        self.logger.debug(f"title    : {title}")
        self.logger.debug(f"content  : {content}")
        try:
            driver = self.controller.get_driver()
            url = f"https://m.stock.naver.com/domestic/stock/{stockcode}/discuss"
            self.logger.debug(f"네이버 종목 토론장으로 이동합니다. {url}")
            driver.get(url)
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "button[class*=DiscussView_button-write]").click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "input[class*=DiscussWritePage_input]").send_keys(title)
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "textarea[class*=DiscussWritePage_textarea]").send_keys(content)
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "button[class*=DiscussWritePage_button]").click()
        except WebDriverException as e:
            raise JaSeleniumError(f'네이버 증권 토론장 글쓰기 실패 - msg: {e.msg}')
