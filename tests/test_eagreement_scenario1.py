from ehealth.eagreement import AskAgreementInputModel, Patient, Practitioner, ClaimAsk, Prescription, Attachment, EAgreementService
from xsdata.models.datatype import XmlDate
import os
import datetime
import pytest
import json
import logging
from uuid import uuid4
from pathlib import Path
from .utils import get_existing_agreements

logger = logging.getLogger(__name__)

KEYSTORE_PASSPHRASE = os.environ.get("KEYSTORE_PASSPHRASE")
KEYSTORE_SSIN = os.environ.get("KEYSTORE_SSIN")
KEYSTORE_PATH = "valid.acc-p12"
DATA_FOLDER = Path(__file__).parent.joinpath("data/faked_eagreement")

def ask_agreement_extended(service: EAgreementService, token: str, input_model: AskAgreementInputModel):
    # do a consult call first to store state
    patient = input_model.patient
    
    existing_agreements = get_existing_agreements(token, service, patient)
    logger.info(existing_agreements)

    # actual call
    response = service.ask_agreement(
            token=token,
            input_model=input_model
        )
    
    store = {
        "input_model": input_model.json(),
        "state": existing_agreements,
        "response": response.transaction_response
    }
    with open(DATA_FOLDER.joinpath(str(uuid4()) + ".json"), "w") as f:
        json.dump(store, f)
    return response

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

def test__6_1_1__no_prescription(sts_service, token, eagreement_service, default_input):
    default_input.claim.prescription = None
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = ask_agreement_extended(eagreement_service, token, default_input)

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

def test__6_1_2__failed_business_checks(sts_service, token, eagreement_service, default_input):
    # TODO this fails if 6_1_3 has executed for this patient
    # temp use another patient
    default_input.patient.ssin = "71070610591"
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eagreement_service.ask_agreement(
            token=token,
            input_model=default_input
        )
    claim_response = [e.resource.claim_response for e in response.response.entry if e.resource.claim_response is not None]
    assert len(claim_response) == 1
    claim_response = claim_response[0]
    assert claim_response.add_item.adjudication.category.coding.code.value == "refusal"
    assert claim_response.add_item.adjudication.reason.coding.code.value == "REF_AGREE_SRV_PHYSIO_010"
    assert claim_response.pre_auth_ref.value.startswith("100") # IO1

@pytest.mark.manual
def test__6_1_3__fa1(sts_service, token, eagreement_service, default_input):
    # preAuthPeriod start 2023-02-25
    # preAuthPeriod end 2024-02-24
    default_input.claim.product_or_service = "fa-1"
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
    assert claim_response.pre_auth_period.start.value == XmlDate.from_date(datetime.date.today() - datetime.timedelta(days=145))
    assert claim_response.pre_auth_period.end.value == XmlDate.from_date(datetime.date.today() + datetime.timedelta(days=219))

@pytest.mark.manual
def test__6_1_4__fa1_extend(sts_service, token, eagreement_service, default_input):
    # first consult to get the preAuthRef
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        existing_agreements = get_existing_agreements(token, eagreement_service, default_input.patient)
        if not existing_agreements.get("fa-1"):
            pytest.xfail("An existing fa-1 agreement is needed for this test")
        else:
            pre_auth_ref = existing_agreements.get("fa-1")[0]

    # extend response
    default_input.claim.pre_auth_ref = pre_auth_ref
    default_input.claim.transaction = "claim-extend"
    default_input.claim.product_or_service = "fa-1"
    default_input.claim.prescription.quantity = 43

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

    # check outcome
    outcome = [e.resource.operation_outcome for e in response.response.entry if e.resource.operation_outcome is not None]
    assert len(outcome) == 1
    outcome = outcome[0]
    assert outcome.issue.details.coding.code.value == "UNAUTHORIZED_CLAIM_PREAUTHREF_INVALID_SUBTYPE"

def test__6_1_5__missing_attachments(sts_service, token, eagreement_service, default_input):
    default_input.claim.product_or_service = "e-j-2"
    default_input.claim.prescription.quantity = 250
    default_input.claim.billable_period = datetime.date.today() - datetime.timedelta(days=90)
    default_input.claim.serviced_date = datetime.date.today() - datetime.timedelta(days=106)
    default_input.claim.prescription.date = datetime.date.today() - datetime.timedelta(days=100)
    # TODO this fails if 6_1_3 has executed for this patient
    # temp use another patient
    default_input.patient.ssin = "71070610591"
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
    assert "MISSING_MEDICALREPORT_ANNEX_IN_PHYSIO_CLAIM_SUPPORTINGINFO" in outcomes or "MISSING_RADIOLOGY_PROTOCOL_ANNEX_IN_PHYSIO_CLAIM_SUPPORTINGINFO" in outcomes

