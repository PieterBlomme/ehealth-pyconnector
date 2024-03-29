from ehealth.eagreement import AskAgreementInputModel, Patient, Practitioner, ClaimAsk, Prescription, Attachment, EAgreementService
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

SSINS = ["71020203354", "64051544103", "96010145781", "84080841501", "68042000773"]
NIHIIS = ["00092210605", "09120132247", "74050344782", "64090403291", "90010352422"]
SSINS = ["96010145781"]
NIHIIS = ["74050344782"]

def _get_existing_agreements(token, eagreement_service, patient) -> Dict[str, List[str]]:
    response = eagreement_service.consult_agreement(
        token=token,
        input_model=patient
    )
    bundle = [e.resource.bundle for e in response.response.entry if e.resource.bundle is not None]
    logger.info(response.response)
    assert len(bundle) == 1
    bundle = bundle[0]
    claim_response = [e.resource.claim_response for e in bundle.entry if e.resource.claim_response is not None]
    existing_agreements = {}
    for c in claim_response:
        if c.status.value != "active":
            logger.info(f"Status {c.status.value} != 'active'")
            continue
        if c.add_item.adjudication.category.coding.code.value not in ("intreatment", "agreement"):
            logger.info(f"Adjudication {c.add_item.adjudication.category.coding.code.value} != 'agreement'")
            continue
        code = c.add_item.product_or_service.coding.code.value
        existing_agreements[code] = existing_agreements.get(code, []) + [c.pre_auth_ref.value]
    return existing_agreements, response

def ask_agreement_extended(service: EAgreementService, token: str, input_model: AskAgreementInputModel):
    # do a consult call first to store state
    patient = input_model.patient
    
    existing_agreements, response = _get_existing_agreements(token, service, patient)
    logger.info(existing_agreements)

    # store consult call
    store = {
        "input_model": patient.json(),
        "state": existing_agreements,
        "response": response.transaction_response
    }
    # with open(DATA_FOLDER.joinpath(str(uuid4()) + ".json"), "w") as f:
        # json.dump(store, f)

    # actual ask call
    response = service.ask_agreement(
            token=token,
            input_model=input_model
        )
    
    store = {
        "input_model": input_model.json(),
        "state": existing_agreements,
        "response": response.transaction_response
    }
    # with open(DATA_FOLDER.joinpath(str(uuid4()) + ".json"), "w") as f:
        # json.dump(store, f)
    return response

