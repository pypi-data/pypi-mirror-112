from .registry import Registry as Registry
from typing import List, Tuple

Service = List[Tuple[str, int]]

class ServiceRegistry(Registry[Service]):
    def __init__(self, initial_services: List[Tuple[str, Service]] = ...) -> None: ...
