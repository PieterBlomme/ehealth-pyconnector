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
            ssin="51060205429",
            givenname="John",
            surname="Smith",
            gender="male"
        ),
        physician=Practitioner(
            nihii="32061701889",
            givenname="John",
            surname="Smith"
        ),
        claim=ClaimAsk(
            product_or_service="fa-6",
            billable_period=datetime.date.today() - datetime.timedelta(days=39),
            serviced_date=datetime.date.today() - datetime.timedelta(days=64),
            prescription=Prescription(
                data_base64="QW5uZXhlIGlubGluZSwgYmFzZTY0ZWQ=",
                snomed_category=91251008,
                snomed_code=91251008,
                date=datetime.date.today() - datetime.timedelta(days=40),
                quantity=60
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
 
def test__6_4_1__refused_due_to_age_requirements(sts_service, token, eagreement_service, default_input):
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
    assert claim_response.add_item.adjudication.reason.coding.code.value == "REF_AGREE_SRV_PHYSIO_010"
    
@pytest.mark.manual
def test__6_4_2__fa1(sts_service, token, eagreement_service, default_input):
    default_input.claim.product_or_service = "fa-1"
    default_input.claim.prescription.quantity = 61
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
    start_agreement = datetime.date.today() - datetime.timedelta(days=39)
    end_agreement = datetime.date.today() + datetime.timedelta(days=325)
    assert claim_response.pre_auth_period.start.value == XmlDate.from_date(start_agreement)
    assert claim_response.pre_auth_period.end.value == XmlDate.from_date(end_agreement)