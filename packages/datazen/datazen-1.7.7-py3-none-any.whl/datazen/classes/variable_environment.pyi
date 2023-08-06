from datazen import ROOT_NAMESPACE as ROOT_NAMESPACE
from datazen.classes.base_environment import BaseEnvironment as BaseEnvironment, LOADTYPE as LOADTYPE
from datazen.enums import DataType as DataType
from typing import List

class VariableEnvironment(BaseEnvironment):
    def load_variables(self, var_loads: LOADTYPE = ..., name: str = ...) -> dict: ...
    def add_variable_dirs(self, dir_paths: List[str], rel_path: str = ..., name: str = ..., allow_dup: bool = ...) -> int: ...
