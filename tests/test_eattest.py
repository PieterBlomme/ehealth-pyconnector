import os
import datetime
import pytest
import logging
from pathlib import Path
from ehealth.sts import STSService
from ehealth.eattestv3.eattest import EAttestV3Service
from ehealth.eattestv3.input_models import EAttestInputModel, Patient, Transaction, CGDItem, Requestor, Location
from ehealth.eattestv3.exceptions import EAttestRetryableAttempt, TechnicalEAttestException
from ehealth.utils.callbacks import storage_callback, file_callback

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
                    kbo_number="0635769870",
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
            ),
            callback_fn=file_callback
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
                    kbo_number="0635769870",
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
                    kbo_number="0635769870",
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
                    kbo_number="0635769870",
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
                    kbo_number="0635769870",
                    cgds=[
                        CGDItem(
                            claim="567011",
                            decisionreference="10016856095552803978",
                            encounterdatetime=datetime.date.today().isoformat(),
                            amount=38.86,
                            kbo_number="0635769870",
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
                    givenname="John",
                    surname="Doe",
                    gender="male",
                    ssin="58112129084"
                ),
                transaction=Transaction(
                    kbo_number="0635769870",
                    cgds=[
                        CGDItem(
                            claim="567011",
                            decisionreference="10020000000002569234",
                            encounterdatetime=datetime.date.today().isoformat(),
                            amount=29.6,
                            requestor=Requestor(
                                givenname="Marie",
                                surname="Nolet de Brauwere van Steeland",
                                nihii="19733263004",
                                date_prescription=datetime.date.fromisoformat('2023-09-02')
                            ),
                        ),
                        CGDItem(
                            claim="567033",
                            decisionreference="10020000000002569234",
                            encounterdatetime=datetime.date.today().isoformat(),
                            amount=8.,
                        ),
                    ]
                )
            ),
            callback_fn=file_callback
        )
    
    acknowledge = response.response.acknowledge
    assert acknowledge.error is None
    assert acknowledge.iscomplete == True

    transaction = response.response.kmehrmessage.folder.transaction
    assert len(transaction) == 3
    cga = transaction[0]
    # fetch invoicing number
    assert cga.cd.value == "cga"
    assert len(cga.item) == 1
    assert cga.item[0].cd.value == "invoicingnumber"
    invoice_number = cga.item[0].content[0].text.value
    logger.info(f"invoice number: {invoice_number}")

    # we are sending incorrect amounts on purpose
    # ensure the right amounts are returned
    cgd_1 = transaction[1]
    assert cgd_1.cd.value == "cgd"
    assert len(cgd_1.item) == 3 # claim, encounteredatetime, fee
    assert cgd_1.item[2].cd.value == "fee"
    assert cgd_1.item[2].cost.decimal == 28.6

    cgd_1 = transaction[2]
    assert cgd_1.cd.value == "cgd"
    assert len(cgd_1.item) == 3 # claim, encounteredatetime, fee
    assert cgd_1.item[2].cd.value == "fee"
    assert cgd_1.item[2].cost.decimal == 7.0

@pytest.mark.skip
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
                    kbo_number="0635769870",
                    cgds=[
                        CGDItem(
                            claim="563393",
                            decisionreference="10020000000002569234",
                            encounterdatetime=datetime.date.today().isoformat(),
                            amount=29.6,
                            requestor=Requestor(
                                givenname="Marie",
                                surname="Nolet de Brauwere van Steeland",
                                nihii="19733263004",
                                date_prescription=datetime.date.fromisoformat('2023-09-02')
                            ),
                        ),
                        CGDItem(
                            claim="639192",
                            decisionreference="10020000000002569234",
                            encounterdatetime=datetime.date.today().isoformat(),
                            amount=8.,
                            requestor=Requestor(
                                givenname="Marie",
                                surname="Nolet de Brauwere van Steeland",
                                nihii="19733263004",
                                date_prescription=datetime.date.fromisoformat('2023-09-02')
                            ),
                        ),
                    ]
                )
            )
        )
    
    acknowledge = response.response.acknowledge
    assert acknowledge.error is None
    logger.info(response.transaction_request)
    logger.info(response.transaction_response)
    assert acknowledge.iscomplete == True

    transaction = response.response.kmehrmessage.folder.transaction
    assert len(transaction) == 3
    cga = transaction[0]
    # fetch invoicing number
    assert cga.cd.value == "cga"
    assert len(cga.item) == 1
    assert cga.item[0].cd.value == "invoicingnumber"
    invoice_number = cga.item[0].content[0].text.value
    logger.info(f"invoice number: {invoice_number}")

    # we are sending incorrect amounts on purpose
    # ensure the right amounts are returned
    cgd_1 = transaction[1]
    assert cgd_1.cd.value == "cgd"
    assert len(cgd_1.item) == 3 # claim, encounteredatetime, fee
    assert cgd_1.item[2].cd.value == "fee"
    assert cgd_1.item[2].cost.decimal == 28.6

    cgd_1 = transaction[2]
    assert cgd_1.cd.value == "cgd"
    assert len(cgd_1.item) == 3 # claim, encounteredatetime, fee
    assert cgd_1.item[2].cd.value == "fee"
    assert cgd_1.item[2].cost.decimal == 7.0

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
                transaction=Transaction(
                    kbo_number="0635769870",
                    cgds=[
                        CGDItem(
                            claim="639472",
                            decisionreference="10020000000002569638",
                            encounterdatetime=datetime.date.today().isoformat(),
                            amount=53.0,
                            requestor=Requestor(
                                givenname="Marie",
                                surname="Nolet de Brauwere van Steeland",
                                nihii="19733263004",
                                date_prescription=datetime.date.fromisoformat('2023-09-02')
                            ),
                            location=Location(
                                nihii="74113047100", code_hc="orgretirementhome"
                            )
                        ),
                    ]
                )
            )
        )
    
    acknowledge = response.response.acknowledge
    assert acknowledge.error is None
    logger.info(response.transaction_request)
    logger.info(response.transaction_response)
    assert acknowledge.iscomplete == True

    transaction = response.response.kmehrmessage.folder.transaction
    assert len(transaction) == 2
    cga = transaction[0]
    # fetch invoicing number
    assert cga.cd.value == "cga"
    assert len(cga.item) == 1
    assert cga.item[0].cd.value == "invoicingnumber"
    invoice_number = cga.item[0].content[0].text.value
    logger.info(f"invoice number: {invoice_number}")

    cgd_1 = transaction[1]
    assert cgd_1.cd.value == "cgd"
    assert len(cgd_1.item) == 3 # claim, encounteredatetime, fee
    assert cgd_1.item[2].cd.value == "fee"
    assert cgd_1.item[2].cost.decimal == 53

    # no information returned about the location, so can't doublecheck

