import pytest
import requests
import logging
from typing import Any

from ehealth.ehbox.ehbox import EHBoxService

logger = logging.getLogger(__name__)

KEYSTORE_PASSPHRASE = "Destroyer666"
KEYSTORE_SSIN = "90060421941"
KEYSTORE_PATH = "valid.acc-p12"
MYCARENET_USER = "kinblomme"
MYCARENET_PWD = "4zlAyn4Gv"


@pytest.fixture()
def token(sts_service):
    return sts_service.get_serialized_token(KEYSTORE_PATH, KEYSTORE_PASSPHRASE, KEYSTORE_SSIN)


@pytest.fixture
def ehbox_service():
    return EHBoxService(
        mycarenet_license_username=MYCARENET_USER,
        mycarenet_license_password=MYCARENET_PWD,
    )

# def storage_callback(
#     content: bytes,
#     meta: Any,
# ):
#     if meta.ssin:
#         identification = meta.ssin
#     elif meta.efact_reference:
#         identification = meta.efact_reference
#     else:
#         identification = f"{meta.registrationNumber}@{meta.mutuality}"
#     filename = f"{meta.timestamp}_{str(meta.type.value)}_{str(meta.call_type.value)}_{identification}.xml"
#     # This is a dummy implementation
#     logger.info(f"Received content: {content} to be stored with filename {filename}")
#     with open(filename, "wb") as f:
#         f.write(content)


def test_get_messages(sts_service, token, ehbox_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        messages = ehbox_service.get_messages(token)
        for message in messages:
            logger.info(message)

def test_send_message(sts_service, token, ehbox_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        with open("/home/pieter/Downloads//dummy_1.pdf", "rb") as f:
            content = f.read()
        ehbox_service.send_message(
            token=token,
            id="90060421941",
            mimeType="application/pdf",
            filename="dummy_1.pdf",
            content=content,
            title="A message",
            quality_type="PHYSIOTHERAPIST_SSIN"
        )