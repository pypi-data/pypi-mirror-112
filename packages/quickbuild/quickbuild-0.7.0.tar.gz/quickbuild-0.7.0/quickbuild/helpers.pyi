from enum import Enum
from typing import Any

class ContentType(Enum):
    PARSE: int
    XML: int
    JSON: int

def response2py(obj: Any, content_type: ContentType) -> Any: ...
