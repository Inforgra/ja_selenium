import logging
import json
import typer
from typing_extensions import Annotated
from .ja_selenium import JaSelenium


class NotTooLongStringFormatter(logging.Formatter):

    def __init__(self, fmt, max_length=120):
        super(NotTooLongStringFormatter, self).__init__(fmt)
        self.max_length = max_length

    def format(self, record):
        if len(record.msg) > self.max_length:
            record.msg = record.msg[:self.max_length] + "..."
        return super().format(record)

def main(
        config: Annotated[str, typer.Argument(help="actions json")] = None,
):

    fmt='%(asctime)s %(name)s %(levelname)s %(message)s'
    logging.basicConfig(format=fmt, level=logging.INFO, datefmt='%Y-%m-%d %I:%M:%S')
    logging.getLogger("ja_selenium").setLevel(logging.DEBUG)
    logging.root.handlers[0].setFormatter(NotTooLongStringFormatter(fmt))

    with open(config) as fp:
        actions = json.load(fp)
        ja_selenium = JaSelenium()
        ja_selenium.set_actions(actions)
        ja_selenium.start()


app = typer.Typer()
app.command()(main)

if __name__ == "__main__":
    app()
