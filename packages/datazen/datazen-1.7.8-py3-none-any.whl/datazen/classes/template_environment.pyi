import jinja2
from datazen import ROOT_NAMESPACE as ROOT_NAMESPACE
from datazen.classes.base_environment import BaseEnvironment as BaseEnvironment, LOADTYPE as LOADTYPE
from datazen.enums import DataType as DataType
from typing import Dict, List

class TemplateEnvironment(BaseEnvironment):
    def load_templates(self, template_loads: LOADTYPE = ..., name: str = ...) -> Dict[str, jinja2.Template]: ...
    def add_template_dirs(self, dir_paths: List[str], rel_path: str = ..., name: str = ..., allow_dup: bool = ...) -> int: ...
