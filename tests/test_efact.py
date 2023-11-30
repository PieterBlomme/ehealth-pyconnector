import os
import datetime
import pytest
import logging
from pathlib import Path
from ehealth.efact.efact import EFactService
from .conftest import MYCARENET_PWD, MYCARENET_USER

logger = logging.getLogger(__name__)

KEYSTORE_PASSPHRASE = os.environ.get("KEYSTORE_PASSPHRASE")
KEYSTORE_SSIN = os.environ.get("KEYSTORE_SSIN")
KEYSTORE_PATH = "valid.acc-p12"
DATA_FOLDER = Path(__file__).parent.joinpath("data")

@pytest.fixture
def efact_service():
    return EFactService(
        mycarenet_license_username=MYCARENET_USER,
        mycarenet_license_password=MYCARENET_PWD,
    )

def test_dummy(sts_service, token, efact_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        efact_service.send_efact(
            token,
        )