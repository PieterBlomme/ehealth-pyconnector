from ehealth.sts import STSService
from ehealth.mda import MDAService, MDAInputModel
from ehealth.mda.attribute_query import Facet, Dimension
from pathlib import Path
from pydantic import ValidationError
import os
import pytest
import datetime
import logging

logger = logging.getLogger(__name__)

TEST_DATA_FOLDER = Path(__file__).parent.joinpath("data")
KEYSTORE_PASSPHRASE = os.environ.get("KEYSTORE_PASSPHRASE")
KEYSTORE_SSIN = os.environ.get("KEYSTORE_SSIN")
KEYSTORE_PATH = TEST_DATA_FOLDER.joinpath("valid.acc-p12")
MYCARENET_USER = os.environ.get("MYCARENET_USER")
MYCARENET_PWD = os.environ.get("MYCARENET_PWD")
NOT_BEFORE = datetime.datetime.fromisoformat("2021-01-01T00:00:00")
NOT_ON_OR_AFTER = datetime.datetime.fromisoformat("2022-01-16T00:00:00")

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

def build_mda_input(
        ssin: str = KEYSTORE_SSIN, 
        notBefore: datetime.datetime = NOT_BEFORE, 
        notOnOrAfter: datetime.datetime=NOT_ON_OR_AFTER,
        **kwargs
        ):
    return MDAInputModel(
            ssin=ssin,
            notBefore=notBefore,
            notOnOrAfter=notOnOrAfter,
            **kwargs
        )

