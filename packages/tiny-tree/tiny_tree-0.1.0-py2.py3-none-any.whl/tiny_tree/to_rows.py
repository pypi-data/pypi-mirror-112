from typing import List


def to_rows(data: List[dict], child_key: str = 'children') -> List[dict]:
    """
    树转行

    ```python
    to_rows([
      {
        "id": 1,
        "title": "item 1",
        "children": [{"id": 2, "parentId": 1, "title": "item 1-1", "children": []}]
      },
    ])
    # [
    #   { "id": 1, "title": "item 1" },
    #   { "id": 2 "parentId": 1, "title": "item 1-1" }
    # ]

    # 自定义子级属性
    to_rows(data, child_key="items")
    ```
    """
    result: List[dict] = []

    def foreach(data: List[dict]):
        for row in data:
            result.append(row)
            foreach(row.pop(child_key, []))

    foreach(data)

    return result
