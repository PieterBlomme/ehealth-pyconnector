from ehealth.sts import STSService
from ehealth.eagreement import EAgreementService, AskAgreementInputModel, Patient, Practitioner, ClaimAsk, Prescription
from pathlib import Path
import os
import datetime
import pytest
import logging

logger = logging.getLogger(__name__)

TEST_DATA_FOLDER = Path(__file__).parent.joinpath("data")
KEYSTORE_PASSPHRASE = os.environ.get("KEYSTORE_PASSPHRASE")
KEYSTORE_SSIN = os.environ.get("KEYSTORE_SSIN")
KEYSTORE_PATH = "valid.acc-p12"
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


def test_eagreement__ask_agreement__happy_path(sts_service, token, eagreement_service):
    input_model = AskAgreementInputModel(
        patient=Patient(
            ssin="90060421941",
            givenname="Pieter",
            surname="Blomme",
            gender="male"
        ),
        physician=Practitioner(
            nihii="00092210605",
            givenname="John",
            surname="Smith"
        ),
        claim=ClaimAsk(
            sub_type="physiotherapy-fb",
            product_or_service="fb-51",
            billable_period=datetime.date.today() - datetime.timedelta(days=145),
            serviced_date=datetime.date.today() - datetime.timedelta(days=156),
            prescription=Prescription(
                data_base64="QW5uZXhlIGlubGluZSwgYmFzZTY0ZWQ=",
                snomed_category=91251008,
                snomed_code=91251008,
                date=datetime.date.today() - datetime.timedelta(days=145),
                quantity=15
            )
        )
    )
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eagreement_service.ask_agreement(
            token=token,
            input_model=input_model
        )
        logger.info(response)

def test_eagreement__consult_agreement__happy_path(sts_service, token, eagreement_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eagreement_service.consult_agreement(
            token=token,
        )
        logger.info(response)

def test_eagreement__scenario1__p1__no_prescription(sts_service, token, eagreement_service):
    input_model = AskAgreementInputModel(
        patient=Patient(
            ssin="71020203354",
            givenname="Dimitri Claude",
            surname="Rossion",
            gender="male"
        ),
        physician=Practitioner(
            nihii="00092210605",
            givenname="John",
            surname="Smith"
        ),
        claim=ClaimAsk(
            sub_type="physiotherapy-fa",
            product_or_service="fa-6",
            billable_period=datetime.date.today() - datetime.timedelta(days=145),
            serviced_date=datetime.date.today() - datetime.timedelta(days=156),
            prescription=None
        )
    )
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eagreement_service.ask_agreement(
            token=token,
            input_model=input_model
        )
    # check message header
    message_header = [e.resource.message_header for e in response.response.entry if e.resource.message_header is not None]
    assert len(message_header) == 1
    message_header = message_header[0]
    assert message_header.event_coding.code.value == "reject"

    # check outcome
    outcome = [e.resource.operation_outcome for e in response.response.entry if e.resource.operation_outcome is not None]
    assert len(outcome) == 1
    outcome = outcome[0]
    assert outcome.issue.severity.value == "error"
    assert outcome.issue.code.value == "business-rule"
    assert outcome.issue.details.coding.code.value == "MISSING_PRESCRIPTION_IN_PHYSIO_CLAIM"

def test_eagreement__scenario1__p1__failed_business_checks(sts_service, token, eagreement_service):
    # refusal
    # REF_AGREE_SRV_PHYSIO_010
    # preAuthEef 10016898541270783418
    # TODO investigate issues, I assume after one succesful call
    # a pending consultation is created and future calls are blocked ...
    input_model = AskAgreementInputModel(
        patient=Patient(
            ssin="71020203354",
            givenname="Dimitri Claude",
            surname="Rossion",
            gender="male"
        ),
        physician=Practitioner(
            nihii="00092210605",
            givenname="John",
            surname="Smith"
        ),
        claim=ClaimAsk(
            sub_type="physiotherapy-fa",
            product_or_service="fa-6",
            billable_period=datetime.date.today() - datetime.timedelta(days=145),
            serviced_date=datetime.date.today() - datetime.timedelta(days=156),
            prescription=Prescription(
                data_base64="QW5uZXhlIGlubGluZSwgYmFzZTY0ZWQ=",
                snomed_category=91251008,
                snomed_code=91251008,
                date=datetime.date.today() - datetime.timedelta(days=150),
                quantity=41
            )
        )
    )
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eagreement_service.ask_agreement(
            token=token,
            input_model=input_model
        )
    logger.info(response.transaction_request)
    for entry in response.response.entry:
        logger.info(entry)
    outcomes = [e.resource.operation_outcome.issue for e in response.response.entry if e.resource.operation_outcome is not None]
    assert len(outcomes) == 1
    issue = outcomes[0]
    assert issue.severity.value == "error"
    assert issue.code.value == "business-rule"
    assert issue.details.coding.code.value == "MISSING_PRESCRIPTION_IN_PHYSIO_CLAIM"

def test_eagreement__scenario1__p1__fa1(sts_service, token, eagreement_service):
    # agreement
    # preAuthPeriod start 2023-02-25
    # preAuthPeriod end 2024-02-24
    # preAuthRef 10016898543898835134
    input_model = AskAgreementInputModel(
        patient=Patient(
            ssin="71020203354",
            givenname="Dimitri Claude",
            surname="Rossion",
            gender="male"
        ),
        physician=Practitioner(
            nihii="00092210605",
            givenname="John",
            surname="Smith"
        ),
        claim=ClaimAsk(
            sub_type="physiotherapy-fa",
            product_or_service="fa-1",
            billable_period=datetime.date.today() - datetime.timedelta(days=145),
            serviced_date=datetime.date.today() - datetime.timedelta(days=156),
            prescription=Prescription(
                data_base64="QW5uZXhlIGlubGluZSwgYmFzZTY0ZWQ=",
                snomed_category=91251008,
                snomed_code=91251008,
                date=datetime.date.today() - datetime.timedelta(days=150),
                quantity=41
            )
        )
    )
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eagreement_service.ask_agreement(
            token=token,
            input_model=input_model
        )
    for entry in response.response.entry:
        logger.info(entry)