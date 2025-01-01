import copy
import functools
import itertools
import json
import time
import urllib

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import ja_selenium.com_naver
import ja_selenium.com_youtube

def sleep(sec, driver):
    time.sleep(sec)

def get(url, driver):
    driver.get(url)

def add_cookie(name, value, driver):
    cookie = { "name": name, "value": value }
    driver.add_cookie(cookie)

def add_cookie2(name, value, domain, driver):
    cookie = { "name": name, "value": value, "domain": domain }
    driver.add_cookie(cookie)

def click(selector, text, driver):
    for x in driver.find_elements(By.CSS_SELECTOR, selector):
        if text in x.text:
            x.click()
            break

def click_index(selector, index, driver):
    driver.find_elements(By.CSS_SELECTOR, selector)[index].click()

def save_links(path, selector, driver):
    elements = driver.find_elements(By.CSS_SELECTOR, selector)
    links = [ e.get_attribute("href") for e in elements ]
    with open(path, "w") as fp:
        json.dump(links, fp)

def save_youtube(path, selector, driver):
    def parse(url):
        return urllib.parse.parse_qs(urllib.parse.urlparse(url).query)['v'][0]
    elements = driver.find_elements(By.CSS_SELECTOR, selector)
    links = [ parse(e.get_attribute("href")) for e in elements ]
    with open(path, "w") as fp:
        json.dump(links, fp)

def send_keys(selector, keys, driver):
    driver.find_element().send_keys(keys)

ACTION_TABLE = {
    "sleep": sleep,
    "get": get,
    "add_cookie": add_cookie,
    "add_cookie2": add_cookie2,
    "click": click,
    "click_index": click_index,
    "save_links": save_links,
    "save_youtube": save_youtube,
    "send_keys": send_keys,
}

def build(table=None):
    TABLE = {}
    TABLE.update(ACTION_TABLE)
    TABLE.update(ja_selenium.com_naver.ACTION_TABLE)
    TABLE.update(ja_selenium.com_youtube.ACTION_TABLE)
    if table is not None:
        TABLE.update(table)
    return lambda actions: [ functools.partial(TABLE[action[0]], *action[1:]) for action in actions ]

def run(driver):
    def _run(actions):
        retval = driver
        for action in actions:
            if retval is None:
                return None
            action(driver)
        return retval
    return _run

def createDriver():
    options = webdriver.FirefoxOptions()
    options.binary_location = "/usr/bin/firefox"
    options.add_argument("--display=:4")
    options.profile = "/home/kjkang/.mozilla/firefox/2p9ha9qk.selenium"
    driver = webdriver.Firefox(options=options)
    return driver

def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

def runner(driver, table=None):
    return compose(run(driver), build(table))
