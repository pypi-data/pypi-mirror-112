from enum import Enum

class Region(Enum):
    US: str
    EU: str
    KR: str
    TW: str
    CN: str

class Locale(Enum):
    en_US: str
    es_MX: str
    pt_BR: str
    en_GB: str
    es_ES: str
    fr_FR: str
    ru_RU: str
    de_DE: str
    pt_PT: str
    it_IT: str
    ko_KR: str
    zh_TW: str
    zh_CN: str

class Namespace(Enum):
    Static: str
    Dynamic: str
    Profile: str

def get_query_str(region: Region, query_str: str) -> str: ...
def get_namespace_str(namespace: Namespace, region: Region): ...

class IconSize(Enum):
    SMALL: int
    MEDIUM: int
    LARGE: int

def get_icon_url(name: str, size: IconSize): ...
