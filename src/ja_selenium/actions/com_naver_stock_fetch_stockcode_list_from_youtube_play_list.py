import logging
from .action import Action


class ComNaverStockFetchStockcodeListFromYoutubePlayList(Action):

    @staticmethod
    def params():
        return ["state_key_read", "state_key_write"]

    def __init__(self, state_key_read, state_key_write):
        self.logger = logging.getLogger('ja_selenium.ComNaverStockFetchStockcodeListFromYoutubePlaylist')
        self.state_key_read = state_key_read
        self.state_key_write = state_key_write

    def run(self):
        self.logger.info("유튜브 목록에서 종목코드를 추출합니다.")
        play_list = self.controller.get_state(self.state_key_read)
        stockcode_list = [self.parse_title(play['title']) + [play["url"]] for play in play_list]
        recent_date = stockcode_list[0][0]
        stockcode_list = [xs for xs in stockcode_list if xs[0] == recent_date]
        self.logger.debug(f"유튜브 목록: {stockcode_list}")
        self.controller.set_state(self.state_key_write, stockcode_list)

    def parse_title(self, title):
        xs = title.split(" ")
        return [xs[0], xs[1], xs[2]]
