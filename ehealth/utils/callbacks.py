from typing import Optional
from pydantic import BaseModel
from enum import Enum
import logging
import datetime

logger = logging.getLogger(__name__)

class ServiceType(str, Enum):
    MDA = "mda"
    ASK_EAGREEMENT = "ask_eagreement"
    ARGUE_EAGREEMENT = "argue_eagreement"
    CANCEL_EAGREEMENT = "cancel_eagreement"
    CONSULT_EAGREEMENT = "consult_eagreement"
    ASYNC_MESSAGES_EAGREEMENT = "async_messages_eagreement"
    EATTEST = "eattest"
    EFACT = "efact"
    CANCEL_EATTEST = "cancel_eattest"
    ASYNC_MESSAGES_EFACT = "async_messages_efact"


class CallType(str, Enum):
    UNENCRYPTED_REQUEST = "UNENCRYPTED_REQUEST"
    ENCRYPTED_REQUEST = "ENCRYPTED_REQUEST"
    UNENCRYPTED_RESPONSE = "UNENCRYPTED_RESPONSE"
    ENCRYPTED_RESPONSE = "ENCRYPTED_RESPONSE"
    XADES_RESPONSE = "XADES_RESPONSE"

class CallMetadata(BaseModel):
    timestamp: datetime.datetime
    type: ServiceType
    call_type: CallType
    ssin: Optional[str] = None
    registrationNumber: Optional[str] = None
    mutuality: Optional[str] = None

    def set_call_type(self, value: CallType):
        d = self.dict()
        d["call_type"] = value
        return CallMetadata(
            **d
        )

def storage_callback(
    content: str,
    meta: CallMetadata
):
    # This is a dummy implementation
    logger.info(type(content))
    logger.info(f"Received content: {content}")
    logger.info(f"Received metadata: {meta.json()}")

def file_callback(
    content: str,
    meta: CallMetadata
):
    with open(f"{meta.ssin}_{meta.registrationNumber}_{meta.type}_{meta.call_type}.xml", "w") as f:
        f.write(content)