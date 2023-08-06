from vtelem.classes.command_queue_daemon import CommandQueueDaemon as CommandQueueDaemon
from vtelem.classes.daemon_manager import DaemonManager as DaemonManager
from vtelem.enums.daemon import DaemonOperation as DaemonOperation, is_operation as is_operation, operation_str as operation_str
from vtelem.types.command_queue_daemon import ResultCbType as ResultCbType

def create_daemon_manager_commander(manager: DaemonManager, daemon: CommandQueueDaemon, result_cb: ResultCbType = ..., command_name: str = ...) -> None: ...
