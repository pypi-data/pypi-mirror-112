from .daemon_base import DaemonBase as DaemonBase
from .telemetry_environment import TelemetryEnvironment as TelemetryEnvironment
from queue import Queue
from typing import Any, Callable

class QueueDaemon(DaemonBase):
    queue: Any
    handle: Any
    def __init__(self, name: str, input_stream: Queue, elem_handle: Callable, env: TelemetryEnvironment = ..., time_keeper: Any = ...) -> None: ...
    def run(self, *_, **__) -> None: ...
