from datazen.classes.task_environment import TaskEnvironment as TaskEnvironment, get_path as get_path
from typing import Any, List, Tuple

LOG: Any

class CommandEnvironment(TaskEnvironment):
    def __init__(self) -> None: ...
    def valid_command(self, entry: dict, _: str, __: dict = ..., deps_changed: List[str] = ...) -> Tuple[bool, bool]: ...
