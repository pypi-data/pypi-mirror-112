import argparse
from vbinds.classes.engine import engine_from_output_root as engine_from_output_root
from vbinds.classes.icon_cache import IconCache as IconCache
from vbinds.classes.playable_class import get_classes as get_classes

def entry(args: argparse.Namespace) -> int: ...
def add_app_args(parser: argparse.ArgumentParser) -> None: ...
