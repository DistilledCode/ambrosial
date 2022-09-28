from json import JSONDecodeError, dump, load
from pathlib import Path

from msgpack import pack, unpack


def savej(fp: Path, orders: list[dict]) -> None:
    curr_ids = {order["order_id"] for order in orders}
    try:
        with open(fp, "r", encoding="utf-8") as f:
            loaded = load(f)
            loaded_ids = {order["order_id"] for order in loaded}
    except (JSONDecodeError, FileNotFoundError):
        with open(fp, "w", encoding="utf-8") as f:
            dump(orders, f, indent=4)
    else:
        if diff := curr_ids.difference(loaded_ids):
            loaded.extend([i for i in orders if i["order_id"] in diff])
        with open(fp, "w", encoding="utf-8") as f:
            dump(loaded, f, indent=4)


def loadj(fp: Path) -> list[dict]:
    with open(fp, "r", encoding="utf-8") as f:
        return load(f)


def saveb(fp: Path, orders: list[dict]) -> None:
    curr_ids = {order["order_id"] for order in orders}
    try:
        with open(fp, "rb") as f:
            loaded = unpack(f)
            loaded_ids = {order["order_id"] for order in loaded}
    except (ValueError, FileNotFoundError):
        with open(fp, "wb") as f:
            pack(orders, f)
    else:
        if diff := curr_ids.difference(loaded_ids):
            loaded.extend([i for i in orders if i["order_id"] in diff])
        with open(fp, "wb") as f:
            pack(orders, f)


def loadb(fp: Path) -> list[dict]:
    with open(fp, "rb") as f:
        return unpack(f)
