from typing import Any, Callable, Dict
from vtelem.classes.channel_group_registry import ChannelGroupRegistry as ChannelGroupRegistry

AppSetup = Callable[[ChannelGroupRegistry, Dict[str, Any]], None]
AppLoop = Callable[[ChannelGroupRegistry, Dict[str, Any]], None]
