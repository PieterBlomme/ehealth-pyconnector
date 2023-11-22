from ehealth.eagreement import AskAgreementInputModel, Patient, Practitioner, ClaimAsk, Prescription
from xsdata.models.datatype import XmlDate
import os
import datetime
import pytest
import json
import logging
from uuid import uuid4
from pathlib import Path
from typing import Dict, List
from .utils import get_existing_agreements

logger = logging.getLogger(__name__)

KEYSTORE_PASSPHRASE = os.environ.get("KEYSTORE_PASSPHRASE")
KEYSTORE_SSIN = os.environ.get("KEYSTORE_SSIN")
KEYSTORE_PATH = "valid.acc-p12"
DATA_FOLDER = Path(__file__).parent.joinpath("data/faked_eagreement")

@pytest.fixture(scope="function")
def input_with_previous_prescription() -> AskAgreementInputModel:
    return AskAgreementInputModel(
        patient=Patient(
            ssin="71020203354",
            givenname="John",
            surname="Smith",
            gender="male"
        ),
        physician=Practitioner(
            nihii="19733263004",
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
                date=datetime.date.today() - datetime.timedelta(days=50),
                quantity=41
            ),
            previous_prescription=Prescription(
                data_base64="QW5uZXhlIGlubGluZSwgYmFzZTY0ZWQ=",
                date=datetime.date.today() - datetime.timedelta(days=55),
                snomed_category=91251008,
                snomed_code=91251008,
                quantity=20
            ),
        )
    )

def test_previous_prescription(sts_service, token, eagreement_service, input_with_previous_prescription):

    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eagreement_service.ask_agreement(
            token=token,
            input_model=input_with_previous_prescription
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
    for issue in outcome.issue:
        logger.info(issue)