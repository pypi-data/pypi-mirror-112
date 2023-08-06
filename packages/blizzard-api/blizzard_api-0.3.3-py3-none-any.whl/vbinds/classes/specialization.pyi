from .engine import Engine as Engine
from .talent import Talent as Talent
from typing import Any, List, Optional, Tuple

def level_to_index(level: int) -> int: ...
def is_talent_active(talent_data: dict) -> bool: ...
def build_row_macro(row_idx: int, row_data: dict) -> Optional[Tuple[str, List[str]]]: ...

class Specialization:
    engine: Any
    data: Any
    talent_rows: Any
    levels: Any
    macros: Any
    name: Any
    to_serialize: Any
    def __init__(self, engine: Engine, spec_id: int) -> None: ...
    def role(self) -> str: ...
