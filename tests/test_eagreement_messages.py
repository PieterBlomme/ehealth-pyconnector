import os
import pytest
import logging
from pathlib import Path
from ehealth.eagreement import EAgreementService

logger = logging.getLogger(__name__)

KEYSTORE_PASSPHRASE = os.environ.get("KEYSTORE_PASSPHRASE")
KEYSTORE_SSIN = os.environ.get("KEYSTORE_SSIN")
KEYSTORE_PATH = "valid.acc-p12"
DATA_FOLDER = Path(__file__).parent.joinpath("data/faked_eagreement")
MYCARENET_USER = os.environ.get("MYCARENET_USER")
MYCARENET_PWD = os.environ.get("MYCARENET_PWD")

@pytest.fixture
def eagreement_service():
    return EAgreementService(
        mycarenet_license_username=MYCARENET_USER,
        mycarenet_license_password=MYCARENET_PWD,
    )


def test__6_1_7(sts_service, token, eagreement_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        responses_async = eagreement_service.async_messages(token)
        eagreement_service.confirm_message(token, "281ec963-d7e3-4bff-a35d-be60af5f3352")
        responses_async = eagreement_service.async_messages(token)
