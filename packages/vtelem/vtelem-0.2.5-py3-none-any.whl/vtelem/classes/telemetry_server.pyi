from .channel_group_registry import ChannelGroupRegistry as ChannelGroupRegistry
from .command_queue_daemon import CommandQueueDaemon as CommandQueueDaemon
from .daemon import Daemon as Daemon
from .daemon_base import DaemonOperation as DaemonOperation
from .daemon_manager import DaemonManager as DaemonManager
from .http_daemon import HttpDaemon as HttpDaemon
from .http_request_mapper import MapperAwareRequestHandler as MapperAwareRequestHandler
from .service_registry import ServiceRegistry as ServiceRegistry
from .stream_writer import StreamWriter as StreamWriter
from .telemetry_daemon import TelemetryDaemon as TelemetryDaemon
from .time_keeper import TimeKeeper as TimeKeeper
from .udp_client_manager import UdpClientManager as UdpClientManager
from .websocket_telemetry_daemon import WebsocketTelemetryDaemon as WebsocketTelemetryDaemon
from typing import Any, Iterator, Tuple
from vtelem.factories.daemon_manager import create_daemon_manager_commander as create_daemon_manager_commander
from vtelem.factories.telemetry_environment import create_channel_commander as create_channel_commander
from vtelem.factories.telemetry_server import register_http_handlers as register_http_handlers
from vtelem.factories.udp_client_manager import create_udp_client_commander as create_udp_client_commander
from vtelem.factories.websocket_daemon import commandable_websocket_daemon as commandable_websocket_daemon
from vtelem.mtu import DEFAULT_MTU as DEFAULT_MTU, discover_ipv4_mtu as discover_ipv4_mtu
from vtelem.types.telemetry_server import AppLoop as AppLoop, AppSetup as AppSetup

class TelemetryServer(HttpDaemon):
    daemons: Any
    state_sem: Any
    first_start: bool
    time_keeper: Any
    channel_groups: Any
    udp_clients: Any
    def __init__(self, tick_length: float, telem_rate: float, http_address: Tuple[str, int] = ..., metrics_rate: float = ..., app_id_basis: float = ..., websocket_cmd_address: Tuple[str, int] = ..., websocket_tlm_address: Tuple[str, int] = ...) -> None: ...
    def register_application(self, name: str, rate: float, setup: AppSetup, loop: AppLoop) -> bool: ...
    def scale_speed(self, scalar: float) -> None: ...
    def start_all(self) -> None: ...
    def stop_all(self) -> None: ...
    def booted(self, *_, **__) -> Iterator[None]: ...
    def await_shutdown(self, timeout: float = ...) -> None: ...
