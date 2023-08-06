from .engine import Engine as Engine
from .specialization import Specialization as Specialization
from typing import Any, Dict, List

class PlayableClass:
    engine: Any
    data: Any
    media: Any
    icon: Any
    name: Any
    to_serialize: Any
    specs: Any
    def __init__(self, engine: Engine, class_id: int) -> None: ...
    def roles(self) -> List[str]: ...
    def macros(self) -> Dict[str, List[str]]: ...

def get_classes(engine: Engine) -> Dict[str, PlayableClass]: ...
