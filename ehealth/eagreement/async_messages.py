from pydantic.dataclasses import dataclass
from pydantic import Extra
from typing import Optional


class Config:
    extra = Extra.forbid

@dataclass(config=Config)
class Response:
    response: Optional[str]
    transaction_request: str
    transaction_response: str
    soap_request: str
    soap_response: str