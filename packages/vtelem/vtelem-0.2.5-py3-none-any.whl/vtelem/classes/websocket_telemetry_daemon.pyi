from .channel_frame import ChannelFrame as ChannelFrame
from .stream_writer import StreamWriter as StreamWriter
from .telemetry_environment import TelemetryEnvironment as TelemetryEnvironment
from .websocket_daemon import WebsocketDaemon as WebsocketDaemon
from typing import Any, Tuple

class WebsocketTelemetryDaemon(WebsocketDaemon):
    def __init__(self, name: str, writer: StreamWriter, address: Tuple[str, int] = ..., env: TelemetryEnvironment = ..., time_keeper: Any = ...) -> None: ...
