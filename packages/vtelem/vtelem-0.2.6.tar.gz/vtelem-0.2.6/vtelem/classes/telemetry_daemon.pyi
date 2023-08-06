from .channel import Channel as Channel
from .daemon import Daemon as Daemon
from .telemetry_environment import TelemetryEnvironment as TelemetryEnvironment
from .time_keeper import TimeKeeper as TimeKeeper
from .user_enum import UserEnum as UserEnum
from typing import List

class TelemetryDaemon(TelemetryEnvironment, Daemon):
    def __init__(self, name: str, mtu: int, rate: float, time_keeper: TimeKeeper, metrics_rate: float = ..., initial_channels: List[Channel] = ..., initial_enums: List[UserEnum] = ..., app_id_basis: float = ...) -> None: ...
