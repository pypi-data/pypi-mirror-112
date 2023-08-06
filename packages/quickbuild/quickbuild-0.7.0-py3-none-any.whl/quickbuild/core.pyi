from quickbuild.endpoints import Agents as Agents, Audits as Audits, Builds as Builds, Configurations as Configurations, Dashboards as Dashboards, Groups as Groups, Memberships as Memberships, Requests as Requests, System as System, Tokens as Tokens, Users as Users
from quickbuild.exceptions import QBError as QBError, QBForbiddenError as QBForbiddenError, QBNotFoundError as QBNotFoundError, QBProcessingError as QBProcessingError, QBServerError as QBServerError
from quickbuild.helpers import ContentType as ContentType
from typing import Any, NamedTuple, Optional

CONTENT_JSON: str

class Response(NamedTuple):
    status: Any
    headers: Any
    body: Any

class QuickBuild:
    agents: Any
    audits: Any
    builds: Any
    configurations: Any
    dashboards: Any
    groups: Any
    memberships: Any
    requests: Any
    system: Any
    tokens: Any
    users: Any
    def __init__(self, content_type: Optional[ContentType]) -> None: ...
