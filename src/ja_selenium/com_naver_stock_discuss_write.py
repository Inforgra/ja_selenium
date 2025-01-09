import ja_selenium
import json
import logging
import os
import random
import time
import typer
import typing_extensions

from selenium.common.exceptions import WebDriverException

CONTENTS = [
    ("매수와 매도 타점을 복기해 봅시다.", "6분 투자로 나의 타점을 한번 복기해 보시길 바랍니다."),
    ("지지와 저항이 발생하는 가격대를 복기해 봅시다.", "6분 투자로 나의 타점을 한번 복기해 보시길 바랍니다."),
    ("가격 움직임에 따른 호가와 차트의 변화를 복기해 봅시다.", "6분 투자로 가격과 호가의 변화를 복기해 보시길 바랍니다."),
    ("거래량이 늘면서 가격이 어떻게 움직이는지 복기해 봅시다.", "6분 투자로 가격과 호가의 변화를 복기해 보시길 바랍니다."),
]

def parse(play):
    (date, stockname, stockcode) = play["title"].split(" ")[:3]
    url = play["url"]
    title, content = random.choice(CONTENTS)
    return {
        "date": date,
        "stockcode": stockcode,
        "stockname": stockname,
        "title": title,
        "content": f"{content}\n{url}",
    }

def main(
        nid_auth: typing_extensions.Annotated[str, typer.Option(help="NID_AUTH")] = None,
        nid_session: typing_extensions.Annotated[str, typer.Option(help="NID_SESSION")] = None,
        playlist: typing_extensions.Annotated[str, typer.Option(help="PLAYLIST")] = None,
):
    logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %I:%M:%S')
    logging.getLogger("ja_selenium").setLevel(logging.DEBUG)

    nid_auth = os.environ["NID_AUTH"]
    nid_session = os.environ["NID_SESSION"]
    playlist = os.environ["PLAYLIST"]
    json_path = "/data/trading-note/youtube-playlist.json"

    driver = ja_selenium.createDriver()

    actions = [
        ["com_youtube_save_playlist", json_path, playlist],
        ["com_naver_login", nid_auth, nid_session],
        ["sleep", 10],
        ["com_naver_stock_mobile_remove_all_discusses"],
    ]

    ja_selenium.runner(driver)(actions)

    actions = []
    with open(json_path) as fp:
        playlist = [ parse(play) for play in json.load(fp) ]
        recent_date = playlist[0]["date"]
        playlist = [ play for play in playlist if play["date"] == recent_date ]
        for play in playlist:
            actions.append([
                "com_naver_stock_mobile_write_discuss",
                play["stockcode"],
                play["title"],
                play["content"],
            ])
            if play != playlist[-1]:
                actions.append(["sleep", 70])

    print(actions)
    try:
        ja_selenium.runner(driver)(actions)
    except WebDriverException as e:
        time.sleep(10)
        raise e

app = typer.Typer()
app.command()(main)

if __name__ == "__main__":
    app()
