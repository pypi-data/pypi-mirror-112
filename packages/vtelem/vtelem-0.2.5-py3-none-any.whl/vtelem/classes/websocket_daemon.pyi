from .event_loop_daemon import EventLoopDaemon as EventLoopDaemon
from .service_registry import ServiceRegistry as ServiceRegistry
from .telemetry_environment import TelemetryEnvironment as TelemetryEnvironment
from typing import Any, Callable, Optional, Tuple

LOG: Any

def create_default_handler(message_consumer: Callable) -> Callable: ...

class WebsocketDaemon(EventLoopDaemon):
    address: Any
    server: Any
    serving: bool
    def __init__(self, name: str, message_consumer: Optional[Callable], address: Tuple[str, int] = ..., env: TelemetryEnvironment = ..., time_keeper: Any = ..., ws_handler: Callable = ...) -> None: ...
