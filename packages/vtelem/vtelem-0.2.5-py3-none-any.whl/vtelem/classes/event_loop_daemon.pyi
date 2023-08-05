from .daemon_base import DaemonBase as DaemonBase
from .telemetry_environment import TelemetryEnvironment as TelemetryEnvironment
from typing import Any

class EventLoopDaemon(DaemonBase):
    eloop: Any
    wait_count: int
    wait_poster: Any
    def __init__(self, name: str, env: TelemetryEnvironment = ..., time_keeper: Any = ...) -> None: ...
    def run(self, *args, **kwargs) -> None: ...
