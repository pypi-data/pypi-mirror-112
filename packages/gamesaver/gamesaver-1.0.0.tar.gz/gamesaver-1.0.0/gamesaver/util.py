from .config import stores_uri
import requests


def get_store(id: int) -> str:
    store = ""
    req = requests.get(stores_uri)
    res = req.json()
    for obj in res:
        if id == obj["storeID"]:
            store = obj["storeName"]

    return store
