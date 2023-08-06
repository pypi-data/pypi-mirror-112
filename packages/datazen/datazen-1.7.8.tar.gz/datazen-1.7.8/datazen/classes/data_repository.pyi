import git
from datazen.compile import write_dir as write_dir
from datazen.load import load_dir_only as load_dir_only
from datazen.parsing import merge as merge
from datazen.paths import EXCLUDES as EXCLUDES
from typing import Any, Iterator

LOG: Any

class DataRepository:
    root: Any
    out_type: Any
    repo: Any
    data: Any
    lock: Any
    def __init__(self, root_dir: str, out_type: str = ...) -> None: ...
    def meld(self, data: dict, root_rel: str = ..., expect_overwrite: bool = ...) -> Iterator[git.Repo]: ...
    def loaded(self, root_rel: str = ..., write_back: bool = ...) -> Iterator[dict]: ...
