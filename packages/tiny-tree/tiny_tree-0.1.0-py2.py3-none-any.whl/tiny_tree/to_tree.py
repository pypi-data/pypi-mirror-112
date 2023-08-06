from typing import List, Callable, Union

from .util import default_to

ROOT_ID = "__ROOT__"


def to_tree(data: List[dict], **kwargs) -> List[dict]:
    """
    行转树

    ```python
    to_tree([
      { "id": 1, "title": "item 1" },
      { "id": 2 "parentId": 1, "title": "item 1-1" }
    ])
    # [
    #   {
    #     "id": 1,
    #     "title": "item 1",
    #     "children": [
    #       {"id": 2, "parentId": 1, "title": "item 1-1", "children": []}
    #     ]
    #   },
    # ]
    ```
    """
    root = kwargs.pop('root', ROOT_ID)

    return exporter(transform(data, **kwargs), root)


def transform(
    data: List[dict],
    id_key: str = 'id',
    parent_key: str = 'parentId',
    child_key: str = 'children',
    transform: Callable[[dict, int], Union[dict, None]] = lambda row, _: row,
    insert: Callable[[List, dict],
                     None] = lambda siblings, node: siblings.append(node)
) -> dict:
    """
    转成成节点树对象，key 是 id，value 其所有子级(含子孙级)节点

    ```python
    transform([
      { "id": 1, "title": "item 1" },
      { "id": 2 "parentId": 1, "title": "item 1-1" }
    ])
    # {
    #    "1": [
    #      {"id": 2, "parentId": 1, "title": "item 1-1", "children": []}
    #    ],
    #    "__ROOT__": [
    #      {
    #        "id": 1,
    #        "title": "item 1",
    #        "children": [
    #          {"id": 2, "parentId": 1, "title": "item 1-1", "children": []}
    #        ]
    #      },
    #      "2": []
    #   ]
    # }
    ```
    """
    result = {}

    for i in range(len(data)):
        row: dict = data[i]

        # id 必须存在
        assert id_key in row, "id is required, in {} rows.".format(i)

        # 数据预处理
        node = transform(row, i)

        # 支持跳过某些数据
        if node is None:
            continue

        # 解决父节点挂载延迟的问题
        node[child_key] = result.setdefault(row[id_key], [])

        # 不能使用 get 函数的默认值，会保留 None
        # 不能使用 or，因为 0 也会被排除
        parent_id = default_to(row.get(parent_key), ROOT_ID)

        # 插入数据
        if parent_id in result:
            insert(result[parent_id], node)
        else:
            insert(result.setdefault(parent_id, []), node)

    return result


def exporter(result: dict, root: Union[str, Callable[[dict], Union[List[dict], None]]]) -> List[dict]:
    """
    从结果中导出数据

    ```python
    # 支持 key
    exporter({ "0": [1] }, "0") # output: [1]

    # 支持函数
    exporter({ "0": [1] }, lambda x: x["0"]) # output: [1]
    ```
    """
    return root(result) if hasattr(root, "__call__") else result.get(root)
