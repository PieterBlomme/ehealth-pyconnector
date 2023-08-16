from ehealth.eagreement import AskAgreementInputModel, Patient, Practitioner, ClaimAsk, Prescription, FakeEAgreementService
from ehealth.sts import FakeSTSService
import os
import datetime
import glob
import json
import pytest
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

KEYSTORE_PASSPHRASE = os.environ.get("KEYSTORE_PASSPHRASE")
KEYSTORE_SSIN = os.environ.get("KEYSTORE_SSIN")
KEYSTORE_PATH = "valid.acc-p12"
DATA_FOLDER = Path(__file__).parent.joinpath("data/faked_eagreement")

@pytest.fixture(scope="function")
def default_input() -> AskAgreementInputModel:
    return AskAgreementInputModel(
        patient=Patient(
            ssin="71020203354",
            givenname="John",
            surname="Smith",
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


@pytest.fixture
def fake_sts_service():
    return FakeSTSService()

@pytest.fixture
def fake_mda_service():
    faked = []
    
    for fp in glob.glob(str(DATA_FOLDER.joinpath("*.json"))):
        with open(fp) as f:
            data = json.load(f)

        input_model = data["input_model"]
        logger.info(data["state"])
        state = data["state"]
        response_string = data["response"]
        faked.append((input_model, state, response_string))
    
    fake = FakeEAgreementService(
        faked=faked,
    )

    # TODO this should not be necessary if we can start from a clean slate
    initial_state = {'fa-1': [10016898543898835134], 'co-1-2-3-0': [10016900510520451182]}
    fake.set_state("71020203354", initial_state)
    return fake

def test__6_1_1__no_prescription(fake_sts_service, token, fake_mda_service, default_input):
    default_input.claim.prescription = None
    with fake_sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = fake_mda_service.ask_agreement(token, default_input)

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