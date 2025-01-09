import logging
import time

from .action import Action

class SetState(Action):

    @staticmethod
    def params():
        return ["key", "value"]

    def __init__(self, key, value):
        self.logger = logging.getLogger('ja_selenium.Get')
        self.key = key
        self.value = value

    def run(self):
        self.logger.debug(f'상태를 저장합니다. - {self.key}: {self.value}')
        self.controller.set_state(self.key, self.value)
