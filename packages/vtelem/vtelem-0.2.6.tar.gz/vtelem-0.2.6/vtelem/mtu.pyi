import socket
from .classes.channel_framer import build_dummy_frame as build_dummy_frame
from enum import IntEnum
from typing import Any, Tuple

LOG: Any
DEFAULT_MTU: Any

class SocketConstants(IntEnum):
    IP_MTU: int
    IP_MTU_DISCOVER: int
    IP_PMTUDISC_DO: int

def create_udp_socket(host: Tuple[str, int], is_client: bool = ...) -> socket.SocketType: ...
def discover_mtu(sock: socket.SocketType, probe_size: int = ..., app_id_basis: float = ...) -> int: ...
def get_free_tcp_port(interface_ip: str = ...) -> int: ...
def discover_ipv4_mtu(host: Tuple[str, int], probe_size: int = ...) -> int: ...
