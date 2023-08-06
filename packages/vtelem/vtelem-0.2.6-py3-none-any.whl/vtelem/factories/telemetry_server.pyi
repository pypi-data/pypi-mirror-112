from typing import Any
from vtelem.classes.command_queue_daemon import CommandQueueDaemon as CommandQueueDaemon
from vtelem.classes.telemetry_daemon import TelemetryDaemon as TelemetryDaemon

def register_http_handlers(server: Any, telem: TelemetryDaemon, cmd: CommandQueueDaemon) -> None: ...
