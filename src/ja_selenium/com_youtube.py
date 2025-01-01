import logging
import json
import time
import random

from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

logger = logging.getLogger("ja_selenium.com_youtube")

TITLES = [
    "매수, 매도 타점을 찾아 봅시다.",
    "가격에 따라 호가와 차트가 어떻게 변해가는지 살펴봅시다.",
    "어떤 가격에서 지지와 저항이 나오는지 살펴봅시다.",
]

def com_youtube_save_playlist(path, url, driver):
    try:
        driver.get(url)
        time.sleep(3)
        urls = driver.find_elements(By.CSS_SELECTOR, "div[id=contents] ytd-playlist-video-renderer a[id=thumbnail]")
        urls = [ url.get_attribute("href") for url in urls ]
        titles = driver.find_elements(By.CSS_SELECTOR, "div[id=contents] ytd-playlist-video-renderer h3")
        titles = [ title.text for title in titles ]
        videos = [ {
            "title": title,
            "url": url,
        } for (url, title) in zip(urls, titles) ]
        logger.debug(f"{videos}")
        with open(path, "w") as fp:
            json.dump(videos, fp, ensure_ascii=False)
    except WebDriverException as e:
        logger.error(f"com_youtube_get_url_from_playlist() - {e.msg}")
        raise e

ACTION_TABLE = {
    "com_youtube_save_playlist": com_youtube_save_playlist
}
