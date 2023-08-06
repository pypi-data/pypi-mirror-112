from .stream_writer import StreamWriter as StreamWriter
from .time_entity import LockEntity as LockEntity
from typing import Any, Tuple
from vtelem.mtu import create_udp_socket as create_udp_socket, discover_mtu as discover_mtu

LOG: Any

class UdpClientManager(LockEntity):
    writer: Any
    clients: Any
    stream_ids: Any
    closer: Any
    def __init__(self, writer: StreamWriter) -> None: ...
    def client_name(self, sock_id: int) -> Tuple[str, int]: ...
    def add_client(self, host: Tuple[str, int]) -> Tuple[int, int]: ...
    def remove_all(self) -> None: ...
    def remove_client(self, sock_id: int) -> None: ...
