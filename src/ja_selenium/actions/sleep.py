import logging
import time
from .action import Action


class Sleep(Action):

    @staticmethod
    def params():
        return ["sleep"]

    def __init__(self, sleep=5):
        self.logger = logging.getLogger('ja_selenium.Get')
        self.sleep = sleep

    def run(self):
        self.logger.debug(f'Action Sleep - sleep: {self.sleep}')
        time.sleep(self.sleep)
