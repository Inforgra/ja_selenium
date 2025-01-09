from .action import Action
from .com_naver_login import ComNaverLogin
from .com_naver_stock_fetch_stockcode_list_from_youtube_play_list import ComNaverStockFetchStockcodeListFromYoutubePlayList
from .com_naver_stock_remove_all_discuss import ComNaverStockRemoveAllDiscuss
from .com_naver_stock_write_discuss import ComNaverStockWriteDiscuss
from .com_youtube_fetch_video_from_play_list import ComYoutubeFetchVideoFromPlayList
from .get import Get
from .set_state import SetState
from .sleep import Sleep
from .write_json import WriteJSON

ACTION_TABLE = {
    'com_naver_login': ComNaverLogin,
    'com_naver_stock_fetch_stockcode_list_from_youtube_play_list': ComNaverStockFetchStockcodeListFromYoutubePlayList,
    'com_naver_stock_remove_all_discuss': ComNaverStockRemoveAllDiscuss,
    'com_naver_stock_write_discuss': ComNaverStockWriteDiscuss,
    'com_youtube_fetch_video_from_play_list': ComYoutubeFetchVideoFromPlayList,
    'get': Get,
    'set_state': SetState,
    'sleep': Sleep,
    'write_json': WriteJSON,
}
