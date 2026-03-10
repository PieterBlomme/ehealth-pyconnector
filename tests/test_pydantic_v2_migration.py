import pytest
import json
import glob
import os
from io import StringIO
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata_pydantic.bindings import XmlParser

# Models
from ehealth.eagreement.ask_agreement import Bundle as EAgreementBundle
from ehealth.mda.response import Response as MDAResponse
from ehealth.eattestv3.send_transaction_response import SendTransactionResponse as EAttestResponse
from ehealth.addressbook.get_professional_contact_info_response import GetProfessionalContactInfoResponse
from ehealth.addressbook.search_professionals_response import SearchProfessionalsResponse
from ehealth.sts.assertion import Assertion

def test_sts_assertion_parsing():
    # Assertion.fake() generates an Assertion object, we can serialize and parse it
    assertion = Assertion.fake()
    from xsdata_pydantic.bindings import XmlSerializer
    serializer = XmlSerializer()
    xml_content = serializer.render(assertion)

    parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
    result = parser.parse(StringIO(xml_content), Assertion)

    assert isinstance(result, Assertion)
    assert result.assertion_id == assertion.assertion_id

def test_eagreement_parsing():
    xml_path = "tests/data/Bundle-ex01.xml"
    assert os.path.exists(xml_path)
    with open(xml_path, "r") as f:
        xml_content = f.read()

    parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
    result = parser.parse(StringIO(xml_content), EAgreementBundle)

    assert isinstance(result, EAgreementBundle)
    assert result.id.value == "ex01"

def test_mda_parsing():
    # Use one of the faked MDA responses
    faked_files = glob.glob("tests/data/faked/*.json")
    assert len(faked_files) > 0
    with open(faked_files[0], "r") as f:
        data = json.load(f)

    xml_content = data["response_string"]
    parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
    result = parser.parse(StringIO(xml_content), MDAResponse)

    assert isinstance(result, MDAResponse)
    assert result.status.status_code.value == 'urn:oasis:names:tc:SAML:2.0:status:Success'

def test_eattest_parsing():
    # Sample eAttest response XML
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<SendTransactionResponse xmlns="http://www.ehealth.fgov.be/messageservices/protocol/v1" xmlns:msgws="http://www.ehealth.fgov.be/messageservices/core/v1" xmlns:kmehr="http://www.ehealth.fgov.be/standards/kmehr/schema/v1" messageProtocoleSchemaVersion="1.0">
    <msgws:response>
        <msgws:id S="ID-KMEHR" SV="1.0">12345</msgws:id>
        <msgws:author>
            <kmehr:hcparty>
                <kmehr:id S="ID-HCPARTY">12345678901</kmehr:id>
                <kmehr:cd S="CD-HCPARTY" SV="1.16">persphysiotherapist</kmehr:cd>
            </kmehr:hcparty>
        </msgws:author>
        <msgws:date>2023-10-27</msgws:date>
        <msgws:time>08:27:00</msgws:time>
        <msgws:request>
            <msgws:id S="ID-KMEHR" SV="1.0">req123</msgws:id>
            <msgws:author>
                <kmehr:hcparty>
                    <kmehr:id S="ID-HCPARTY">12345678901</kmehr:id>
                    <kmehr:cd S="CD-HCPARTY" SV="1.16">persphysiotherapist</kmehr:cd>
                </kmehr:hcparty>
            </msgws:author>
            <msgws:date>2023-10-27</msgws:date>
            <msgws:time>08:27:00</msgws:time>
        </msgws:request>
    </msgws:response>
    <msgws:acknowledge>
        <msgws:iscomplete>true</msgws:iscomplete>
    </msgws:acknowledge>
</SendTransactionResponse>
"""
    parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
    result = parser.parse(StringIO(xml_content), EAttestResponse)

    assert isinstance(result, EAttestResponse)
    assert result.acknowledge.iscomplete is True

def test_address_book_get_parsing():
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<GetProfessionalContactInfoResponse xmlns="urn:be:fgov:ehealth:addressbook:protocol:v1" xmlns:ns2="urn:be:fgov:ehealth:commons:core:v2" xmlns:ns3="urn:be:fgov:ehealth:aa:complextype:v1" Id="req123" IssueInstant="2023-10-27T08:27:00Z">
    <ns2:Status>
        <ns2:StatusCode Value="urn:be:fgov:ehealth:commons:core:v2:status:success"/>
    </ns2:Status>
    <IndividualContactInformation>
        <ns3:LastName>Doe</ns3:LastName>
        <ns3:FirstName>John</ns3:FirstName>
        <ns3:Language>nl</ns3:Language>
        <ns3:Gender>male</ns3:Gender>
        <ns3:BirthDate>1980-01-01</ns3:BirthDate>
    </IndividualContactInformation>
</GetProfessionalContactInfoResponse>
"""
    parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
    # We need to handle potential model issues here if they arise
    result = parser.parse(StringIO(xml_content), GetProfessionalContactInfoResponse)

    assert isinstance(result, GetProfessionalContactInfoResponse)
    assert result.individual_contact_information.last_name == "Doe"

def test_address_book_search_parsing():
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<SearchProfessionalsResponse xmlns="urn:be:fgov:ehealth:addressbook:protocol:v1" xmlns:ns2="urn:be:fgov:ehealth:commons:core:v2" xmlns:ns3="urn:be:fgov:ehealth:aa:complextype:v1" Offset="0" MaxElements="10" Id="req123" IssueInstant="2023-10-27T08:27:00Z">
    <ns2:Status>
        <ns2:StatusCode Value="urn:be:fgov:ehealth:commons:core:v2:status:success"/>
        <ns2:StatusMessage>Success</ns2:StatusMessage>
    </ns2:Status>
    <ns3:HealthCareProfessional>
        <ns3:LastName>Doe</ns3:LastName>
        <ns3:FirstName>John</ns3:FirstName>
        <ns3:Profession>
            <ns3:ProfessionCode authenticSource="AS" type="T">PHYSICIAN</ns3:ProfessionCode>
            <ns3:ProfessionFriendlyName xml:lang="nl">Arts</ns3:ProfessionFriendlyName>
            <ns3:NIHII>12345678</ns3:NIHII>
        </ns3:Profession>
    </ns3:HealthCareProfessional>
</SearchProfessionalsResponse>
"""
    parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
    result = parser.parse(StringIO(xml_content), SearchProfessionalsResponse)

    assert isinstance(result, SearchProfessionalsResponse)
    assert len(result.health_care_professional) == 1
    assert result.health_care_professional[0].last_name == "Doe"