@pytest.mark.manual
def test__6_1_6__with_supporting_attachments(sts_service, token, eagreement_service, default_input):
    default_input.claim.product_or_service = "e-j-2"
    default_input.claim.prescription.quantity = 251
    default_input.claim.billable_period = datetime.date.today() - datetime.timedelta(days=100)
    default_input.claim.serviced_date = datetime.date.today() - datetime.timedelta(days=106)
    default_input.claim.prescription.date = datetime.date.today() - datetime.timedelta(days=100)
    default_input.claim.attachments = [
        Attachment(
            data_base64="QW5uZXhlIGlubGluZSwgYmFzZTY0ZWQ=",
            type="medical-report",
            title="attahcment",
        ),
        Attachment(
            data_base64="QW5uZXhlIGlubGluZSwgYmFzZTY0ZWQ=",
            type="radiology-protocol",
            title="attahcment",
        ),
    ]
    # TODO this fails if 6_1_3 has executed for this patient
    # temp use another patient
    default_input.patient.ssin = "71070610591"
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eagreement_service.ask_agreement(
            token=token,
            input_model=default_input
        )

    # xfail if pending request
    outcome = [e.resource.operation_outcome for e in response.response.entry if e.resource.operation_outcome is not None]
    if len(outcome) == 1:
        outcome = outcome[0]
        if outcome.issue.details.coding.code.value == "UNAUTHORIZED_CLAIM_DUE_TO_EXISTING_IN_PROCESS_CLAIM":
            pytest.xfail("TODO existing in process claim needs to be handled (can we cancel it somehow?)")
    
    # check claim response
    claim_response = [e.resource.claim_response for e in response.response.entry if e.resource.claim_response is not None]
    assert len(claim_response) == 1
    claim_response = claim_response[0]
    assert claim_response.add_item.adjudication.category.coding.code.value == "intreatment"
    assert claim_response.pre_auth_ref.value.startswith("100") # IO1

def test__6_1_7__async_agreement(sts_service, token, eagreement_service, default_input):
    # TODO will only work if 6_1_6 intreatment worked
    # TODO cannot continue until there are actual messages
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eagreement_service.async_messages(
            token=token,
        )
        logger.info(response)

@pytest.mark.manual
def test__6_1_8__conflict_with_existing_agreement(sts_service, token, eagreement_service, default_input):
    # NOTE essentially a copy of 6_1_6.  
    # If 6_1_6 executed first, this test will succeed
    default_input.claim.product_or_service = "e-j-2"
    default_input.claim.prescription.quantity = 200
    default_input.claim.billable_period = datetime.date.today() - datetime.timedelta(days=100)
    default_input.claim.serviced_date = datetime.date.today() - datetime.timedelta(days=106)
    default_input.claim.prescription.date = datetime.date.today() - datetime.timedelta(days=105)
    default_input.claim.attachments = [
        Attachment(
            data_base64="QW5uZXhlIGlubGluZSwgYmFzZTY0ZWQ=",
            type="medical-report",
            title="attahcment",
        ),
        Attachment(
            data_base64="QW5uZXhlIGlubGluZSwgYmFzZTY0ZWQ=",
            type="radiology-protocol",
            title="attahcment",
        ),
    ]
    # TODO this fails if 6_1_3 has executed for this patient
    # temp use another patient
    default_input.patient.ssin = "71070610591"
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eagreement_service.ask_agreement(
            token=token,
            input_model=default_input
        )

    # xfail if no existing agreement
    outcome = [e.resource.operation_outcome for e in response.response.entry if e.resource.operation_outcome is not None]
    if not len(outcome) == 1:
        pytest.xfail("No existing agreement for patient")
    
    # check message header
    message_header = [e.resource.message_header for e in response.response.entry if e.resource.message_header is not None]
    assert len(message_header) == 1
    message_header = message_header[0]
    assert message_header.event_coding.code.value == "reject"

    # check outcome
    outcome = [e.resource.operation_outcome for e in response.response.entry if e.resource.operation_outcome is not None]
    assert len(outcome) == 1
    outcome = outcome[0]
    assert outcome.issue.details.coding.code.value in (
        "UNAUTHORIZED_CLAIM_DUE_TO_EXISTING_AGREEMENT",
        "UNAUTHORIZED_CLAIM_DUE_TO_EXISTING_IN_PROCESS_CLAIM"
    )

@pytest.mark.manual
def test__6_1_9__conflict_with_existing_agreement__refusal_case(sts_service, token, eagreement_service, default_input):
    # TODO fails due to existing agreement, but not one that I requested??

    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        existing_agreements = get_existing_agreements(token, eagreement_service, default_input.patient)
        logger.info(existing_agreements)
        if not existing_agreements.get("fa-1"):
            pytest.xfail("An existing fa-1 agreement is needed for this test")

    default_input.claim.product_or_service = "co-1-2-3-0"
    default_input.claim.prescription.quantity = 9
    default_input.claim.billable_period = datetime.date.today() - datetime.timedelta(days=29)
    default_input.claim.serviced_date = datetime.date.today() - datetime.timedelta(days=32)
    default_input.claim.prescription.date = datetime.date.today() - datetime.timedelta(days=30)

    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = eagreement_service.ask_agreement(
            token=token,
            input_model=default_input
        )

    logger.info(response.transaction_request)
    logger.info(response.transaction_response)

    # check claim_response
    claim_response = [e.resource.claim_response for e in response.response.entry if e.resource.claim_response is not None]
    assert len(claim_response) == 1
    claim_response = claim_response[0]
    assert claim_response.add_item.adjudication.category.coding.code.value == "refusal"
    assert claim_response.add_item.adjudication.reason.coding.code.value == "REF_AGREE_SRV_PHYSIO_0001"
    assert claim_response.pre_auth_ref.value.startswith("100") # IO1