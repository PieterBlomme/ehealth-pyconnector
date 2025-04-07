import pytest
import logging
from ehealth.efact.efact import EFactService
from typing import Any

logger = logging.getLogger(__name__)

KEYSTORE_PASSPHRASE = "Destroyer666"
KEYSTORE_SSIN = "90121320026"
KEYSTORE_PATH = "valid-eattest.acc-p12"
MYCARENET_USER = "kinblomme"
MYCARENET_PWD = "4zlAyn4Gv"


@pytest.fixture()
def token(sts_service):
    return sts_service.get_serialized_token(KEYSTORE_PATH, KEYSTORE_PASSPHRASE, KEYSTORE_SSIN)


@pytest.fixture
def efact_service():
    return EFactService(
        mycarenet_license_username=MYCARENET_USER,
        mycarenet_license_password=MYCARENET_PWD,
    )

def storage_callback(
    content: bytes,
    meta: Any,
):
    if meta.ssin:
        identification = meta.ssin
    elif meta.efact_reference:
        identification = meta.efact_reference
    else:
        identification = f"{meta.registrationNumber}@{meta.mutuality}"
    filename = f"{meta.timestamp}_{str(meta.type.value)}_{str(meta.call_type.value)}_{identification}.xml"
    # This is a dummy implementation
    logger.info(f"Received content: {content} to be stored with filename {filename}")
    with open(filename, "wb") as f:
        f.write(content)


def test_confirm_message(sts_service, token, efact_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        messages = efact_service.get_messages(token, callback_fn=storage_callback)
        logger.info(f"num messages: {len(messages)}")
        for m in messages:
            logger.info(m.message.base64_hash)
            logger.info(m.message.reference)