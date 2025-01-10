import logging
import random
import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .action import Action
from ..exception import JaSeleniumError


class ComNaverStockDiscussWrite(Action):

    @staticmethod
    def params():
        return ["stockcode_list", "contents", "login_list"]

    def __init__(self, stockcode_list, contents, login_list):
        self.logger = logging.getLogger('ja_selenium.ComNaverStockDiscussWrite')
        self.stockcode_list = stockcode_list
        self.contents = contents
        self.login_list = login_list
        self.login_index = 0

    def run(self):
        self.login()
        for (date, _, stockcode, url) in self.controller.get_state(self.stockcode_list):
            if self.check(stockcode):
                self.logger.info(f'토론장내에 내 글이 있습니다 - stockcode: {stockcode}')
            else:
                self.remove(stockcode)
                title, content = random.choice(self.contents)
                content = content.replace('[URL]', url)
                self.write(stockcode, title, content)

    def login(self):
        try:
            if self.login_index > len(self.login_list) - 1:
                raise JaSeleniumError('Failed ComNaverStockDiscussWrite.login - 더 이상 로그인할 ID가 없습니다.')
            login = self.login_list[self.login_index]
            driver = self.controller.get_driver()
            driver.get('http://www.naver.com')
            driver.add_cookie({"name": "NID_AUT", "value": login["auth"], "domain": ".naver.com"})
            driver.add_cookie({"name": "NID_SES", "value": login["session"], "domain": ".naver.com"})
            time.sleep(1)
            driver.get('http://www.naver.com')
            time.sleep(1)
            self.login_index = self.login_index + 1
        except WebDriverException as e:
            raise JaSeleniumError(f'Failed ComNaverStockDiscussWrite.login - index: {self.index}, msg: {e.msg}')

    def check(self, stockcode):
        self.logger.info(f'네이버 증권 토론장에서 내 글을 확인합니다 - stockcode: {stockcode}')
        try:
            driver = self.controller.get_driver()
            url = f'https://m.stock.naver.com/domestic/stock/{stockcode}/discuss'
            self.logger.debug(f'페이지를 요청합니다 - url: {url}')
            driver.get(url)
            time.sleep(3)
            driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            articles = driver.find_elements(By.CSS_SELECTOR, "ul[class*=DiscussListItem_list] li")
            for article in articles:
                desc = article.find_elements(By.CSS_SELECTOR, 'span[class*=DiscussListItem_desc]')
                if len(desc) == 0:
                    continue
                if '*' not in desc[0].text:
                    return True
            return False
        except WebDriverException as e:
            raise JaSeleniumError(f'Failed ComNaverStockDiscussWrite.check - stockcode: {stockcode}, msg: {e.msg}')

    def remove(self, stockcode):
        self.logger.info(f'네이버 증권 토론장에서 내 글을 삭제합니다 - stockcode: {stockcode}')
        try:
            driver = self.controller.get_driver()
            url = f'https://m.stock.naver.com/discuss/my/domestic/stock/{stockcode}'
            self.logger.debug(f'페이지를 요청합니다 - url: {url}')
            driver.get(url)
            time.sleep(3)
            for el in driver.find_elements(By.CSS_SELECTOR, 'ul[class*=DiscussListItem_list] li'):
                el.find_element(By.CSS_SELECTOR, 'button[class*=DiscussListItem_menu]').click()
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, 'button[class*=DiscussListItem_editButton]').click()
                time.sleep(1)
                driver.find_element(By.CSS_SELECTOR, 'button[class*=button_confirm]').click()
        except WebDriverException as e:
            raise JaSeleniumError(f'Failed ComNaverStockDiscussWrite.remove - stockcode: {stockcode}, msg: {e.msg}')

    def write(self, stockcode, title, content):
        self.logger.info(f'네이버 증권 토론장에 글을 작성합니다')
        self.logger.debug(f"stockcode: {stockcode}")
        self.logger.debug(f"title    : {title}")
        self.logger.debug(f"content  : {content}")
        try:
            driver = self.controller.get_driver()
            url = f"https://m.stock.naver.com/domestic/stock/{stockcode}/discuss"
            self.logger.debug(f'페이지를 요청합니다 - url: {url}')
            driver.get(url)
            time.sleep(1)
            try:
                text = driver.find_element(By.CSS_SELECTOR, 'div[class*=Dialog_article]').text
                self.logger.debug(f'토론장 메시지: {text}')
                if "1분" in text:
                    time.sleep(60)
                    driver.get(url)
                if "30건" in text:
                    self.login()
                    driver.get(url)
            except WebDriverException:
                pass
            driver.find_element(By.CSS_SELECTOR, "button[class*=DiscussView_button-write]").click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "input[class*=DiscussWritePage_input]").send_keys(title)
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "textarea[class*=DiscussWritePage_textarea]").send_keys(content)
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "button[class*=DiscussWritePage_button]").click()
        except WebDriverException as e:
            raise JaSeleniumError(f'Failed ComNaverStockDiscussWrite.write - stockcode: {stockcode}, msg: {e.msg}')
