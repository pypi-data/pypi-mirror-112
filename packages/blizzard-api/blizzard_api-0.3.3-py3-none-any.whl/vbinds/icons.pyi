from typing import Any, Optional
from vbinds.enums import IconSize as IconSize, get_icon_url as get_icon_url

LOG: Any

def get_icon(name: str, dest_root: str = ..., size: IconSize = ..., size_subdir: bool = ...) -> Optional[str]: ...
