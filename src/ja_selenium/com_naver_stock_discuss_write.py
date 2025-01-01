import ja_selenium
import json
import os
import random
import time
import typer
import typing_extensions

from selenium.common.exceptions import WebDriverException

TITLES = [
    "효과적인 매매전략을 찾아봅시다.",
    "매수, 매도 타점을 분석해 봅시다.",
    "매수와 매도의 적절한 타이밍을 파악해봅시다.",
    "지지와 저항이 발생하는 가격을 발견해봅시다.",
    "지지와 저항이 형성되는 가격을 알아봅시다.",
    "가격 움직임에 따른 차트와 호가의 변화를 탐색해봅시다.",
    "가격 변동과 함께 살펴보는 호가와 차트.",
]

def parse(play):
    (date, stockname, stockcode) = play["title"].split(" ")[:3]
    url = play["url"]
    return {
        "date": date,
        "stockcode": stockcode,
        "stockname": stockname,
        "title": random.choice(TITLES),
        "content": f"\n{url}",
    }

def main(
        nid_auth: typing_extensions.Annotated[str, typer.Option(help="NID_AUTH")] = None,
        nid_session: typing_extensions.Annotated[str, typer.Option(help="NID_SESSION")] = None,
        playlist: typing_extensions.Annotated[str, typer.Option(help="PLAYLIST")] = None,
):
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

    try:
        ja_selenium.runner(driver)(actions)
    except WebDriverException as e:
        time.sleep(10)
        raise e

app = typer.Typer()
app.command()(main)

if __name__ == "__main__":
    app()
