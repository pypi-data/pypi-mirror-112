from . import METRIC_PRIM as METRIC_PRIM
from .channel_group import ChannelGroup as ChannelGroup
from .telemetry_environment import TelemetryEnvironment as TelemetryEnvironment
from typing import Any, Callable

class State:
    name: Any
    run_fn: Any
    entering_fn: Any
    leaving_fn: Any
    metrics: Any
    is_initial_state: bool
    def __init__(self, name: str, run: Callable = ..., entering: Callable = ..., leaving: Callable = ..., env: TelemetryEnvironment = ..., rate: float = ...) -> None: ...
    def __eq__(self, other) -> bool: ...
    def entering(self, prev_state_name: str, data: dict) -> bool: ...
    def run(self, data: dict) -> str: ...
    def leaving(self, next_state_name: str, data: dict) -> bool: ...
