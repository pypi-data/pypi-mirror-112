from . import ID_ENV_KEY as ID_ENV_KEY, SECRET_ENV_KEY as SECRET_ENV_KEY
from .cache import Cache as Cache
from typing import Any, Optional
from vbinds.enums import Region as Region

class TokenEngine:
    log: Any
    token_server: str
    cache: Any
    region: Any
    def __init__(self, cache: Cache, region: Region = ...) -> None: ...
    def get_token(self) -> Optional[str]: ...
    def get_credentials(self) -> Optional[dict]: ...
    def set_credentials(self, client_id, client_secret, write_cache: bool = ...): ...
