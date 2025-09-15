import pytest
import requests
import logging
from ehealth.therlink.therlink import TherLinkService, TherLinkPatient
from typing import Any

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
def therlink_service():
    return TherLinkService(
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


def test_post_therlink(sts_service, token, therlink_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        p = TherLinkPatient(
            firstname="Pieter",
            lastname="Blomme",
            ssin="90060421941"
        )
        content_encoded = therlink_service.create_therlink_content(token, p)

        response = requests.post("http://localhost:8099/certificate", json={"data": content_encoded})
        print(f"response {response.content} of type {type(response.content)}")
        if response.status_code != 200:
            raise Exception(response.content)
    
        p.signed_encoded = response.content
        therlink_service.post_therlink(token, p)

def test_post_therlink_eidnumber(sts_service, token, therlink_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        p = TherLinkPatient(
            firstname="Mona",
            lastname="Blomme",
            ssin="24061608411",
            eidnumber="615136039755"
        )
        therlink_service.post_therlink(token, p)

def test_has_therlink(sts_service, token, therlink_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        p = TherLinkPatient(
            firstname="Mona",
            lastname="Blomme",
            ssin="24061608411",
        )
        result = therlink_service.has_therlink(token, p)
        print(result)


def test_revoke_therlink_eidnumber(sts_service, token, therlink_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        p = TherLinkPatient(
            firstname="Mona",
            lastname="Blomme",
            ssin="24061608411",
            eidnumber="615136039755"
        )
        therlink_service.revoke_therlink(token, p)

def test_get_therlink_eidnumber(sts_service, token, therlink_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        p = TherLinkPatient(
            firstname="Mona",
            lastname="Blomme",
            ssin="24061608411",
            eidnumber="615136039755"
        )
        therlink_service.get_therlink(token, p)
