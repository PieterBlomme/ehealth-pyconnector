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

SSINS = ["87060215703", "87122330147", "96030160346", "70461304103", "68042110938"]
NIHIIS = ["54032409450", "05452903529", "88112535643", "30610131001", "90010156541"]
SSINS = ["87060215703"]
NIHIIS = ["54032409450"]

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
 
@pytest.mark.manual
def test_cancel_agreement(sts_service, token, eagreement_service, default_input):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        default_input.patient.ssin = "71070610591"
        existing_agreements = get_existing_agreements(token, eagreement_service, default_input.patient)
        logger.info(existing_agreements)
        if len(existing_agreements) == 0:
            return
        
        default_input.claim = ClaimAsk(
            transaction="claim-cancel",
            product_or_service="fa-1",
            pre_auth_ref="10020000000000400373"
        )

        response = eagreement_service.cancel_agreement(
            token=token,
            input_model=default_input
        )
        logger.info(response)
        existing_agreements = get_existing_agreements(token, eagreement_service, default_input.patient)
        logger.info(existing_agreements)

@pytest.mark.parametrize("ssin, nihii", zip(SSINS, NIHIIS))
def test__6_3_1(sts_service, token, eagreement_service, default_input, ssin, nihii):
    default_input.patient.ssin = ssin
    default_input.physician.nihii = nihii

    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        existing_agreements = get_existing_agreements(token, eagreement_service, default_input.patient)
        logger.info(existing_agreements)
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
    assert (
        "UNAUTHORIZED_PRODUCTORSERVICE_IN_CLAIM_ITEM_PRODUCTORSERVICE" in outcomes or
        "INCONSISTENT_CLAIM_PRODUCTORSERVICE_WITH_CLAIM_SUBTYPE" in outcomes
        )

@pytest.mark.parametrize("ssin, nihii", zip(SSINS, NIHIIS))
def test__6_3_2(sts_service, token, eagreement_service, default_input, ssin, nihii):
    default_input.patient.ssin = ssin
    default_input.physician.nihii = nihii

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


@pytest.mark.parametrize("ssin, nihii", zip(SSINS, NIHIIS))
def test__6_3_3(sts_service, token, eagreement_service, default_input, ssin, nihii):
    # NOTE: xfail fb-56 shouldn't be allowed but I get an agreement
    default_input.patient.ssin = ssin
    default_input.physician.nihii = nihii

    default_input.claim.product_or_service = "fb-56"
    default_input.claim.prescription.quantity = 52
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
    assert claim_response.add_item.adjudication.category.coding.code.value == "refusal"
    assert claim_response.pre_auth_ref.value.startswith("100") # IO1
    assert claim_response.add_item.adjudication.reason.coding.code.value == "REF_AGREE_SRV_PHYSIO_012"

@pytest.mark.parametrize("ssin, nihii", zip(SSINS, NIHIIS))
def test__6_3_4(sts_service, token, eagreement_service, default_input, ssin, nihii):
    default_input.patient.ssin = ssin
    default_input.physician.nihii = nihii

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

@pytest.mark.parametrize("ssin, nihii", zip(SSINS, NIHIIS))
def test__6_3_5(sts_service, token, eagreement_service, default_input, ssin, nihii):
    default_input.patient.ssin = ssin
    default_input.physician.nihii = nihii
    
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
    outcomes = [e.resource.operation_outcome.issue[0].details.coding.code.value for e in response.response.entry if e.resource.operation_outcome is not None]
    assert (
        "INVALID_SERVICEREQUEST_PRESCRIPTIONDATE" in outcomes
        )

@pytest.mark.manual
@pytest.mark.parametrize("ssin, nihii", zip(SSINS, NIHIIS))
def test__6_3_6(sts_service, token, eagreement_service, default_input, ssin, nihii):
    default_input.patient.ssin = ssin
    default_input.physician.nihii = nihii
    
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

@pytest.mark.asynchronous
@pytest.mark.parametrize("ssin, nihii", zip(SSINS, NIHIIS))
def test__6_3_7(sts_service, token, eagreement_service, default_input, ssin, nihii):
    default_input.patient.ssin = ssin
    default_input.physician.nihii = nihii

    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        existing_agreements = get_existing_agreements(token, eagreement_service, default_input.patient)
        logger.info(existing_agreements)
        
@pytest.mark.asynchronous
def test__6_3_8__async_closed(sts_service, token, eagreement_service, default_input):
    raise NotImplementedError("needs async implemented")

@pytest.mark.asynchronous
def test__6_3_9__extend(sts_service, token, eagreement_service, default_input):
    raise NotImplementedError("needs async implemented")

@pytest.mark.asynchronous
def test__6_3_10__extend(sts_service, token, eagreement_service, default_input):
    raise NotImplementedError("needs async implemented")