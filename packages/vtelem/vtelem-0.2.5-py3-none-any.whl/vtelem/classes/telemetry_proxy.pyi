from .daemon_base import DaemonBase as DaemonBase, DaemonState as DaemonState
from .telemetry_environment import TelemetryEnvironment as TelemetryEnvironment
from .type_primitive import TypePrimitive as TypePrimitive
from queue import Queue
from typing import Any, Tuple
from vtelem.mtu import DEFAULT_MTU as DEFAULT_MTU, create_udp_socket as create_udp_socket

LOG: Any

class TelemetryProxy(DaemonBase):
    socket: Any
    mtu: Any
    frames: Any
    expected_id: Any
    curr_id: Any
    def __init__(self, host: Tuple[str, int], output_stream: Queue, app_id: TypePrimitive, env: TelemetryEnvironment, mtu: int = ...) -> None: ...
    def update_mtu(self, new_mtu: int) -> None: ...
    def run(self, *_, **__) -> None: ...
