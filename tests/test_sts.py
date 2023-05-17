from ehealth.sts import FakeSTSService, STSService, KeyStoreException, SoapFaultException
from ehealth.mda import MDAService
from pathlib import Path
import os
import pytest
import logging

logger = logging.getLogger(__name__)
KEYSTORE_PASSPHRASE = os.environ.get("KEYSTORE_PASSPHRASE")
KEYSTORE_SSIN = os.environ.get("KEYSTORE_SSIN")
TEST_DATA_FOLDER = Path(__file__).parent.joinpath("data")

def service():
    return STSService()

def fake_service():
    return FakeSTSService()

@pytest.mark.parametrize(
    "sts_service", [service(), fake_service()]
)
def test_sts__valid_certificate(sts_service):
    path = TEST_DATA_FOLDER.joinpath("valid.acc-p12")
    token = sts_service.get_serialized_token(str(path), KEYSTORE_PASSPHRASE, KEYSTORE_SSIN)
    with sts_service.session(token, str(path), KEYSTORE_PASSPHRASE) as session:
        pass # logger.info(token)

@pytest.mark.parametrize(
    "sts_service", [service(), fake_service()]
)
def test_sts__empty_password(sts_service):
    path = TEST_DATA_FOLDER.joinpath("valid.acc-p12")
    with pytest.raises(KeyStoreException):
        sts_service.get_serialized_token(str(path), "", KEYSTORE_SSIN)

@pytest.mark.parametrize(
    "service", [service(), fake_service()]
)
def test_sts__invalid_password(service):
    path = TEST_DATA_FOLDER.joinpath("valid.acc-p12")
    with pytest.raises(KeyStoreException):
        service.get_serialized_token(str(path), "invalid", KEYSTORE_SSIN)

@pytest.mark.parametrize(
    "sts_service", [service(), fake_service()]
)  
def test_sts__not_a_certificate_password(sts_service):
    path = Path(__file__)
    with pytest.raises(KeyStoreException):
        sts_service.get_serialized_token(str(path), KEYSTORE_PASSPHRASE, KEYSTORE_SSIN)


def test_sts__not_an_acc_certificate():
    sts_service = service()
    path = TEST_DATA_FOLDER.joinpath("invalid.p12")
    with pytest.raises(SoapFaultException):
        sts_service.get_serialized_token(str(path), KEYSTORE_PASSPHRASE, KEYSTORE_SSIN)

def test_sts__bad_endpoint():
    path = TEST_DATA_FOLDER.joinpath("valid.acc-p12")
    sts_service = STSService(sts_endpoint="$uddi{uddi:ehealth-fgov-be:business:etkdepot:v1}")
    with pytest.raises(SoapFaultException):
        sts_service.get_serialized_token(str(path), KEYSTORE_PASSPHRASE, KEYSTORE_SSIN)

