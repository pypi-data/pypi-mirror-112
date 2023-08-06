from . import DEFAULT_CACHE as DEFAULT_CACHE
from .cache import Cache as Cache
from .class_data_engine import ClassDataEngine as ClassDataEngine
from .spec_data_engine import SpecDataEngine as SpecDataEngine

class Engine(ClassDataEngine, SpecDataEngine): ...

def engine_from_output_root(output_dir: str) -> Engine: ...
