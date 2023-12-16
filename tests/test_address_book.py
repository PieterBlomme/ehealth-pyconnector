from ehealth.sts import STSService
from ehealth.addressbook.address_book import AddressBookService, InvalidNihii, UnknownNihii
from pathlib import Path
import os
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
    return STSService()

@pytest.fixture
def ab_service():
    return AddressBookService()

@pytest.fixture()
def token(sts_service):
    return sts_service.get_serialized_token(KEYSTORE_PATH, KEYSTORE_PASSPHRASE, KEYSTORE_SSIN)

def test_address_book_get_nihii(sts_service, token, ab_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        get_response = ab_service.get(prof_nihii="19733263")
        assert get_response.individual_contact_information.first_name == 'Marie'
        assert get_response.individual_contact_information.last_name == 'Nolet de Brauwere van Steeland'
        assert get_response.individual_contact_information.professional_information.profession.profession_code.value == "PHYSICIAN"
        # nihii with added qualification
        assert get_response.individual_contact_information.professional_information.profession.nihii == "19733263004"

def test_address_book_get_nihii_with_qual(sts_service, token, ab_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        get_response = ab_service.get(prof_nihii="19733263004")
        assert get_response.individual_contact_information.first_name == 'Marie'
        assert get_response.individual_contact_information.last_name == 'Nolet de Brauwere van Steeland'
        assert get_response.individual_contact_information.professional_information.profession.profession_code.value == "PHYSICIAN"
        # nihii with added qualification
        assert get_response.individual_contact_information.professional_information.profession.nihii == "19733263004"

def test_address_book_get_nihii_too_short(sts_service, token, ab_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        with pytest.raises(InvalidNihii):
            ab_service.get(prof_nihii="197332")

def test_address_book_get_nihii_too_long(sts_service, token, ab_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        with pytest.raises(InvalidNihii):
            ab_service.get(prof_nihii="19733263004123")

def test_address_book_get_nihii_unknown(sts_service, token, ab_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        with pytest.raises(UnknownNihii):
            ab_service.get(prof_nihii="12345678")

def test_address_book_search(sts_service, token, ab_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        search_response = ab_service.search(last_name_search="nolet")
        assert len(search_response.health_care_professional) == 3

def test_address_book_search_incl_first_name(sts_service, token, ab_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        search_response = ab_service.search(last_name_search="nolet", first_name_search="mar")
        assert len(search_response.health_care_professional) == 1

def test_address_book_search_many(sts_service, token, ab_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        search_response = ab_service.search(last_name_search="vande")
        assert len(search_response.health_care_professional) == 57
        
def test_address_book_search__janss_causes_issues(sts_service, token, ab_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        search_response = ab_service.search(last_name_search="janss")
        assert len(search_response.health_care_professional) == 0
