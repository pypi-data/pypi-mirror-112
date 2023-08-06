from . import EventType as EventType
from .event_queue import EventQueue as EventQueue
from .type_primitive import TypePrimitive as TypePrimitive
from json import JSONEncoder
from typing import Any, Optional
from vtelem.enums.primitive import Primitive as Primitive

class Channel(TypePrimitive):
    name: Any
    rate: Any
    commandable: Any
    last_emitted: Any
    def __init__(self, name: str, instance: Primitive, rate: float, event_queue: EventQueue = ..., commandable: bool = ...) -> None: ...
    def command(self, value: Any, time: float = ..., add: bool = ...) -> bool: ...
    def set_rate(self, rate: float) -> None: ...
    def emit(self, time: float) -> Optional[Any]: ...

class ChannelEncoder(JSONEncoder):
    def default(self, o) -> dict: ...
