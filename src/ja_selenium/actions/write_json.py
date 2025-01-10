import json
import logging
from .action import Action


class WriteJSON(Action):

    @staticmethod
    def params():
        return ["filename", "state_key"]

    def __init__(self, filename, state_key):
        self.logger = logging.getLogger('ja_selenium.WriteJSON')
        self.filename = filename
        self.state_key = state_key

    def run(self):
        value = self.controller.get_state(self.state_key)
        self.logger.debug(f'Action WriteJSON - key: {self.state_key}, value: {value}')
        with open(self.filename, 'w') as fp:
            json.dump(value, fp, ensure_ascii=False)