@pytest.fixture(scope="function")
def default_input() -> AskAgreementInputModel:
    return AskAgreementInputModel(
        patient=Patient(
            ssin="",
            givenname="John",
            surname="Smith",
            gender="male"
        ),
        physician=Practitioner(
            nihii="",
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

@pytest.mark.parametrize("ssin, nihii", zip(SSINS, NIHIIS))
def test__6_1_1(sts_service, token, eagreement_service, default_input, ssin, nihii):
    default_input.patient.ssin = ssin
    default_input.physician.nihii = nihii

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
    for issue in outcome.issue:
        assert issue.severity.value == "error"
        assert issue.code.value == "business-rule"
        assert issue.details.coding.code.value == "MISSING_PRESCRIPTION_IN_PHYSIO_CLAIM"

@pytest.mark.parametrize("ssin, nihii", zip(SSINS, NIHIIS))
def test__6_1_2(sts_service, token, eagreement_service, default_input, ssin, nihii):
    # expected to fail for 71020203354 (existing agreement at the moment)
    # the others fail due to UKNOWN_PRACTITIONER_IDENTIFIER and even UNAUTHORIZED_SECTOR_IN_SERVICEREQUEST_REQUESTER ??
    default_input.patient.ssin = ssin
    default_input.physician.nihii = nihii

    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        existing_agreements = get_existing_agreements(token, eagreement_service, default_input.patient)
        logger.info(f"Existing agreements: {existing_agreements}")
        response = ask_agreement_extended(eagreement_service, token, default_input)

    outcome = [e.resource.operation_outcome for e in response.response.entry if e.resource.operation_outcome is not None]
    logger.warning(outcome)
    logger.warning(response.transaction_response)

    claim_response = [e.resource.claim_response for e in response.response.entry if e.resource.claim_response is not None]
    assert len(claim_response) == 1
    claim_response = claim_response[0]
    assert claim_response.add_item.adjudication.category.coding.code.value == "refusal"
    assert claim_response.add_item.adjudication.reason.coding.code.value == "REF_AGREE_SRV_PHYSIO_010"
    assert claim_response.pre_auth_ref.value.startswith("100") # IO1

@pytest.mark.manual
def test__6_1_3(sts_service, token, eagreement_service, default_input):
    # preAuthPeriod start 2023-02-25
    # preAuthPeriod end 2024-02-24
    default_input.claim.product_or_service = "fa-1"
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = ask_agreement_extended(eagreement_service, token, default_input)
    # check claim response
    claim_response = [e.resource.claim_response for e in response.response.entry if e.resource.claim_response is not None]
    assert len(claim_response) == 1
    claim_response = claim_response[0]
    assert claim_response.add_item.adjudication.category.coding.code.value == "agreement"
    assert claim_response.pre_auth_ref.value.startswith("100") # IO1
    assert claim_response.pre_auth_period.start.value == XmlDate.from_date(datetime.date.today() - datetime.timedelta(days=145))
    assert claim_response.pre_auth_period.end.value == XmlDate.from_date(datetime.date.today() + datetime.timedelta(days=219))

@pytest.mark.manual
@pytest.mark.parametrize("ssin, nihii", zip(SSINS, NIHIIS))
def test__6_1_4(sts_service, token, eagreement_service, default_input, ssin, nihii):
    default_input.patient.ssin = ssin
    default_input.physician.nihii = nihii

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
    for issue in outcome.issue:
        assert issue.details.coding.code.value == "UNAUTHORIZED_CLAIM_PREAUTHREF_INVALID_SUBTYPE"

@pytest.mark.parametrize("ssin, nihii", zip(SSINS, NIHIIS))
def test__6_1_5(sts_service, token, eagreement_service, default_input, ssin, nihii):
    default_input.patient.ssin = ssin
    default_input.physician.nihii = nihii

    default_input.claim.product_or_service = "e-j-2"
    default_input.claim.prescription.quantity = 250
    default_input.claim.billable_period = datetime.date.today() - datetime.timedelta(days=90)
    default_input.claim.serviced_date = datetime.date.today() - datetime.timedelta(days=106)
    default_input.claim.prescription.date = datetime.date.today() - datetime.timedelta(days=100)
    # TODO this fails if 6_1_3 has executed for this patient
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = ask_agreement_extended(eagreement_service, token, default_input)
    # check message header
    message_header = [e.resource.message_header for e in response.response.entry if e.resource.message_header is not None]
    assert len(message_header) == 1
    message_header = message_header[0]
    assert message_header.event_coding.code.value == "reject"

    # check outcomes
    outcomes = [e.resource.operation_outcome.issue[0].details.coding.code.value for e in response.response.entry if e.resource.operation_outcome is not None]
    # for some reason I only get one of the errors
    assert "MISSING_MEDICALREPORT_ANNEX_IN_PHYSIO_CLAIM_SUPPORTINGINFO" in outcomes or "MISSING_RADIOLOGY_PROTOCOL_ANNEX_IN_PHYSIO_CLAIM_SUPPORTINGINFO" in outcomes

@pytest.mark.manual
@pytest.mark.parametrize("ssin, nihii", zip(SSINS, NIHIIS))
def test__6_1_6(sts_service, token, eagreement_service, default_input, ssin, nihii):
    default_input.patient.ssin = ssin
    default_input.physician.nihii = nihii

    default_input.claim.product_or_service = "e-j-2"
    default_input.claim.prescription.quantity = 251
    default_input.claim.billable_period = datetime.date.today() - datetime.timedelta(days=100)
    default_input.claim.serviced_date = datetime.date.today() - datetime.timedelta(days=106)
    default_input.claim.prescription.date = datetime.date.today() - datetime.timedelta(days=100)
    default_input.claim.attachments = [
        Attachment(
            data_base64="QW5uZXhlIGlubGluZSwgYmFzZTY0ZWQ=",
            type="medical-report",
            title="attachment",
        ),
        Attachment(
            data_base64="QW5uZXhlIGlubGluZSwgYmFzZTY0ZWQ=",
            type="radiology-protocol",
            title="attachment",
        ),
    ]
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = ask_agreement_extended(eagreement_service, token, default_input)

    # xfail if pending request
    outcome = [e.resource.operation_outcome for e in response.response.entry if e.resource.operation_outcome is not None]
    if len(outcome) == 1:
        outcome = outcome[0]
        if outcome.issue[0].details.coding.code.value == "UNAUTHORIZED_CLAIM_DUE_TO_EXISTING_IN_PROCESS_CLAIM":
            pytest.xfail("TODO existing in process claim needs to be handled (can we cancel it somehow?)")
    
    # check claim response
    claim_response = [e.resource.claim_response for e in response.response.entry if e.resource.claim_response is not None]
    assert len(claim_response) == 1
    claim_response = claim_response[0]
    assert claim_response.add_item.adjudication.category.coding.code.value == "intreatment"
    assert claim_response.pre_auth_ref.value.startswith("100") # IO1

@pytest.mark.asynchronous
@pytest.mark.parametrize("ssin, nihii", zip(SSINS, NIHIIS))
def test__6_1_7(sts_service, token, eagreement_service, default_input, ssin, nihii):
    default_input.patient.ssin = ssin
    default_input.physician.nihii = nihii

    # TODO will only work if 6_1_6 intreatment worked
    # TODO cannot continue until there are actual m
    # essages
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        responses_async = eagreement_service.async_messages(token)
        assert len(responses_async) > 0

        found = False
        for response_async in responses_async:
            # check patient
            patients = [e.resource.patient for e in response_async.response.entry if e.resource.patient is not None]
            assert (len(patients)) == 1
            patient = patients[0]
            if patient.identifier.value.value != ssin:
                continue

            # check claim response
            claim_responses = [e.resource.claim_response for e in response_async.response.entry if e.resource.claim_response is not None]
            assert len(claim_responses) == 1
            claim_response = claim_responses[0]
            if claim_response.add_item.product_or_service.coding.code.value != "e-j-2":
                continue
            else:
                found = True
            assert claim_response.add_item.adjudication.category.coding.code.value == "agreement"
        assert found, "No matching message found"

@pytest.mark.manual
@pytest.mark.parametrize("ssin, nihii", zip(SSINS, NIHIIS))
def test__6_1_8(sts_service, token, eagreement_service, default_input, ssin, nihii):
    # Only works with a fixed setup date :( ...
    # output is only correct if servicedDate is the same as 6_1_6
    default_input.patient.ssin = ssin
    default_input.physician.nihii = nihii

    # NOTE essentially a copy of 6_1_6.  
    # If 6_1_7 executed first, this test will succeed
    default_input.claim.product_or_service = "e-j-2"
    default_input.claim.prescription.quantity = 200
    default_input.claim.billable_period = datetime.date.today() - datetime.timedelta(days=100)
    # serviced_date should be equal to serviced_date previous agreement
    default_input.claim.serviced_date = datetime.date.today() - datetime.timedelta(days=106)
    default_input.claim.prescription.date = datetime.date.today() - datetime.timedelta(days=105)
    default_input.claim.attachments = [
        Attachment(
            data_base64="QW5uZXhlIGlubGluZSwgYmFzZTY0ZWQ=",
            type="medical-report",
            title="attachment",
        ),
        Attachment(
            data_base64="QW5uZXhlIGlubGluZSwgYmFzZTY0ZWQ=",
            type="radiology-protocol",
            title="attachment",
        ),
    ]

    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = ask_agreement_extended(eagreement_service, token, default_input)

    # xfail if no existing agreement
    outcome = [e.resource.operation_outcome for e in response.response.entry if e.resource.operation_outcome is not None]
    
    # check message header
    message_header = [e.resource.message_header for e in response.response.entry if e.resource.message_header is not None]
    assert len(message_header) == 1
    message_header = message_header[0]
    logger.info(message_header)
    assert message_header.event_coding.code.value == "reject"

    # check outcome
    outcome = [e.resource.operation_outcome for e in response.response.entry if e.resource.operation_outcome is not None]
    assert len(outcome) == 1
    outcome = outcome[0]
    for issue in outcome.issue:
        assert issue.details.coding.code.value in (
            "UNAUTHORIZED_CLAIM_DUE_TO_EXISTING_AGREEMENT",
            "UNAUTHORIZED_CLAIM_DUE_TO_EXISTING_IN_PROCESS_CLAIM"
        )

@pytest.mark.manual
@pytest.mark.parametrize("ssin, nihii", zip(SSINS, NIHIIS))
def test__6_1_9(sts_service, token, eagreement_service, default_input, ssin, nihii):
    # fails on outcome due to existing co-1-2-3-0 agreement
    # not one that I created ...
    
    default_input.patient.ssin = ssin
    default_input.physician.nihii = nihii

    default_input.claim.product_or_service = "co-1-2-3-0"
    default_input.claim.prescription.quantity = 9
    default_input.claim.billable_period = datetime.date.today() - datetime.timedelta(days=29)
    default_input.claim.serviced_date = datetime.date.today() - datetime.timedelta(days=32)
    default_input.claim.prescription.date = datetime.date.today() - datetime.timedelta(days=30)

    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        response = ask_agreement_extended(eagreement_service, token, default_input)
    outcome = [e.resource.operation_outcome for e in response.response.entry if e.resource.operation_outcome is not None]
    assert len(outcome) == 1
    outcome = outcome[0]
    for issue in outcome.issue:
        logger.info(outcome)

    # check claim_response
    claim_response = [e.resource.claim_response for e in response.response.entry if e.resource.claim_response is not None]
    assert len(claim_response) == 1
    claim_response = claim_response[0]
    assert claim_response.add_item.adjudication.category.coding.code.value == "refusal"
    assert claim_response.add_item.adjudication.reason.coding.code.value == "REF_AGREE_SRV_PHYSIO_0001"
    assert claim_response.pre_auth_ref.value.startswith("100") # IO1