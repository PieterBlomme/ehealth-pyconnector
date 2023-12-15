from xsdata.models.datatype import XmlDate
import os
import datetime
import pytest
import logging
from pathlib import Path
from ehealth.eattestv3.eattest import EAttestV3Service
from ehealth.eattestv3.input_models import EAttestInputModel, Patient, Transaction, CGDItem, Requestor
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

def test_4_1_1(sts_service, token, eattest_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eattest_service.send_attestation(
            token, 
            input_model=EAttestInputModel(
                patient=Patient(
                    givenname="John",
                    surname="Doe",
                    gender="male",
                    ssin="71020203354"
                ),
                transaction=Transaction(
                    bank_account="0635769870",
                    decisionreference="10020000000003100613",
                    cgds=[
                        CGDItem(
                            claim="560652",
                            decisionreference="10020000000003100613",
                            encounterdatetime=datetime.date.today().isoformat(),
                            amount=38.86,
                            requestor=Requestor(
                                givenname="Marie",
                                surname="Nolet de Brauwere van Steeland",
                                nihii="19733263004",
                                date_prescription=datetime.date.fromisoformat('2023-12-01')
                            ),
                        ),
                    ]
                )
            )
        )
    
    acknowledge = response.response.acknowledge
    assert acknowledge.error is not None
    assert acknowledge.error.cd.value == 269
    logger.info(acknowledge.error.cd.value)

def test_4_1_2(sts_service, token, eattest_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eattest_service.send_attestation(
            token, 
            input_model=EAttestInputModel(
                patient=Patient(
                    givenname="John",
                    surname="Doe",
                    gender="male",
                    ssin="58112129084"
                ),
                transaction=Transaction(
                    bank_account="0635769870",
                    cgds=[
                        CGDItem(
                            claim="567011",
                            decisionreference="50914202200000015966",
                            encounterdatetime=datetime.date.today().isoformat(),
                            amount=38.86,
                            requestor=Requestor(
                                givenname="Marie",
                                surname="Nolet de Brauwere van Steeland",
                                nihii="19733263004",
                                date_prescription=datetime.date.fromisoformat('2023-12-01')
                            ),
                        ),
                    ]
                )
            )
        )
    
    acknowledge = response.response.acknowledge
    assert acknowledge.error is not None
    assert acknowledge.error.cd.value == 267
    logger.info(acknowledge.error.cd.value)

def test_4_1_3(sts_service, token, eattest_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eattest_service.send_attestation(
            token, 
            input_model=EAttestInputModel(
                patient=Patient(
                    givenname="John",
                    surname="Doe",
                    gender="male",
                    ssin="58112129084"
                ),
                transaction=Transaction(
                    bank_account="0635769870",
                    cgds=[
                        CGDItem(
                            claim="560652",
                            decisionreference="10020000000002569234",
                            encounterdatetime=datetime.date.today().isoformat(),
                            amount=38.86,
                            requestor=Requestor(
                                givenname="Marie",
                                surname="Nolet de Brauwere van Steeland",
                                nihii="19733263004",
                                date_prescription=datetime.date.fromisoformat('2023-12-01')
                            ),
                        ),
                    ]
                )
            )
        )
    
    acknowledge = response.response.acknowledge
    assert acknowledge.error is not None
    logger.info(acknowledge.error.cd.value)
    assert acknowledge.error.cd.value == 268

@pytest.mark.skip
def test_4_1_4(sts_service, token, eattest_service):
    # manual testing
    pass

def test_4_1_5(sts_service, token, eattest_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eattest_service.send_attestation(
            token, 
            input_model=EAttestInputModel(
                patient=Patient(
                    givenname="John",
                    surname="Doe",
                    gender="male",
                    ssin="54032409450"
                ),
                transaction=Transaction(
                    bank_account="0635769870",
                    cgds=[
                        CGDItem(
                            claim="567011",
                            decisionreference="10016856095552803978",
                            encounterdatetime=datetime.date.today().isoformat(),
                            amount=38.86,
                            requestor=Requestor(
                                givenname="Marie",
                                surname="Nolet de Brauwere van Steeland",
                                nihii="19733263004",
                                date_prescription=datetime.date.fromisoformat('2023-12-01')
                            ),
                        ),
                        CGDItem(
                            claim="567011",
                            decisionreference="10016856095552803978",
                            encounterdatetime=(datetime.date.today() - datetime.timedelta(days=1)).isoformat(),
                            amount=38.86,
                            requestor=Requestor(
                                givenname="Marie",
                                surname="Nolet de Brauwere van Steeland",
                                nihii="19733263004",
                                date_prescription=datetime.date.fromisoformat('2023-12-01')
                            ),
                        ),
                    ]
                )
            )
        )
    
    acknowledge = response.response.acknowledge
    assert acknowledge.error is not None
    assert acknowledge.error.cd.value == 271
    logger.info(acknowledge.error.cd.value)

def test_4_1_6(sts_service, token, eattest_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eattest_service.send_attestation(
            token, 
            input_model=EAttestInputModel(
                patient=Patient(
                    givenname="John",
                    surname="Doe",
                    gender="male",
                    ssin="58112129084"
                ),
                transaction=Transaction(
                    amount=38.86,
                    bank_account="0635769870",
                    cgds=[
                        CGDItem(
                            claim="567011",
                            decisionreference="10016856095552803978",
                            encounterdatetime=datetime.date.today().isoformat(),
                            amount=38.86,
                            bank_account="0635769870",
                            requestor=Requestor(
                                givenname="Marie",
                                surname="Nolet de Brauwere van Steeland",
                                nihii="19733263004",
                                date_prescription=datetime.date.fromisoformat('2023-12-01')
                            ),
                        ),
                    ]
                )
            )
        )
    
    acknowledge = response.response.acknowledge
    assert acknowledge.error is not None
    assert acknowledge.error.cd.value == 274
    logger.info(acknowledge.error.cd.value)

def test_4_2_1(sts_service, token, eattest_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eattest_service.send_attestation(
            token, 
            input_model=EAttestInputModel(
                patient=Patient(
                    givenname="Youssef",
                    surname="Mghoghi",
                    gender="male",
                    ssin="68042000773"
                ),
                transaction=Transaction(
                    bank_account="0635769870",
                    cgds=[
                        CGDItem(
                            claim="567011",
                            decisionreference="90094042023349000066",
                            encounterdatetime=datetime.date.today().isoformat(),
                            amount=28.6,
                            requestor=Requestor(
                                givenname="Marie",
                                surname="Nolet de Brauwere van Steeland",
                                nihii="19733263004",
                                date_prescription=datetime.date.fromisoformat('2023-12-01')
                            ),
                        ),
                        CGDItem(
                            claim="567033",
                            decisionreference="90094042023349000066",
                            encounterdatetime=datetime.date.today().isoformat(),
                            amount=7.,
                            requestor=Requestor(
                                givenname="Marie",
                                surname="Nolet de Brauwere van Steeland",
                                nihii="19733263004",
                                date_prescription=datetime.date.fromisoformat('2023-12-01')
                            ),
                        ),
                    ]
                )
            )
        )
    
    acknowledge = response.response.acknowledge
    logger.info(response.transaction_request)
    logger.info(response.transaction_response)
    assert acknowledge.error is None

def test_4_2_2(sts_service, token, eattest_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eattest_service.send_attestation(
            token, 
            input_model=EAttestInputModel(
                patient=Patient(
                    givenname="John",
                    surname="Doe",
                    gender="male",
                    ssin="32061701889"
                ),
                transaction=Transaction(
                    bank_account="0635769870",
                    cgds=[
                        CGDItem(
                            claim="563393",
                            decisionreference="10020000000002569234",
                            encounterdatetime=datetime.date.today().isoformat(),
                            amount=38.86,
                        ),
                        CGDItem(
                            claim="639192",
                            decisionreference="10020000000002569234",
                            encounterdatetime=datetime.date.today().isoformat(),
                            amount=38.86,
                        ),
                    ]
                )
            )
        )
    
    acknowledge = response.response.acknowledge
    logger.info(response.transaction_request)
    logger.info(response.transaction_response)
    assert acknowledge.error is None

def test_4_2_3(sts_service, token, eattest_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eattest_service.send_attestation(
            token, 
            input_model=EAttestInputModel(
                patient=Patient(
                    givenname="John",
                    surname="Doe",
                    gender="male",
                    ssin="38060819220"
                ),
                requestor=Requestor(
                    givenname="John",
                    surname="Doe",
                    nihii="13679869620"
                ),
                transaction=Transaction(
                    bank_account="0635769870",
                    cgds=[
                        CGDItem(
                            claim="639472",
                            decisionreference="10020000000002569638",
                            encounterdatetime=datetime.date.today().isoformat(),
                            amount=38.86,
                        ),
                    ]
                )
            )
        )
    
    acknowledge = response.response.acknowledge
    logger.info(response.transaction_request)
    logger.info(response.transaction_response)
    assert acknowledge.error is None