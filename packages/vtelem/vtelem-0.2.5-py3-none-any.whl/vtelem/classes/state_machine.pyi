from . import METRIC_PRIM as METRIC_PRIM
from .channel_group import ChannelGroup as ChannelGroup
from .state import State as State
from .telemetry_environment import TelemetryEnvironment as TelemetryEnvironment
from .time_entity import LockEntity as LockEntity
from typing import Any, Iterator, List, Tuple

LOG: Any

class StateMachine(LockEntity):
    states: Any
    current_state: Any
    name: Any
    metrics: Any
    def __init__(self, name: str, states: List[State], initial_state: State = ..., initial_data: dict = ..., env: TelemetryEnvironment = ..., rate: float = ...) -> None: ...
    def data(self) -> Iterator[dict]: ...
    def run(self, new_data: dict = ...) -> Tuple[State, State]: ...
