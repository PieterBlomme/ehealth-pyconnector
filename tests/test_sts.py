from ehealth.sts import FakeSTSService, STSService, KeyStoreException, SoapFaultException
from pathlib import Path
import os
import time
import random
import pytest
import logging
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

logger = logging.getLogger(__name__)
KEYSTORE_PASSPHRASE = os.environ.get("KEYSTORE_PASSPHRASE")
KEYSTORE_SSIN = os.environ.get("KEYSTORE_SSIN")

def service():
    return STSService()

def fake_service():
    return FakeSTSService()

@pytest.mark.parametrize(
    "sts_service", [service(), fake_service()]
)
def test_sts__valid_certificate(sts_service):
    cert = "valid.acc-p12"
    token = sts_service.get_serialized_token(cert, KEYSTORE_PASSPHRASE, KEYSTORE_SSIN)
    with sts_service.session(token, cert, KEYSTORE_PASSPHRASE) as session:
        pass # logger.info(token)

@pytest.mark.parametrize(
    "sts_service", [service(), fake_service()]
)
def test_sts__empty_password(sts_service):
    cert = "valid.acc-p12"
    with pytest.raises(KeyStoreException):
        sts_service.get_serialized_token(cert, "", KEYSTORE_SSIN)

@pytest.mark.parametrize(
    "service", [service(), fake_service()]
)
def test_sts__invalid_password(service):
    cert = "valid.acc-p12"
    with pytest.raises(KeyStoreException):
        service.get_serialized_token(cert, "invalid", KEYSTORE_SSIN)

@pytest.mark.parametrize(
    "sts_service", [service(), fake_service()]
)  
def test_sts__not_a_certificate_password(sts_service):
    bad_file = Path(__file__).name
    with pytest.raises(KeyStoreException):
        sts_service.get_serialized_token(bad_file, KEYSTORE_PASSPHRASE, KEYSTORE_SSIN)


def test_sts__not_an_acc_certificate():
    sts_service = service()
    cert = "invalid.p12"
    with pytest.raises(SoapFaultException):
        sts_service.get_serialized_token(cert, KEYSTORE_PASSPHRASE, KEYSTORE_SSIN)

def test_sts__bad_endpoint():
    cert = "valid.acc-p12"
    sts_service = STSService(sts_endpoint="$uddi{uddi:ehealth-fgov-be:business:etkdepot:v1}")
    with pytest.raises(SoapFaultException):
        sts_service.get_serialized_token(cert, KEYSTORE_PASSPHRASE, KEYSTORE_SSIN)


def task_set_random_config_value(uid):
    sts_service = STSService()
    token = sts_service.get_serialized_token("valid.acc-p12", KEYSTORE_PASSPHRASE, KEYSTORE_SSIN)
    with sts_service.session(token, "valid.acc-p12", KEYSTORE_PASSPHRASE) as session:
        sts_service.config_validator.setProperty("uid_test", uid)
        time.sleep(random.random()*10)
        result = sts_service.config_validator.getProperty("uid_test")
        assert result == uid

            
def test_sts__multiple_sessions():
    """
    Unclear if the current approach is safe across multiple concurrent STS sessions.
    Probably best not to count on it, but this test seems to indicate that it's ok
    """
    with ThreadPoolExecutor(max_workers=10) as ex:
        ex.map(task_set_random_config_value, [str(uuid4()) for _ in range(10)])
        