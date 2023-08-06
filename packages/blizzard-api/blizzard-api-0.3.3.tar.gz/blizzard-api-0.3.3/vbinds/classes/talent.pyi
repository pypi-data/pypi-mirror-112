from .engine import Engine as Engine
from typing import Any

class Spell:
    engine: Any
    data: Any
    media: Any
    to_serialize: Any
    def __init__(self, engine: Engine, spell_id: int) -> None: ...
    def name(self) -> str: ...

class Talent:
    engine: Any
    data: Any
    spell: Any
    to_serialize: Any
    def __init__(self, engine: Engine, talent_id: int) -> None: ...
    def name(self) -> str: ...