def test_mda__valid_ssin(sts_service, token, mda_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        mda = mda_service.get_member_data(
            token=token,
            mda_input=build_mda_input()
        )
        assert mda.response.status.status_code.value == 'urn:oasis:names:tc:SAML:2.0:status:Success'

def test_mda__ssin_combined_with_registration_number(token, mda_service):
    with pytest.raises(ValidationError):
        mda_service.get_member_data(
            token=token,
            mda_input=build_mda_input(registrationNumber = "1234"),
        )

def test_mda__ssin_combined_with_mutuality(token, mda_service):
    with pytest.raises(ValidationError):
        mda_service.get_member_data(
            token=token,
            mda_input=build_mda_input(mutuality = "1234"),
        )

def test_mda__registration_number_without_mutuality(token, mda_service):
    with pytest.raises(ValidationError):
        mda_service.get_member_data(
            token=token,
            mda_input=build_mda_input(registrationNumber = "1234", ssin=None),
        )
def test_mda__mutuality_without_registration_number(token, mda_service):
    with pytest.raises(ValidationError):
        mda_service.get_member_data(
            token=token,
            mda_input=build_mda_input(mutuality = "1234", ssin=None),
        )

def test_mda__invalid_ssin(sts_service, token, mda_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        mda = mda_service.get_member_data(
            token=token,
            mda_input=build_mda_input(ssin="1234"),
        )
        status = mda.response.status
        assert status.status_code.status_code.value == 'urn:be:cin:nippin:SAML:status:AttributeQueryError'
        assert status.status_detail.fault.fault_code == 'INPUT_ERROR'
        assert status.status_detail.fault.details.detail[0].detail_code == 'INVALID_INSS_FORMAT'
        assert status.status_detail.fault.details.detail[0].message == 'The INSS has an invalid format (not 11 digits)'

def test_mda__partial_response(sts_service, token, mda_service):
    ssin = "66010301329"
    facets = [
                    Facet(
                        id="urn:be:cin:nippin:chronicCondition",
                    )
                ]
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        mda = mda_service.get_member_data(
            token=token,
            mda_input=build_mda_input(ssin=ssin, facets=facets),
        )
        status = mda.response.status
        assert status.status_code.value == 'urn:oasis:names:tc:SAML:2.0:status:Success'
        assert status.status_code.status_code.value == 'urn:be:cin:nippin:SAML:status:PartialAnswer'
        assert status.status_detail.fault.fault_code == 'WARNING'
        assert status.status_detail.fault.details.detail[0].detail_code == 'BO_MISSING_FACET'
        assert status.status_detail.fault.details.detail[0].detail_source == 'FBIO'
        assert status.status_detail.fault.details.detail[1].detail_code == 'FACET_EXCEPTION'
        assert status.status_detail.fault.details.detail[1].detail_source == 'CHRONICCONDITION'
        assert status.status_detail.fault.details.detail[1].message == 'facet CHRONICCONDITION is not supported by FBIO'

def test_mda__invalid_facet(sts_service, token, mda_service):
    facets = [
                    Facet(
                        id="urn:be:cin:nippin:someWeirdFacet",
                    )
                ]
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        # fetch regular
        mda = mda_service.get_member_data(
            token=token,
            mda_input=build_mda_input(facets=facets),
        )
        status = mda.response.status
        assert mda.response.status.status_code.value == 'urn:oasis:names:tc:SAML:2.0:status:Requester'
        assert status.status_code.status_code.value == 'urn:be:cin:nippin:SAML:status:AttributeQueryError'
        assert status.status_detail.fault.fault_code == 'INPUT_ERROR'
        assert status.status_detail.fault.details.detail[0].detail_code == 'UNKNOWN_FACET'
        assert status.status_detail.fault.details.detail[0].message == 'A requested facet does not exist'
        assert mda.response.assertion == [] # nothing returned


def test_mda__valid_and_invalid_facet(sts_service, token, mda_service):
    facets = [
                    Facet(
                        id="urn:be:cin:nippin:someWeirdFacet",
                    ),
                    Facet(
                        id="urn:be:cin:nippin:insurability",
                        dimensions=[
                            Dimension(
                                id="requestType",
                                value="information",
                            ),
                            Dimension(
                                id="contactType",
                                value="other",
                            ),
                        ]
                    )
                ]
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        # fetch regular
        mda = mda_service.get_member_data(
            token=token,
            mda_input=build_mda_input(facets=facets),
        )
        status = mda.response.status
        assert mda.response.status.status_code.value == 'urn:oasis:names:tc:SAML:2.0:status:Requester'
        assert status.status_code.status_code.value == 'urn:be:cin:nippin:SAML:status:AttributeQueryError'
        assert status.status_detail.fault.fault_code == 'INPUT_ERROR'
        assert status.status_detail.fault.details.detail[0].detail_code == 'UNKNOWN_FACET'
        assert status.status_detail.fault.details.detail[0].message == 'A requested facet does not exist'
        assert mda.response.assertion == [] # nothing returned


def test_mda__invalid_dimension(sts_service, token, mda_service):
    facets = [
                    Facet(
                        id="urn:be:cin:nippin:insurability",
                        dimensions=[
                            Dimension(
                                id="loremipsem",
                                value="loremipsem",
                            ),
                        ]
                    )
                ]
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        # fetch regular
        mda = mda_service.get_member_data(
            token=token,
            mda_input=build_mda_input(facets=facets),
        )
        status = mda.response.status
        assert mda.response.status.status_code.value == 'urn:oasis:names:tc:SAML:2.0:status:Requester'
        assert status.status_code.status_code.value == 'urn:be:cin:nippin:SAML:status:AttributeQueryError'
        assert status.status_detail.fault.fault_code == 'INPUT_ERROR'
        assert status.status_detail.fault.details.detail[0].detail_code == 'INVALID_DIMENSION_ID'
        assert status.status_detail.fault.details.detail[0].message == 'A dimension is invalid in a facet'
        assert mda.response.assertion == [] # nothing returned

def test_mda__invalid_dimension_value(sts_service, token, mda_service):
    facets = [
                    Facet(
                        id="urn:be:cin:nippin:insurability",
                        dimensions=[
                            Dimension(
                                id="requestType",
                                value="loremipsem",
                            ),
                        ]
                    )
                ]
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        # fetch regular
        mda = mda_service.get_member_data(
            token=token,
            mda_input=build_mda_input(facets=facets),
        )
        status = mda.response.status
        assert mda.response.status.status_code.value == 'urn:oasis:names:tc:SAML:2.0:status:Requester'
        assert status.status_code.status_code.value == 'urn:be:cin:nippin:SAML:status:AttributeQueryError'
        assert status.status_detail.fault.fault_code == 'INPUT_ERROR'
        assert status.status_detail.fault.details.detail[0].detail_code == 'UNALLOWED_REQUESTTYPE'
        assert status.status_detail.fault.details.detail[0].message == 'The value of requestType is not in the list of allowed values'
        assert mda.response.assertion == [] # nothing returned

# MDA TEST SCENARIOS (Physiotherapy)

def test_mda__scenario_1(sts_service, token, mda_service):
    ssin = "84022148878"
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        mda = mda_service.get_member_data(
            token=token,
            mda_input=build_mda_input(ssin=ssin),
        )
        assert mda.response.status.status_code.value == 'urn:oasis:names:tc:SAML:2.0:status:Success'

        def _parse_period(assertion) -> dict:
            for attribute in assertion.attribute_statement.attribute:
                if attribute.name == 'urn:be:cin:nippin:cb1':
                    cb1 = attribute.attribute_value[0].value
                    return {
                        'cb1': cb1,
                    }

        insurability_periods = [_parse_period(a) for a in mda.response.assertion if a.advice.assertion_type == 'urn:be:cin:nippin:insurability:period']
        # expect at least 2 periods
        assert len(insurability_periods) >= 2
        assert insurability_periods[0]["cb1"] != insurability_periods[1]["cb1"]


def test_mda__scenario_2(sts_service, token, mda_service):
    ssin = "57010179489"
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        mda = mda_service.get_member_data(
            token=token,
            mda_input=build_mda_input(ssin=ssin),
        )
        assert mda.response.status.status_code.value == 'urn:oasis:names:tc:SAML:2.0:status:Success'

        # payment assertion should exist
        payment = [a for a in mda.response.assertion if a.advice.assertion_type == 'urn:be:cin:nippin:insurability:payment']
        assert len(payment) == 1
        # byIO should be True
        by_io = [attr for attr in payment[0].attribute_statement.attribute if attr.name == 'urn:be:cin:nippin:payment:byIO' and attr.attribute_value[0].value == 'True']
        assert len(by_io) == 1
    

def test_mda__scenario_3(sts_service, token, mda_service):
    ssin = "16112106736"
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        mda = mda_service.get_member_data(
            token=token,
            mda_input=build_mda_input(ssin=ssin),
        )
        assert mda.response.status.status_code.value == 'urn:oasis:names:tc:SAML:2.0:status:Success'

        # patientData assertion should exist
        patientData = [a for a in mda.response.assertion if a.advice.assertion_type == 'urn:be:cin:nippin:insurability:patientData']
        assert len(patientData) == 1
        # deceasedDate should exist
        deceasedDate = [attr for attr in patientData[0].attribute_statement.attribute if attr.name == 'urn:be:cin:nippin:careReceiver:deceasedDate']
        assert len(deceasedDate) == 1

        # generalSituation assertion should exist
        generalSituation = [a for a in mda.response.assertion if a.advice.assertion_type == 'urn:be:cin:nippin:insurability:generalSituation']
        assert len(generalSituation) == 1
        # event should be closedBefore
        event = [attr for attr in generalSituation[0].attribute_statement.attribute if attr.name == 'urn:be:cin:nippin:generalSituation:event' and attr.attribute_value[0].value == 'closedBefore']
        assert len(event) == 1


def test_mda__scenario_4(sts_service, token, mda_service):
    ssin = "53020927795"
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
            token=token,
            mda_input=build_mda_input(ssin=ssin, facets=facets),
        )
        assert mda.response.status.status_code.value == 'urn:oasis:names:tc:SAML:2.0:status:Success'

        # hospitalization info expected
        hospitalization = [a for a in mda.response.assertion if a.advice.assertion_type == 'urn:be:cin:nippin:hospitalisation']
        assert len(hospitalization) == 1
        
def test_mda__scenario_5(sts_service, token, mda_service):
    ssin = "58112438989"
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        mda = mda_service.get_member_data(
            token=token,
            mda_input=build_mda_input(ssin=ssin),
        )
        assert mda.response.status.status_code.value == 'urn:oasis:names:tc:SAML:2.0:status:Success'

        # medicalHouse info expected
        medicalHouse = [a for a in mda.response.assertion if a.advice.assertion_type == 'urn:be:cin:nippin:medicalHouse']
        assert len(medicalHouse) == 1
        # type should be Kine
        type_ = [attr for attr in medicalHouse[0].attribute_statement.attribute if attr.name == 'urn:be:cin:nippin:medicalHouse:type' and attr.attribute_value[0].value == 'Kine']
        assert len(type_) == 1

def test_mda__scenario_6(sts_service, token, mda_service):
    ssin = "70021546287"
    # for invoicing
    facets = [
                    Facet(
                        id="urn:be:cin:nippin:insurability",
                        dimensions=[
                            Dimension(
                                id="requestType",
                                value="invoicing",
                            ),
                            Dimension(
                                id="contactType",
                                value="other",
                            ),
                        ]
                    )
                ]
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        mda = mda_service.get_member_data(
            token=token,
            mda_input=build_mda_input(ssin=ssin, facets=facets),
        )
        assert mda.response.status.status_code.value == 'urn:oasis:names:tc:SAML:2.0:status:Success'

        # medicalHouse info expected
        periods = [a for a in mda.response.assertion if a.advice.assertion_type == 'urn:be:cin:nippin:insurability:period']
        assert len(periods) > 0
        # payment approval should not be None
        for p in periods:
            approval = [attr for attr in p.attribute_statement.attribute if attr.name == 'urn:be:cin:nippin:paymentApproval' and attr.attribute_value[0].value is not None]
            assert len(approval) == 1

def test_mda__scenario_7(sts_service, token, mda_service):
    # facet not allowed for physiotherpay
    ssin = "57052511675"
    facets = [
                    Facet(
                        id="urn:be:cin:nippin:carePath",
                    )
                ]
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        mda = mda_service.get_member_data(
            token=token,
            mda_input=build_mda_input(ssin=ssin, facets=facets),
        )
        
        assert mda.response.status.status_code.status_code.value == 'urn:be:cin:nippin:SAML:status:AttributeQueryError'
        assert mda.response.status.status_detail.fault.fault_code == 'AUTHORIZATION_ERROR'
        assert mda.response.status.status_detail.fault.details.detail[0].detail_code == 'UNAUTHORIZED_FACET'

def test_mda__scenario_8(sts_service, token, mda_service):
    ssin = "63102909243"
    facets = [
                    Facet(
                        id="urn:be:cin:nippin:chronicCondition",
                    )
                ]
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        mda = mda_service.get_member_data(
            token=token,
            mda_input=build_mda_input(ssin=ssin, facets=facets),
        )
        assert mda.response.status.status_code.value == 'urn:oasis:names:tc:SAML:2.0:status:Success'

        # chronicCondition info expected
        chronicCondition = [a for a in mda.response.assertion if a.advice.assertion_type == 'urn:be:cin:nippin:chronicCondition']
        assert len(chronicCondition) == 1

        # at least one year available
        chronicConditionYears = [attr for attr in chronicCondition[0].attribute_statement.attribute if attr.name == 'urn:be:cin:nippin:chronicCondition:year']
        assert len(chronicConditionYears) > 0

def test_mda__scenario_9(sts_service, token, mda_service):
    # facet not allowed for physiotherapy
    ssin = "46121723514"
    facets = [
                    Facet(
                        id="urn:be:cin:nippin:referencePharmacy",
                    )
                ]
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        mda = mda_service.get_member_data(
            token=token,
            mda_input=build_mda_input(ssin=ssin, facets=facets),
        )
        
        assert mda.response.status.status_code.status_code.value == 'urn:be:cin:nippin:SAML:status:AttributeQueryError'
        assert mda.response.status.status_detail.fault.fault_code == 'AUTHORIZATION_ERROR'
        assert mda.response.status.status_detail.fault.details.detail[0].detail_code == 'UNAUTHORIZED_FACET'


def test_mda__scenario_10(sts_service, token, mda_service):
    ssin = "58121520763"
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        # fetch regular
        mda = mda_service.get_member_data(
            token=token,
            mda_input=build_mda_input(ssin=ssin),
        )
        assert mda.response.status.status_code.value == 'urn:oasis:names:tc:SAML:2.0:status:Success'

        # patientData info expected
        patientData = [a for a in mda.response.assertion if a.advice.assertion_type == 'urn:be:cin:nippin:insurability:patientData']
        assert len(patientData) == 1
        
        # fetch with regNumber@mutuality
        mda = mda_service.get_member_data(
            token=token,
            mda_input=build_mda_input(ssin=None, registrationNumber="0001995151258", mutuality="319")
        )
        assert mda.response.status.status_code.value == 'urn:oasis:names:tc:SAML:2.0:status:Success'

        # patientData info expected
        patientData2 = [a for a in mda.response.assertion if a.advice.assertion_type == 'urn:be:cin:nippin:insurability:patientData']
        assert len(patientData2) == 1
        
        # check equality on some fields
        for attr_name in (
            'urn:be:fgov:person:ssin',
            'urn:be:cin:nippin:careReceiver:name',
            'urn:be:cin:nippin:careReceiver:firstName',
            'urn:be:cin:nippin:careReceiver:birthDate'
        ):
            a = [attr for attr in patientData[0].attribute_statement.attribute if attr.name == attr_name]
            b = [attr for attr in patientData2[0].attribute_statement.attribute if attr.name == attr_name]
            assert a == b
            assert len(a) == 1



def test_mda__scenario_11(sts_service, token, mda_service):
    ssin = "45112243029"
    facets = [
                    Facet(
                        id="urn:be:cin:nippin:globalMedicalFile",
                    )
                ]
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        # fetch regular
        mda = mda_service.get_member_data(
            token=token,
            mda_input=build_mda_input(ssin=ssin, facets=facets),
        )
        assert mda.response.status.status_code.value == 'urn:oasis:names:tc:SAML:2.0:status:Success'

        # globalMedicalFile info expected
        globalMedicalFile = [a for a in mda.response.assertion if a.advice.assertion_type == 'urn:be:cin:nippin:globalMedicalFile']
        assert len(globalMedicalFile) == 1
        

def test_mda__scenario_12(sts_service, token, mda_service):
    ssin = "72102534304"
    facets = [
                    Facet(
                        id="urn:be:cin:nippin:palliativeStatus",
                    )
                ]
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        # fetch regular
        mda = mda_service.get_member_data(
            token=token,
            mda_input=build_mda_input(ssin=ssin, facets=facets),
        )
        assert mda.response.status.status_code.value == 'urn:oasis:names:tc:SAML:2.0:status:Success'

        # palliativeStatus info expected
        palliativeStatus = [a for a in mda.response.assertion if a.advice.assertion_type == 'urn:be:cin:nippin:palliativeStatus']
        assert len(palliativeStatus) == 1
        

@pytest.mark.skip(reason="unitIssuance not available for physiotherapy")
def test_mda__scenario_13(sts_service, token, mda_service):
    pass

@pytest.mark.skip(reason="maxInvoiced not available for physiotherapy")
def test_mda__scenario_14(sts_service, token, mda_service):
    pass


def test_mda__facet_not_available(sts_service, token, mda_service):
    # patient is non palliative
    ssin = "90060421941"
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
                                value="other",
                            ),
                        ]
                    ),
                    Facet(
                        id="urn:be:cin:nippin:palliativeStatus",
                    )
                ]
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        # fetch regular
        mda = mda_service.get_member_data(
            token=token,
            mda_input=build_mda_input(ssin=ssin, facets=facets),
        )
        assert mda.response.status.status_code.value == 'urn:oasis:names:tc:SAML:2.0:status:Success'

        logger.info(mda.response.status)

        # palliativeStatus info not expected since patient not pallative
        # no errors ...
        palliativeStatus = [a for a in mda.response.assertion if a.advice.assertion_type == 'urn:be:cin:nippin:palliativeStatus']
        assert len(palliativeStatus) == 0