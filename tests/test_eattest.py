from ehealth.eagreement import AskAgreementInputModel, Patient, Practitioner, ClaimAsk, Prescription, Attachment, EAgreementService
from xsdata.models.datatype import XmlDate
import os
import datetime
import pytest
import logging
from pathlib import Path
from ehealth.eattestv3.eattest import EAttestV3Service
from .conftest import MYCARENET_PWD, MYCARENET_USER

logger = logging.getLogger(__name__)

KEYSTORE_PASSPHRASE = os.environ.get("KEYSTORE_PASSPHRASE")
KEYSTORE_SSIN = os.environ.get("KEYSTORE_SSIN")
KEYSTORE_PATH = "valid.acc-p12"
DATA_FOLDER = Path(__file__).parent.joinpath("data/faked_eagreement")

@pytest.fixture
def eattest_service():
    return EAttestV3Service(
        mycarenet_license_username=MYCARENET_USER,
        mycarenet_license_password=MYCARENET_PWD,
    )

def test_happy_path(sts_service, token, eattest_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eattest_service.send_attestation(token)