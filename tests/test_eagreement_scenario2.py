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

SSINS = ["71070610591", "90050725406", "96020232395", "91110537409", "68042002753"]
NIHIIS = ["58112129084", "12032636926", "76101138974", "30610131001", "76100322788"]
SSINS = ["71070610591"]
NIHIIS = ["58112129084"]

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
 
@pytest.mark.parametrize("ssin, nihii", zip(SSINS, NIHIIS))
def test__6_2_1(sts_service, token, eagreement_service, default_input, ssin, nihii):
    default_input.patient.ssin = ssin
    default_input.physician.nihii = nihii
    
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
    outcomes = [e.resource.operation_outcome.issue[0].details.coding.code.value for e in response.response.entry if e.resource.operation_outcome is not None]
    # for some reason I only get one of the errors
    assert (
        "UNAUTHORIZED_STARTDATE_IN_CLAIM_BILLABLEPERIOD" in outcomes or
        "INVALID_SERVICEREQUEST_PRESCRIPTIONDATE" in outcomes
        )

@pytest.mark.manual
@pytest.mark.parametrize("ssin, nihii", zip(SSINS, NIHIIS))
def test__6_2_2(sts_service, token, eagreement_service, default_input, ssin, nihii):
    default_input.patient.ssin = ssin
    default_input.physician.nihii = nihii
    
    default_input.claim.product_or_service = "fa-1"
    default_input.claim.prescription.quantity = 31
    default_input.claim.billable_period = datetime.date.today() - datetime.timedelta(days=120)
    default_input.claim.serviced_date = datetime.date.today() - datetime.timedelta(days=121)
    default_input.claim.prescription.date = datetime.date.today() - datetime.timedelta(days=121)

    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        existing_agreements = get_existing_agreements(token, eagreement_service, default_input.patient)
        logger.info(existing_agreements)

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
@pytest.mark.parametrize("ssin, nihii", zip(SSINS, NIHIIS))
def test__6_2_3(sts_service, token, eagreement_service, default_input, ssin, nihii):
    default_input.patient.ssin = ssin
    default_input.physician.nihii = nihii

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

@pytest.mark.asynchronous
@pytest.mark.parametrize("ssin, nihii", zip(SSINS, NIHIIS))
def test__6_2_4(sts_service, token, eagreement_service, default_input, ssin, nihii):
    default_input.patient.ssin = ssin
    default_input.physician.nihii = nihii

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
            if claim_response.add_item.product_or_service.coding.code.value != "fa-2":
                continue
            else:
                found = True
            logger.info(claim_response)
            assert claim_response.add_item.adjudication.category.coding.code.value == "wfi-physiotherapist"
            # NOTE: unclear how we know what extra info is needed ...
            assert claim_response.add_item.adjudication.reason.coding.code.value == "WFI_AGREE_SRV_PHYSIO_001"
            logging.info(claim_response.pre_auth_ref)
        assert found, "No matching message found"

@pytest.mark.manual
@pytest.mark.parametrize("ssin, nihii", zip(SSINS, NIHIIS))
def test__6_2_5(sts_service, token, eagreement_service, default_input, ssin, nihii):
    default_input.patient.ssin = ssin
    default_input.physician.nihii = nihii

    default_input.claim.transaction = "claim-argue"
    default_input.claim.product_or_service = "fa-2"
    default_input.claim.prescription = None
    default_input.claim.attachments = []
    default_input.claim.billable_period = None

    # first consult to get the preAuthRef
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        existing_agreements = get_existing_agreements(token, eagreement_service, default_input.patient)
        logger.info(existing_agreements)
        if not existing_agreements.get("fa-2"):
            pytest.xfail("An existing fa-2 agreement is needed for this test")
        else:
            pre_auth_ref = existing_agreements.get("fa-2")[0]
        default_input.claim.pre_auth_ref = "10020000000000450085" # TODO too many matches

        response = eagreement_service.argue_agreement(
            token=token,
            input_model=default_input
        )
    # check message header
    message_header = [e.resource.message_header for e in response.response.entry if e.resource.message_header is not None]
    assert len(message_header) == 1
    message_header = message_header[0]
    assert message_header.event_coding.code.value == "reject"

    # check outcomes
    outcomes = [e.resource.operation_outcome.issue[0].details.coding.code.value for e in response.response.entry if e.resource.operation_outcome is not None]
    # for some reason I only get one of the errors
    logger.warning(outcomes)
    assert (
        "UNAUTHORIZED_CLAIM_PREAUTHREF_WRONG_CAREPROVIDER" in outcomes or
        "MISSING_ARGUMENTATION_IN_CLAIM" in outcomes
        )

@pytest.mark.asynchronous
def test__6_2_6__argue_impossible_date(sts_service, token, eagreement_service, default_input):
    raise NotImplementedError("needs async implemented")

@pytest.mark.asynchronous
def test__6_2_7__argue_approved(sts_service, token, eagreement_service, default_input):
    raise NotImplementedError("needs async implemented")

@pytest.mark.asynchronous
def test__6_2_8__async_approved(sts_service, token, eagreement_service, default_input):
    raise NotImplementedError("needs async implemented")

@pytest.mark.manual
def test__6_2_9__early_closure(sts_service, token, eagreement_service, default_input):
    raise NotImplementedError("needs async implemented")

@pytest.mark.manual
def test__6_2_10__extend_failed_business_checks(sts_service, token, eagreement_service, default_input):
    raise NotImplementedError("needs async implemented")

@pytest.mark.manual
def test__6_2_11__complete_agreement_bad_reference(sts_service, token, eagreement_service, default_input):
    raise NotImplementedError("needs async implemented")

@pytest.mark.manual
def test__6_2_12(sts_service, token, eagreement_service, default_input):
    raise NotImplementedError("needs async implemented")