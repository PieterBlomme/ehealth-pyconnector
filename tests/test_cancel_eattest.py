import os
import datetime
import pytest
import logging
from pathlib import Path
from ehealth.sts import STSService
from ehealth.eattestv3.eattest import EAttestV3Service
from ehealth.eattestv3.input_models import CancelEAttestInputModel, Patient, Transaction, CGDItem, Requestor, Location
from ehealth.utils.callbacks import file_callback
from ehealth.eattestv3.exceptions import EAttestRetryableAttempt, TechnicalEAttestException
from .conftest import MYCARENET_PWD, MYCARENET_USER

logger = logging.getLogger(__name__)

KEYSTORE_PASSPHRASE = os.environ.get("KEYSTORE_PASSPHRASE")
KEYSTORE_SSIN = "90121320026"
KEYSTORE_PATH = "valid-eattest.acc-p12"
DATA_FOLDER = Path(__file__).parent.joinpath("data/faked_eagreement")

@pytest.fixture
def sts_service():
    return STSService()

@pytest.fixture()
def token(sts_service):
    return sts_service.get_serialized_token(KEYSTORE_PATH, KEYSTORE_PASSPHRASE, KEYSTORE_SSIN)

@pytest.fixture
def eattest_service():
    return EAttestV3Service(
        mycarenet_license_username=MYCARENET_USER,
        mycarenet_license_password=MYCARENET_PWD,
    )

def test_4_1_1(sts_service, token, eattest_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eattest_service.cancel_attestation(
            token, 
            input_model=CancelEAttestInputModel(
                patient=Patient(
                    givenname="John",
                    surname="Doe",
                    gender="male",
                    ssin="68042000773"
                ),
                invoice_number="940-1-240130-0000001-84",
                reason="C"
            ),
            callback_fn=file_callback
        )
    
    logger.info(response.soap_request)

def test_retryable(sts_service, token, eattest_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        with pytest.raises(TechnicalEAttestException) as exc_info:
            response = eattest_service.cancel_attestation(
                token, 
                input_model=CancelEAttestInputModel(
                    patient=Patient(
                        givenname="John",
                        surname="Doe",
                        gender="male",
                        ssin="68042000773"
                    ),
                    invoice_number="940-1-240130-0000001-84",
                    reason="C",
                    force_retryable=True
                ),
                callback_fn=file_callback,
            )

        retryable = exc_info.value.retryable
        response = eattest_service.retry_cancel_attestation(
            token=token,
            input_model=retryable,
            callback_fn=file_callback
        )
    logger.info(response.soap_request)