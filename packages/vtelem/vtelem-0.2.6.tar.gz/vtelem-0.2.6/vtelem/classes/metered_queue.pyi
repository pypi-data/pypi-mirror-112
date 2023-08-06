from queue import Queue
from typing import Any
from vtelem.enums.primitive import Primitive as Primitive

class MeteredQueue(Queue):
    env: Any
    name: Any
    def __init__(self, name: str, env: Any, maxsize: int = ...) -> None: ...
    def get(self, block: bool = ..., timeout: float = ...) -> Any: ...
    def put(self, item: Any, block: bool = ..., timeout: float = ...) -> None: ...
