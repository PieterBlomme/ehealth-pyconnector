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
            ssin="87060215703",
            givenname="John",
            surname="Smith",
            gender="male"
        ),
        physician=Practitioner(
            nihii="54032409450",
            givenname="John",
            surname="Smith"
        ),
        claim=ClaimAsk(
            product_or_service="fb-35",
            billable_period=datetime.date.today() - datetime.timedelta(days=87),
            serviced_date=datetime.date.today() - datetime.timedelta(days=89),
            prescription=Prescription(
                data_base64="QW5uZXhlIGlubGluZSwgYmFzZTY0ZWQ=",
                snomed_category=91251008,
                snomed_code=91251008,
                date=datetime.date.today() - datetime.timedelta(days=88),
                quantity=38
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
 
def test__6_3_1__fb_35_does_not_exist(sts_service, token, eagreement_service, default_input):
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
    assert (
        "UNAUTHORIZED_PRODUCTORSERVICE_IN_CLAIM_ITEM_PRODUCTORSERVICE" in outcomes or
        "INCONSISTENT_CLAIM_PRODUCTORSERVICE_WITH_CLAIM_SUBTYPE" in outcomes
        )
    
def test__6_3_2__bad_age_requirements(sts_service, token, eagreement_service, default_input):
    default_input.claim.product_or_service = "fb-51"
    default_input.claim.prescription.quantity = 51
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eagreement_service.ask_agreement(
            token=token,
            input_model=default_input
        )
    # check claim response
    claim_response = [e.resource.claim_response for e in response.response.entry if e.resource.claim_response is not None]
    assert len(claim_response) == 1
    claim_response = claim_response[0]
    assert claim_response.add_item.adjudication.category.coding.code.value == "refusal"
    assert claim_response.pre_auth_ref.value.startswith("100") # IO1
    assert claim_response.add_item.adjudication.reason.coding.code.value == "REF_AGREE_SRV_PHYSIO_015"

def test__6_3_3__fb_56(sts_service, token, eagreement_service, default_input):
    default_input.claim.product_or_service = "fb-56"
    default_input.claim.prescription.quantity = 52
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eagreement_service.ask_agreement(
            token=token,
            input_model=default_input
        )
    # check claim response
    claim_response = [e.resource.claim_response for e in response.response.entry if e.resource.claim_response is not None]
    assert len(claim_response) == 1
    claim_response = claim_response[0]
    assert claim_response.add_item.adjudication.category.coding.code.value == "refusal"
    assert claim_response.pre_auth_ref.value.startswith("100") # IO1
    assert claim_response.add_item.adjudication.reason.coding.code.value == "REF_AGREE_SRV_PHYSIO_012"

@pytest.mark.manual
def test__6_3_4__fb_55_ok(sts_service, token, eagreement_service, default_input):
    default_input.claim.product_or_service = "fb-55"
    default_input.claim.prescription.quantity = 53
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
    start_agreement = datetime.date.today() - datetime.timedelta(days=87)
    assert claim_response.pre_auth_period.start.value == XmlDate.from_date(start_agreement)
    assert claim_response.pre_auth_period.end.value == XmlDate.from_date(
        datetime.date(year=start_agreement.year + 2, month=12, day=31)
    )

def test__6_3_5__fb_58(sts_service, token, eagreement_service, default_input):
    default_input.claim.product_or_service = "fb-58"
    default_input.claim.prescription.quantity = 54
    default_input.claim.prescription.date = datetime.date.today() - datetime.timedelta(days=188)
    default_input.claim.billable_period = datetime.date.today() - datetime.timedelta(days=189)
    default_input.claim.serviced_date = datetime.date.today() - datetime.timedelta(days=2)
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
    assert (
        "INVALID_SERVICEREQUEST_PRESCRIPTIONDATE" in outcomes
        )

@pytest.mark.manual
def test__6_3_6__fb_58_ok(sts_service, token, eagreement_service, default_input):
    default_input.claim.product_or_service = "fb-58"
    default_input.claim.prescription.quantity = 55
    default_input.claim.prescription.date = datetime.date.today() - datetime.timedelta(days=5)
    default_input.claim.billable_period = datetime.date.today() - datetime.timedelta(days=2)
    default_input.claim.serviced_date = datetime.date.today() - datetime.timedelta(days=6)
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

def test__6_3_7__async(sts_service, token, eagreement_service, default_input):
    raise NotImplementedError("needs async implemented")

def test__6_3_8__async_closed(sts_service, token, eagreement_service, default_input):
    raise NotImplementedError("needs async implemented")

def test__6_3_9__extend(sts_service, token, eagreement_service, default_input):
    raise NotImplementedError("needs async implemented")

def test__6_3_10__extend(sts_service, token, eagreement_service, default_input):
    raise NotImplementedError("needs async implemented")