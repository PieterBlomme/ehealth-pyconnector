from ehealth.sts import FakeSTSService, STSService, KeyStoreException, SoapFaultException
from ehealth.mda import MDAService
from ehealth.mda.attribute_query import Facet, Dimension
from pathlib import Path
from typing import List
import os
import pytest
import datetime
import logging

logger = logging.getLogger(__name__)

TEST_DATA_FOLDER = Path(__file__).parent.joinpath("data")
KEYSTORE_PASSPHRASE = os.environ.get("KEYSTORE_PASSPHRASE")
KEYSTORE_SSIN = os.environ.get("KEYSTORE_SSIN")
KEYSTORE_PATH = str(TEST_DATA_FOLDER.joinpath("valid.acc-p12"))
MYCARENET_USER = os.environ.get("MYCARENET_USER")
MYCARENET_PWD = os.environ.get("MYCARENET_PWD")

@pytest.fixture
def sts_service():
    return STSService()

@pytest.fixture
def mda_service():
    return MDAService(
        mycarenet_license_username=MYCARENET_USER,
        mycarenet_license_password=MYCARENET_PWD,
    )

@pytest.fixture()
def token(sts_service):
    return sts_service.get_serialized_token(KEYSTORE_PATH, KEYSTORE_PASSPHRASE, KEYSTORE_SSIN)
    
def test_mda__valid_ssin(sts_service, token, mda_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        mda = mda_service.get_member_data(
            ssin=KEYSTORE_SSIN,
            token=token,
            notBefore=datetime.datetime.fromisoformat("2018-01-15T00:00:00"),
            notOnOrAfter=datetime.datetime.fromisoformat("2018-01-16T00:00:00"),
        )
        assert mda.response.status.status_code.value == 'urn:oasis:names:tc:SAML:2.0:status:Success'
        logger.info(mda.transaction_request)
        logger.info(mda.transaction_response)
        logger.info(mda.soap_request)
        logger.info(mda.soap_response)
        
def test_mda__invalid_ssin(sts_service, token, mda_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        mda = mda_service.get_member_data(
            ssin=1234,
            token=token,
            notBefore=datetime.datetime.fromisoformat("2018-01-15T00:00:00"),
            notOnOrAfter=datetime.datetime.fromisoformat("2018-01-16T00:00:00"),
        )
        status = mda.response.status
        assert status.status_code.status_code.value == 'urn:be:cin:nippin:SAML:status:AttributeQueryError'
        assert status.status_detail.fault.fault_code == 'INPUT_ERROR'
        assert status.status_detail.fault.details.detail.detail_code == 'INVALID_INSS_FORMAT'
        assert status.status_detail.fault.details.detail.message == 'The INSS has an invalid format (not 11 digits)'

# MDA TEST SCENARIOS (Physiotherapy)

NOT_BEFORE = datetime.datetime.fromisoformat("2021-01-01T00:00:00")
NOT_ON_OR_AFTER = datetime.datetime.fromisoformat("2022-01-16T00:00:00")

@pytest.mark.parametrize(
    "ssin", ["84022148878", "58121520763", pytest.param("76022354782", marks=pytest.mark.xfail(reason="Only 1 period returned")), "67120143655", "61111712346"]
)
def test_mda__scenario_1(sts_service, token, mda_service, ssin):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        mda = mda_service.get_member_data(
            ssin=ssin,
            token=token,
            notBefore=NOT_BEFORE,
            notOnOrAfter=NOT_ON_OR_AFTER,
        )
        assert mda.response.status.status_code.value == 'urn:oasis:names:tc:SAML:2.0:status:Success'

        def _parse_period(assertion) -> dict:
            for attribute in assertion.attribute_statement.attribute:
                if attribute.name == 'urn:be:cin:nippin:cb1':
                    cb1 = attribute.attribute_value.value
                    return {
                        'cb1': cb1,
                    }

        insurability_periods = [_parse_period(a) for a in mda.response.assertion if a.advice.assertion_type == 'urn:be:cin:nippin:insurability:period']
        # expect at least 2 periods
        assert len(insurability_periods) >= 2
        assert insurability_periods[0]["cb1"] != insurability_periods[1]["cb1"]

@pytest.mark.parametrize(
    "ssin", ["68091400202", "57010179489", "74080925023", "70021546287", "82062220229"]
)
def test_mda__scenario_2(sts_service, token, mda_service, ssin):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        mda = mda_service.get_member_data(
            ssin=ssin,
            token=token,
            notBefore=NOT_BEFORE,
            notOnOrAfter=NOT_ON_OR_AFTER,
        )
        assert mda.response.status.status_code.value == 'urn:oasis:names:tc:SAML:2.0:status:Success'

        for a in mda.response.assertion:
            if a.advice.assertion_type == "urn:be:cin:nippin:insurability:payment":
                for attribute in a.attribute_statement.attribute:
                    if attribute.name == 'urn:be:cin:nippin:payment:byIO':
                        assert attribute.attribute_value.value == 'True'
    
@pytest.mark.parametrize(
    "ssin", ["30050802512", "51052809178", "16112106736", "23102820194", "45072705334"]
)
def test_mda__scenario_3(sts_service, token, mda_service, ssin):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        mda = mda_service.get_member_data(
            ssin=ssin,
            token=token,
            notBefore=NOT_BEFORE,
            notOnOrAfter=NOT_ON_OR_AFTER,
        )
        assert mda.response.status.status_code.value == 'urn:oasis:names:tc:SAML:2.0:status:Success'

        for a in mda.response.assertion:
            if a.advice.assertion_type == 'urn:be:cin:nippin:insurability:patientData':
                # deceased date should be set
                assert len([attr for attr in a.attribute_statement.attribute if attr.name == 'urn:be:cin:nippin:careReceiver:deceasedDate']) == 1
            if a.advice.assertion_type == 'urn:be:cin:nippin:insurability:generalSituation':
                # closedBefore event presetn
                assert len([attr for attr in a.attribute_statement.attribute if attr.name == 'urn:be:cin:nippin:generalSituation:event' and attr.attribute_value.value == 'closedBefore']) == 1
            

@pytest.mark.parametrize(
    "ssin", ["53020927795", "67032535928", "63102909243", "69021902691", "77092206582"]
)
def test_mda__scenario_4(sts_service, token, mda_service, ssin):
    # hospitalized facet
    facets = [
                    Facet(
                        id="urn:be:cin:nippin:insurability",
                        dimensions=[
                            Dimension(
                                id="requestType",
                                value="information",
                            ),
                            Dimension(
                                id="contactType",
                                value="hospitalized",
                            ),
                        ]
                    )
                ]
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        mda = mda_service.get_member_data(
            ssin=ssin,
            token=token,
            notBefore=NOT_BEFORE,
            notOnOrAfter=NOT_ON_OR_AFTER,
            facets=facets,
        )
        assert mda.response.status.status_code.value == 'urn:oasis:names:tc:SAML:2.0:status:Success'

        # hospitalization info expected
        hospitalization = [a for a in mda.response.assertion if a.advice.assertion_type == 'urn:be:cin:nippin:hospitalisation']
        assert len(hospitalization) == 1