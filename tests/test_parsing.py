"""
Testing parser.parse(StringIO(response_string), <TARGET_CLASS>) with the files in tests/data/examples_pydantic
"""
from io import StringIO
from xsdata_pydantic.bindings import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from ehealth.addressbook.get_professional_contact_info_response import GetProfessionalContactInfoResponse
from ehealth.addressbook.search_professionals_response import SearchProfessionalsResponse
from ehealth.sts.assertion import Assertion
from ehealth.eagreement.ask_agreement import Bundle as AskResponseBundle, Response as AskResponse
from ehealth.eagreement.consult_agreement import Bundle as ConsultResponseBundle, Response as ConsultResponse
from ehealth.eagreement.async_messages import Bundle as AsyncBundle, Response as AsyncResponse
from ehealth.eattestv3.send_transaction_response import SendTransactionResponse
from ehealth.mda.response import Response as MdaResponse
import logging

logger = logging.getLogger(__name__)

def test_parse_addressbook_get_response():
    parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
    with open("tests/data/examples_pydantic/response_get_addressbook.xml", "r") as f:
        response_string = f.read()
    response = parser.parse(StringIO(response_string), GetProfessionalContactInfoResponse)
    logger.info(response)

def test_parse_addresssbook_search_response():
    parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
    with open("tests/data/examples_pydantic/response_search_addressbook.xml", "r") as f:
        response_string = f.read()
    response = parser.parse(StringIO(response_string), SearchProfessionalsResponse)
    logger.info(response)

def test_parse_token():
    parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
    with open("tests/data/examples_pydantic/response_token.xml", "r") as f:
        response_string = f.read()
    response = parser.parse(StringIO(response_string), Assertion)
    logger.info(response)

def test_parse_eagreement():
    parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
    with open("tests/data/examples_pydantic/response_eagreement.xml", "r") as f:
        response_string = f.read()
    response = parser.parse(StringIO(response_string), AskResponseBundle)
    logger.info(response)

def test_parse_eattest():
    parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
    with open("tests/data/examples_pydantic/response_eattest.xml", "r") as f:
        response_string = f.read()
    response = parser.parse(StringIO(response_string), SendTransactionResponse)
    logger.info(response)

def test_parse_mda():
    parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
    with open("tests/data/examples_pydantic/response_mda.xml", "r") as f:
        response_string = f.read()
    response = parser.parse(StringIO(response_string), MdaResponse)
    logger.info(response)

def test_parse_eagreement_consult():
    parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
    with open("tests/data/examples_pydantic/response_eagreement_consult.xml", "r") as f:
        response_string = f.read()
    response = parser.parse(StringIO(response_string), ConsultResponseBundle)
    logger.info(response)

def test_parse_eagreement_async():
    parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
    with open("tests/data/examples_pydantic/response_eagreement_async.xml", "r") as f:
        response_string = f.read()
    response = parser.parse(StringIO(response_string), AsyncBundle)
    logger.info(response)