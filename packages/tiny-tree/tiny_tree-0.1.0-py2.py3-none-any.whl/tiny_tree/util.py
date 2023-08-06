from typing import Callable, Any, List


Predicate = Callable[[Any, int, List[Any]], Any]


def find_index(list: List[Any], predicate: Predicate) -> int:
    """
    参考 js 的 Array#findIndex 方法

    ```python
    data = [{ "name": "foo" }, { "name": "bar" }]

    find_index(data, lambda value, index, array: value.get('name') == 'bar')
    # output: 1
    ```
    """
    for index in range(len(list)):
        if predicate(list[index], index, list):
            return index

    return -1


def default_to(value, default_value):
    return default_value if value is None else value
