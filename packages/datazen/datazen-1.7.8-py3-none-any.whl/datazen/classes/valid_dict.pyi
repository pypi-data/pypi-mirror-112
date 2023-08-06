from cerberus import Validator as Validator
from collections import UserDict
from typing import Any

LOG: Any

class ValidDict(UserDict):
    name: Any
    validator: Any
    valid: Any
    def __init__(self, name: str, data: dict, schema: Validator) -> None: ...
