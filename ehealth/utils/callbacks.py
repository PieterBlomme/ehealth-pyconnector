from typing import Optional
from pydantic import BaseModel
from enum import Enum
import logging
import datetime

logger = logging.getLogger(__name__)

class ServiceType(str, Enum):
    MDA = "mda"

class CallType(str, Enum):
    UNENCRYPTED_REQUEST = "UNENCRYPTED_REQUEST"
    ENCRYPTED_REQUEST = "ENCRYPTED_REQUEST"
    UNENCRYPTED_RESPONSE = "UNENCRYPTED_RESPONSE"
    ENCRYPTED_RESPONSE = "ENCRYPTED_RESPONSE"

class CallMetadata(BaseModel):
    timestamp: datetime.datetime
    type: ServiceType
    call_type: CallType
    ssin: Optional[str] = None
    registrationNumber: Optional[str] = None
    mutuality: Optional[str] = None

def storage_callback(
    content: str,
    meta: CallMetadata
):
    # This is a dummy implementation
    logger.info(f"Received content: {content}")
    logger.info(f"Received metadata: {meta.json()}")