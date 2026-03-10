import pytest
from io import StringIO
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata_pydantic.bindings import XmlParser
from ehealth.eagreement.ask_agreement import Bundle
import os

def test_pydantic_v2_xml_parsing():
    xml_path = "tests/data/Bundle-ex01.xml"
    assert os.path.exists(xml_path)

    with open(xml_path, "r") as f:
        xml_content = f.read()

    parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
    # This is the pattern we want to prove works
    result = parser.parse(StringIO(xml_content), Bundle)

    assert isinstance(result, Bundle)
    assert result.id.value == "ex01"
    assert len(result.entry) > 0

    # Verify that the problematic field (patient identifier value) was parsed correctly
    # Find the patient entry
    patient_entry = next(e for e in result.entry if e.resource.patient)
    assert patient_entry.resource.patient.identifier.value.value == "n° inscription mutualiste"

if __name__ == "__main__":
    pytest.main([__file__])
