from datazen.classes.task_environment import TaskEnvironment as TaskEnvironment
from datazen.compile import get_compile_output as get_compile_output, str_compile as str_compile
from datazen.paths import advance_dict_by_path as advance_dict_by_path
from datazen.targets import resolve_dep_data as resolve_dep_data
from typing import Any, List, Tuple

LOG: Any

class CompileEnvironment(TaskEnvironment):
    def __init__(self) -> None: ...
    def valid_compile(self, entry: dict, namespace: str, dep_data: dict = ..., deps_changed: List[str] = ...) -> Tuple[bool, bool]: ...
