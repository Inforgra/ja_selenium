import logging

from selenium import webdriver

from .actions import ACTION_TABLE
from .exception import JaSeleniumError

class JaSelenium:

    def __init__(self, options=None):
        self.logger = logging.getLogger('ja_selenium.JaSelenium')
        self.driver = None
        self.state = {}
        self.options = options
        self.actions = []

    def get_driver(self):
        return self.driver

    def get_state(self, key):
        return self.state[key]

    def set_state(self, key, value):
        self.logger.debug(f'상태변경 {key}: {value}')
        self.state[key] = value

    def set_actions(self, actions):
        for action in actions:
            cls = ACTION_TABLE[action["action"]]
            params = [ (k, v) for k, v in action.items() if k in cls.params() ]
            params = dict(params)
            self.actions.append([cls, params])

    def start(self):
        options = webdriver.FirefoxOptions()
        options.binary_location = "/usr/bin/firefox"
        options.add_argument("--display=:4")
        options.profile = "/home/kjkang/.mozilla/firefox/2p9ha9qk.selenium"
        self.logger.info("웹드라이버를 시작합니다.")
        self.driver = webdriver.Firefox(options=options)
        try:
            for cls, params in self.actions:
                self.logger.info(f"액션을 실행합니다 - {cls}, {params}")
                action = cls(**params)
                action.set_controller(self)
                action.run()
        except JaSeleniumError as e:
            self.logger.error(e)
        finally:
            self.logger.info("웹드라이브를 종료합니다.")
            self.driver.close()
