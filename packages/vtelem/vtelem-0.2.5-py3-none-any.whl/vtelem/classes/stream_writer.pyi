from .channel_frame import ChannelFrame as ChannelFrame
from .queue_daemon import QueueDaemon as QueueDaemon
from io import BytesIO
from queue import Queue
from typing import Any, Callable

LOG: Any

class StreamWriter(QueueDaemon):
    curr_id: int
    queue_id: int
    streams: Any
    queues: Any
    error_handle: Any
    def __init__(self, name: str, frame_queue: Queue, error_handle: Callable[[int], None] = ...) -> None: ...
    def add_queue(self, queue: Queue) -> int: ...
    def add_stream(self, stream: BytesIO) -> int: ...
    def remove_stream(self, stream_id: int) -> bool: ...
    def remove_queue(self, queue_id: int, inject_none: bool = ...) -> bool: ...
