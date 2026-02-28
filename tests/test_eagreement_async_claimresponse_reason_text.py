"""Test that async ClaimResponse adjudication reason text is parsed correctly."""
from io import StringIO
from pathlib import Path

import pytest
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata_pydantic.bindings import XmlParser

from ehealth.eagreement.async_messages import Bundle as AsyncBundle


DATA_DIR = Path(__file__).parent / "data"
ASYNC_RESPONSE_WITH_REASON_TEXT = DATA_DIR / "async_claimresponse_reason_text.xml"

EXPECTED_REASON_TEXT = (
    "Justificatif manquant concernant la situation pathologique précédente: "
    "préciser la date d'apparition, la situation pathologique, ..."
)


def test_async_claimresponse_reason_text_parsed():
    """Parsing async response XML populates adjudication.reason.text.value."""
    xml = ASYNC_RESPONSE_WITH_REASON_TEXT.read_text()
    parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
    bundle = parser.parse(StringIO(xml), AsyncBundle)

    claim_responses = [
        e.resource.claim_response
        for e in bundle.entry
        if e.resource is not None and e.resource.claim_response is not None
    ]
    assert len(claim_responses) == 1
    claim_response = claim_responses[0]

    assert claim_response.add_item is not None
    assert claim_response.add_item.adjudication is not None
    assert claim_response.add_item.adjudication.reason is not None
    assert claim_response.add_item.adjudication.reason.coding is not None
    assert claim_response.add_item.adjudication.reason.coding.code.value == "WFI_AGREE_SRV_PHYSIO_004"

    # The reason text value (human-readable message) must be present and correct
    reason_text = claim_response.add_item.adjudication.reason.text
    assert reason_text is not None
    assert reason_text.value == EXPECTED_REASON_TEXT
