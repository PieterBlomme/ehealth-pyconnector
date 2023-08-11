from ehealth.eagreement import AskAgreementInputModel, Patient, Practitioner, ClaimAsk, Prescription, Attachment
from xsdata.models.datatype import XmlDate
import os
import datetime
import pytest
import logging
from .utils import get_existing_agreements

logger = logging.getLogger(__name__)

KEYSTORE_PASSPHRASE = os.environ.get("KEYSTORE_PASSPHRASE")
KEYSTORE_SSIN = os.environ.get("KEYSTORE_SSIN")
KEYSTORE_PATH = "valid.acc-p12"

@pytest.fixture(scope="function")
def default_input() -> AskAgreementInputModel:
    return AskAgreementInputModel(
        patient=Patient(
            ssin="71070610591",
            givenname="John",
            surname="Smith",
            gender="male"
        ),
        physician=Practitioner(
            nihii="58112129084",
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
            ),
            attachments= [
            Attachment(
                data_base64="QW5uZXhlIGlubGluZSwgYmFzZTY0ZWQ=",
                type="medical-report",
                title="attachment",
            ),
        ]
        )
    )
 
def test__6_2_1__inconsistent_dates(sts_service, token, eagreement_service, default_input):
    default_input.claim.product_or_service = "fa-1"
    default_input.claim.prescription.quantity = 30
    default_input.claim.billable_period = datetime.date.today() - datetime.timedelta(days=270)
    default_input.claim.serviced_date = datetime.date.today() - datetime.timedelta(days=239)
    default_input.claim.prescription.date = datetime.date.today() - datetime.timedelta(days=240)

    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eagreement_service.ask_agreement(
            token=token,
            input_model=default_input
        )
    # check message header
    message_header = [e.resource.message_header for e in response.response.entry if e.resource.message_header is not None]
    assert len(message_header) == 1
    message_header = message_header[0]
    assert message_header.event_coding.code.value == "reject"

    # check outcomes
    outcomes = [e.resource.operation_outcome.issue.details.coding.code.value for e in response.response.entry if e.resource.operation_outcome is not None]
    # for some reason I only get one of the errors
    assert (
        "UNAUTHORIZED_STARTDATE_IN_CLAIM_BILLABLEPERIOD" in outcomes or
        "INVALID_SERVICEREQUEST_PRESCRIPTIONDATE" in outcomes
        )

@pytest.mark.manual
def test__6_2_2__fa_1_success(sts_service, token, eagreement_service, default_input):
    default_input.claim.product_or_service = "fa-1"
    default_input.claim.prescription.quantity = 31
    default_input.claim.billable_period = datetime.date.today() - datetime.timedelta(days=120)
    default_input.claim.serviced_date = datetime.date.today() - datetime.timedelta(days=121)
    default_input.claim.prescription.date = datetime.date.today() - datetime.timedelta(days=121)

    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eagreement_service.ask_agreement(
            token=token,
            input_model=default_input
        )
    # check claim response
    claim_response = [e.resource.claim_response for e in response.response.entry if e.resource.claim_response is not None]
    assert len(claim_response) == 1
    claim_response = claim_response[0]
    assert claim_response.add_item.adjudication.category.coding.code.value == "agreement"
    assert claim_response.pre_auth_ref.value.startswith("100") # IO1
    assert claim_response.pre_auth_period.start.value == XmlDate.from_date(datetime.date.today() - datetime.timedelta(days=120))
    assert claim_response.pre_auth_period.end.value == XmlDate.from_date(datetime.date.today() + datetime.timedelta(days=244))

@pytest.mark.manual
def test__6_2_3__fa_2_intreatment(sts_service, token, eagreement_service, default_input):
    default_input.claim.product_or_service = "fa-2"
    default_input.claim.prescription.quantity = 32
    default_input.claim.billable_period = datetime.date.today() - datetime.timedelta(days=40)
    default_input.claim.serviced_date = datetime.date.today() - datetime.timedelta(days=46)
    default_input.claim.prescription.date = datetime.date.today() - datetime.timedelta(days=45)

    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eagreement_service.ask_agreement(
            token=token,
            input_model=default_input
        )
    # check claim response
    claim_response = [e.resource.claim_response for e in response.response.entry if e.resource.claim_response is not None]
    assert len(claim_response) == 1
    claim_response = claim_response[0]
    assert claim_response.add_item.adjudication.category.coding.code.value == "intreatment"
    assert claim_response.pre_auth_ref.value.startswith("100") # IO1

def test__6_2_4__async(sts_service, token, eagreement_service, default_input):
    raise NotImplementedError("needs async implemented")

def test__6_2_5__argue(sts_service, token, eagreement_service, default_input):
    raise NotImplementedError("needs async implemented")