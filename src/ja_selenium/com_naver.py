import logging
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

logger = logging.getLogger("ja_selenium.com_naver")

def com_naver_login(nid_auth, nid_session, driver):
    """
    네이버 - 로그인
    """
    logger.debug("com_naver_login()")
    try:
        driver.get("https://www.naver.com")
        driver.add_cookie({ "name": "NID_AUT", "value": nid_auth, "domain": ".naver.com" })
        driver.add_cookie({ "name": "NID_SES", "value": nid_session, "domain": ".naver.com" })
        time.sleep(1)
        driver.get("https://www.naver.com")
    except WebDriverException as e:
        logger.error(f"com_naver_login() - {e.msg}")
        raise e

def com_naver_stock_mobile_remove_first_discuss(driver):
    """
    네이버::증권 - 내가 쓴 게시글 중 첫번째 게시글 삭제
    """
    logger.debug("com_naver_stock_mobile_remove_first_discuss()")
    try:
        driver.get("https://m.stock.naver.com/discuss/my/domestic/stock/005930?search=all")
        stockname = driver.find_element(By.CSS_SELECTOR, "ul[class*=DiscussListItem] li:first-child a:first-child div").text
        title = driver.find_element(By.CSS_SELECTOR, "ul[class*=DiscussListItem] li:first-child a:first-child strong").text
        content = driver.find_element(By.CSS_SELECTOR, "ul[class*=DiscussListItem] li:first-child a:first-child p").text
        logger.info(f"게시글을 삭제합니다. - stockname: {stockname}, title: {title}, content: {content}")
        driver.find_element(By.CSS_SELECTOR, "ul[class*=DiscussListItem] li:first-child button[class*=DiscussListItem_menu]").click()
        driver.find_element(By.CSS_SELECTOR, "button[class*=DiscussListItem_editButton]").click()
        driver.find_element(By.CSS_SELECTOR, "button[class*=Dialog_button][class*=button_confirm]").click()
        logging.info("게시글을 삭제하였습니다.")
    except WebDriverException as e:
        logger.error(f"com_naver_stock_mobile_remove_first_discuss() - {e.msg}")
        raise e

def com_naver_stock_mobile_remove_last_discuss(driver):
    """
    네이버::증권 - 내가 쓴 게시글 중 마지막 게시글 삭제
    """
    logger.debug("com_naver_stock_mobile_remove_last_discuss()")
    try:
        driver.get("https://m.stock.naver.com/discuss/my/domestic/stock/005930?search=all")
        stockname = driver.find_element(By.CSS_SELECTOR, "ul[class*=DiscussListItem] li:last-child a:last-child div").text
        title = driver.find_element(By.CSS_SELECTOR, "ul[class*=DiscussListItem] li:last-child a:last-child strong").text
        content = driver.find_element(By.CSS_SELECTOR, "ul[class*=DiscussListItem] li:last-child a:last-child p").text
        logger.info(f"게시글을 삭제합니다. - stockname: {stockname}, title: {title}, content: {content}")
        driver.find_element(By.CSS_SELECTOR, "ul[class*=DiscussListItem] li:last-child button[class*=DiscussListItem_menu]").click()
        driver.find_element(By.CSS_SELECTOR, "button[class*=DiscussListItem_editButton]").click()
        driver.find_element(By.CSS_SELECTOR, "button[class*=Dialog_button][class*=button_confirm]").click()
        logging.info("게시글을 삭제하였습니다.")
    except WebDriverException as e:
        logger.error(f"com_naver_stock_mobile_remove_last_discuss() - {e.msg}")
        raise e


def com_naver_stock_mobile_remove_all_discusses(driver):
    """
    네이버::증권 - 내가 쓴 게시글 모두 삭제
    """
    logger.debug("com_naver_stock_mobile_remove_all_discusses()")
    while True:
        try:
            driver.get("https://m.stock.naver.com/discuss/my/domestic/stock/005930?search=all")
            discusses = driver.find_elements(By.CSS_SELECTOR, "ul[class*=DiscussListItem]")
            if len(discusses) == 0:
                logger.info("내 게시글이 더 이상 없습니다.")
                return
            com_naver_stock_mobile_remove_first_discuss(driver)
        except WebDriverException as e:
            logger.error(f"com_naver_stock_mobile_remove_all_discusses() - {e.msg}")
            raise e

def com_naver_stock_mobile_write_discuss(stockcode, title, content, driver):
    """
    네이버::증권 - 글 게시 하기
    """
    logger.debug("com_naver_stock_mobile_write_discuss()")
    try:
        driver.get(f"https://m.stock.naver.com/domestic/stock/{stockcode}/discuss")
        driver.find_element(By.CSS_SELECTOR, "button[class*=DiscussView_button-write]").click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "input[class*=DiscussWritePage_input]").send_keys(title)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "textarea[class*=DiscussWritePage_textarea]").send_keys(content)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "button[class*=DiscussWritePage_button]").click()
    except WebDriverException as e:
        logger.error(f"com_naver_stock_mobile_write_discuss() - {e.msg}")
        raise e


ACTION_TABLE = {
    "com_naver_login": com_naver_login,
    "com_naver_stock_mobile_remove_first_discuss": com_naver_stock_mobile_remove_first_discuss,
    "com_naver_stock_mobile_remove_last_discuss": com_naver_stock_mobile_remove_last_discuss,
    "com_naver_stock_mobile_remove_all_discusses": com_naver_stock_mobile_remove_all_discusses,
    "com_naver_stock_mobile_write_discuss": com_naver_stock_mobile_write_discuss,
}
