import logging
import time
import urllib.parse

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from .action import Action
from ..exception import JaSeleniumError

class ComNaverStockRemoveAllDiscuss(Action):

    @staticmethod
    def params():
        return []

    def __init__(self):
        self.logger = logging.getLogger('ja_selenium.ComNaverStockRemoveAllDiscuss')

    def run(self):
        try:
            driver = self.controller.get_driver()
            while True:
                driver.get("https://m.stock.naver.com/discuss/my/domestic/stock/005930?search=all")
                discusses = driver.find_elements(By.CSS_SELECTOR, "ul[class*=DiscussListItem]")
                if len(discusses) == 0:
                    self.logger.info("내 게시글이 더 이상 없습니다.")
                    return
                self.remove_first_discuss()
                time.sleep(1)
        except WebDriverException as e:
            raise JaSeleniumError(f'네이버 증권 토론장 게시글 삭제 실패 - msg: {e.msg}')


    def remove_first_discuss(self):
        self.logger.debug("첫번째 게시글을 삭제합니다.")
        try:
            driver = self.controller.get_driver()
            driver.get("https://m.stock.naver.com/discuss/my/domestic/stock/005930?search=all")
            stockname = driver.find_element(By.CSS_SELECTOR, "ul[class*=DiscussListItem] li:first-child a:first-child div").text
            title = driver.find_element(By.CSS_SELECTOR, "ul[class*=DiscussListItem] li:first-child a:first-child strong").text
            content = driver.find_element(By.CSS_SELECTOR, "ul[class*=DiscussListItem] li:first-child a:first-child p").text
            self.logger.info(f"게시글을 삭제합니다. - stockname: {stockname}, title: {title}, content: {content}")
            driver.find_element(By.CSS_SELECTOR, "ul[class*=DiscussListItem] li:first-child button[class*=DiscussListItem_menu]").click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "button[class*=DiscussListItem_editButton]").click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "button[class*=Dialog_button][class*=button_confirm]").click()
            time.sleep(1)
        except WebDriverException as e:
            raise JaSeleniumError(f'네이버 증권 토론장 첫번째 게시글 삭제 실패 - msg: {e.msg}')
