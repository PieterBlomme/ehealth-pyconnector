import os
import pytest
import logging
from pathlib import Path
from ehealth.sts import STSService
from ehealth.eagreement import EAgreementService, Patient

logger = logging.getLogger(__name__)

KEYSTORE_PASSPHRASE = os.environ.get("KEYSTORE_PASSPHRASE")
KEYSTORE_SSIN = "90060421941"
KEYSTORE_PATH = "valid.acc-p12"
DATA_FOLDER = Path(__file__).parent.joinpath("data/faked_eagreement")
MYCARENET_USER = os.environ.get("MYCARENET_USER")
MYCARENET_PWD = os.environ.get("MYCARENET_PWD")

@pytest.fixture
def sts_service():
    return STSService()


@pytest.fixture
def eagreement_service():
    return EAgreementService(
        mycarenet_license_username=MYCARENET_USER,
        mycarenet_license_password=MYCARENET_PWD,
    )

@pytest.fixture()
def token(sts_service):
    return sts_service.get_serialized_token(KEYSTORE_PATH, KEYSTORE_PASSPHRASE, KEYSTORE_SSIN)

def test__consult_with_io(sts_service, token, eagreement_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eagreement_service.consult_agreement(token,
            Patient(ssin=None, insurancymembership='0812814934608', insurancenumber='509', givenname='Fadel', surname='Farwi', gender='male')
        )
        logger.info(response)