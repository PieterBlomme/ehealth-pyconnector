from ehealth.sts import FakeSTSService
from ehealth.mda import FakeMDAService, MDAInputModel
from ehealth.mda.attribute_query import Facet, Dimension
from pathlib import Path
from pydantic import ValidationError
import os
import json
import glob
import pytest
import datetime
import logging

logger = logging.getLogger(__name__)

TEST_DATA_FOLDER = Path(__file__).parent.joinpath("data")
KEYSTORE_PASSPHRASE = os.environ.get("KEYSTORE_PASSPHRASE")
KEYSTORE_SSIN = os.environ.get("KEYSTORE_SSIN")
KEYSTORE_PATH = "valid.acc-p12"
MYCARENET_USER = os.environ.get("MYCARENET_USER")
MYCARENET_PWD = os.environ.get("MYCARENET_PWD")
NOT_BEFORE = datetime.datetime.fromisoformat("2021-01-01T00:00:00")
NOT_ON_OR_AFTER = datetime.datetime.fromisoformat("2022-01-16T00:00:00")

@pytest.fixture
def sts_service():
    return FakeSTSService()

@pytest.fixture
def mda_service():
    faked = []
    
    for fp in glob.glob(str(TEST_DATA_FOLDER.joinpath("faked/*.json"))):
        with open(fp) as f:
            data = json.load(f)

        mda_input = MDAInputModel(**data["mda_input"])
        response_string = data["response_string"]
        faked.append((mda_input, response_string))
        
    return FakeMDAService(
        faked=faked,
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