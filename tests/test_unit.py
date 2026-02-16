import pytest
import json
from pathlib import Path
from ehealth.sts.sts import STSService
from ehealth.mda.mda import MDAService
from ehealth.eagreement.eagreement import EAgreementService
from ehealth.eagreement.ask_agreement import Bundle as AskResponseBundle

@pytest.fixture
def token():
    return Path(__file__).parent.joinpath("data/token.xml").read_text()

@pytest.fixture
def mda_response():
    fp = Path(__file__).parent.joinpath("data/faked/2023-05-30T14:52:04.900078.json")
    with open(fp) as f:
        data = json.load(f)
    return data["response_string"]

@pytest.fixture
def eagreement_response():
    fp = Path(__file__).parent.joinpath("data/faked_eagreement/1a19624f-7c42-4530-9287-ea3231399e88.json")
    with open(fp) as f:
        data = json.load(f)
    return data["response"]

def test_parse_token(token):
    assertion = STSService.parse_token(token)
    assert assertion is not None
    
def test_parse_mda_response(token):
    response = MDAService.parse_response(token)
    assert response is not None
    
def test_parse_eagreement_response(eagreement_response):
    response = EAgreementService.parse_response(eagreement_response, AskResponseBundle)
    assert response is not None