def test_4_2_4(sts_service, token, eattest_service):
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
                    kbo_number="0635769870",
                    cgds=[
                        CGDItem(
                            claim="561433",
                            decisionreference="10020000000002569234",
                            encounterdatetime=datetime.date.today().isoformat(),
                            amount=7.67,
                            requestor=Requestor(
                                givenname="Marie",
                                surname="Nolet de Brauwere van Steeland",
                                nihii="19733263004",
                                date_prescription=datetime.date.fromisoformat('2023-09-02')
                            ),
                        )
                    ]
                )
            )
        )
    
    acknowledge = response.response.acknowledge
    assert acknowledge.error is None
    assert acknowledge.iscomplete == True

    transaction = response.response.kmehrmessage.folder.transaction
    assert len(transaction) == 2
    cga = transaction[0]
    # fetch invoicing number
    assert cga.cd.value == "cga"
    assert len(cga.item) == 1
    assert cga.item[0].cd.value == "invoicingnumber"
    invoice_number = cga.item[0].content[0].text.value
    logger.info(f"invoice number: {invoice_number}")

    cgd_1 = transaction[1]
    assert cgd_1.cd.value == "cgd"
    assert len(cgd_1.item) == 3 # claim, encounteredatetime, fee
    assert cgd_1.item[2].cd.value == "fee"
    assert cgd_1.item[2].cost.decimal == 7.67

def test_4_2_5(sts_service, token, eattest_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eattest_service.send_attestation(
            token, 
            input_model=EAttestInputModel(
                patient=Patient(
                    givenname="John",
                    surname="Doe",
                    gender="male",
                    ssin="99122847869"
                ),
                transaction=Transaction(
                    kbo_number="0635769870",
                    cgds=[
                        CGDItem(
                            claim="561610",
                            decisionreference="10016850959538533755",
                            encounterdatetime=datetime.date.today().isoformat(),
                            amount=28.0,
                            requestor=Requestor(
                                givenname="Marie",
                                surname="Nolet de Brauwere van Steeland",
                                nihii="19733263004",
                                date_prescription=datetime.date.fromisoformat('2023-09-02')
                            ),
                            supplement=10.0
                        )
                    ]
                )
            )
        )
    
    acknowledge = response.response.acknowledge
    assert acknowledge.error is None
    assert acknowledge.iscomplete == True

    transaction = response.response.kmehrmessage.folder.transaction
    assert len(transaction) == 2
    cga = transaction[0]
    # fetch invoicing number
    assert cga.cd.value == "cga"
    assert len(cga.item) == 1
    assert cga.item[0].cd.value == "invoicingnumber"
    invoice_number = cga.item[0].content[0].text.value
    logger.info(f"invoice number: {invoice_number}")

    cgd_1 = transaction[1]
    assert cgd_1.cd.value == "cgd"
    assert len(cgd_1.item) == 3 # claim, encounteredatetime, fee
    assert cgd_1.item[2].cd.value == "fee"
    assert cgd_1.item[2].cost.decimal == 28.0

    # no information returned about the supplement, so can't doublecheck


def test_retryable(sts_service, token, eattest_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        with pytest.raises(TechnicalEAttestException) as exc_info:
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
                        kbo_number="0635769870",
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
                    ),
                    force_retryable=True
                ),
                callback_fn=file_callback
            )
    
        retryable = exc_info.value.retryable
        response = eattest_service.retry_send_attestation(
            token=token,
            input_model=retryable,
            callback_fn=file_callback
        )
    acknowledge = response.response.acknowledge
    assert acknowledge.error is not None
    assert acknowledge.error.cd.value == 269
    logger.info(acknowledge.error.cd.value)