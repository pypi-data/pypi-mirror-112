from .config import deals_uri
from .util import get_store
from .output import Table
from rich.progress import Progress
import requests


def search_deals(user_title: str, user_store: str) -> None:
    output = Table(show_header=True, header_style="bold magenta")

    req = requests.get(deals_uri)
    res = req.json()
    data = sorted(res, key=lambda k: k["title"])

    with Progress() as progress:
        task = progress.add_task("Finding Deals", total=len(data))
        for obj in data:
            progress.update(task, advance=1)
            title = obj["title"]
            if user_title != None and user_title.lower() != title.lower():
                continue
            store = get_store(obj["storeID"])
            if user_store != None and user_store.lower() != store.lower():
                continue
            output.table.add_row(title, store, obj["normalPrice"], obj["salePrice"])

    output.print()
