from typing import Tuple
from vtelem.classes.command_queue_daemon import CommandQueueDaemon as CommandQueueDaemon
from vtelem.classes.telemetry_environment import TelemetryEnvironment as TelemetryEnvironment
from vtelem.classes.time_keeper import TimeKeeper as TimeKeeper
from vtelem.classes.websocket_daemon import WebsocketDaemon as WebsocketDaemon

def commandable_websocket_daemon(name: str, daemon: CommandQueueDaemon, address: Tuple[str, int] = ..., env: TelemetryEnvironment = ..., keeper: TimeKeeper = ...) -> WebsocketDaemon: ...
