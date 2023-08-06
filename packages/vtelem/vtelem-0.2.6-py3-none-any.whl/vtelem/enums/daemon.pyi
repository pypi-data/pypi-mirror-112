from enum import IntEnum
from typing import Optional

class DaemonState(IntEnum):
    ERROR: int
    IDLE: int
    STARTING: int
    RUNNING: int
    PAUSED: int
    STOPPING: int

class DaemonOperation(IntEnum):
    NONE: int
    START: int
    STOP: int
    PAUSE: int
    UNPAUSE: int
    RESTART: int

def operation_str(operation: DaemonOperation) -> str: ...
def is_operation(operation: str) -> bool: ...
def str_to_operation(operation: str) -> Optional[DaemonOperation]: ...
