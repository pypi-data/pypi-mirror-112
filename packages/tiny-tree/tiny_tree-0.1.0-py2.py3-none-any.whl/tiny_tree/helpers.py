from typing import Callable, Any, List, Union

from .util import find_index


def add_property(key: str, value: Any):
    def transform(row: dict, index: int) -> dict:
        row.setdefault(key, value)
        return row

    return transform


def sort_insert_with(compare: Callable[[dict, dict], Union[int, bool]]):
    def sort_insert(siblings: List[dict], node: dict) -> None:
        index = find_index(siblings, lambda row, *_: compare(node, row))
        if index == -1:
            siblings.append(node)
        else:
            siblings.insert(index, node)
    return sort_insert


def sort_insert(key: str):
    return sort_insert_with(lambda a, b: a[key] - b[key])
