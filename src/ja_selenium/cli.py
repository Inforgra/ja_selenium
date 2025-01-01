import json
import typer
from typing_extensions import Annotated
from .ja_selenium import createDriver
from .ja_selenium import runner

def main(
        config: Annotated[str, typer.Argument(help="actions json")] = None,
):
    with open(config) as fp:
        actions = json.load(fp)
        driver = createDriver()
        runner(driver)(actions)
        driver.close()

app = typer.Typer()
app.command()(main)

if __name__ == "__main__":
    app()
