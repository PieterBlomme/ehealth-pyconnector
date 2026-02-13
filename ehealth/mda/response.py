from dataclasses import field
from pydantic import ConfigDict
from pydantic.dataclasses import dataclass
from typing import List, Optional, Union
from xml.etree.ElementTree import QName
from xsdata.models.datatype import XmlDate, XmlDateTime

@dataclass(config=ConfigDict(extra='forbid'))
class Dimension:
    class Meta:
        namespace = ""

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    value: str = field(
        default=""
    )


@dataclass(config=ConfigDict(extra='forbid'))
class AttributeValue:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    type: Optional[QName] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/2001/XMLSchema-instance",
        }
    )
    value: Union[str, bool, XmlDate] = field(
        default=""
    )


@dataclass(config=ConfigDict(extra='forbid'))
class NameId:
    class Meta:
        name = "NameID"
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    format: Optional[str] = field(
        default=None,
        metadata={
            "name": "Format",
            "type": "Attribute",
        }
    )
    value: Optional[str] = field(
        default=None
    )


@dataclass(config=ConfigDict(extra='forbid'))
class SubjectConfirmationData:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    not_before: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "NotBefore",
            "type": "Attribute",
        }
    )
    not_on_or_after: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "NotOnOrAfter",
            "type": "Attribute",
        }
    )


@dataclass(config=ConfigDict(extra='forbid'))
class StatusCode:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:protocol"

    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Attribute",
        }
    )
    status_code: Optional["StatusCode"] = field(
        default=None,
        metadata={
            "name": "StatusCode",
            "type": "Element",
        }
    )

@dataclass(config=ConfigDict(extra='forbid'))
class Facet:
    class Meta:
        namespace = "urn:be:cin:nippin:memberdata:saml:extension"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dimension: List[Dimension] = field(
        default_factory=list,
        metadata={
            "name": "Dimension",
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass(config=ConfigDict(extra='forbid'))
class Attribute:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
        }
    )
    attribute_value: List[AttributeValue] = field(
        default=list,
        metadata={
            "name": "AttributeValue",
            "type": "Element",
        }
    )


@dataclass(config=ConfigDict(extra='forbid'))
class SubjectConfirmation:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    method: Optional[str] = field(
        default=None,
        metadata={
            "name": "Method",
            "type": "Attribute",
        }
    )
    subject_confirmation_data: Optional[SubjectConfirmationData] = field(
        default=None,
        metadata={
            "name": "SubjectConfirmationData",
            "type": "Element",
        }
    )

@dataclass
class Detail:
    class Meta:
        namespace = "urn:be:cin:types:v1"

    detail_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "DetailCode",
            "type": "Element",
        }
    )
    detail_source: Optional[str] = field(
        default=None,
        metadata={
            "name": "DetailSource",
            "type": "Element",
        }
    )
    location: Optional[str] = field(
        default=None,
        metadata={
            "name": "Location",
            "type": "Element",
        }
    )
    message: Optional[str] = field(
        default=None,
        metadata={
            "name": "Message",
            "type": "Element",
        }
    )
@dataclass
class Details:
    class Meta:
        namespace = "urn:be:cin:types:v1"

    detail: List[Detail] = field(
        default=list,
        metadata={
            "name": "Detail",
            "type": "Element",
        }
    )
    
@dataclass
class Fault:
    class Meta:
        namespace = ""

    type: Optional[QName] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/2001/XMLSchema-instance",
        }
    )
    fault_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "FaultCode",
            "type": "Element",
            "namespace": "urn:be:cin:types:v1",
        }
    )
    fault_source: Optional[str] = field(
        default=None,
        metadata={
            "name": "FaultSource",
            "type": "Element",
            "namespace": "urn:be:cin:types:v1",
        }
    )
    message: Optional[object] = field(
        default=None,
        metadata={
            "name": "Message",
            "type": "Element",
            "namespace": "urn:be:cin:types:v1",
        }
    )
    details: Optional[Details] = field(
        default=None,
        metadata={
            "name": "Details",
            "type": "Element",
            "namespace": "urn:be:cin:types:v1",
        }
    )
    
@dataclass
class StatusDetail:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:protocol"

    fault: Optional[Fault] = field(
        default=None,
        metadata={
            "name": "Fault",
            "type": "Element",
            "namespace": "",
        }
    )

    fault_with_namespace: Optional[Fault] = field(
        default=None,
        metadata={
            "name": "Fault",
            "type": "Element",
            "namespace": "urn:be:cin:types:v1",
        }
    )
@dataclass(config=ConfigDict(extra='forbid'))
class Status:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:protocol"

    status_code: Optional[StatusCode] = field(
        default=None,
        metadata={
            "name": "StatusCode",
            "type": "Element",
        }
    )
    
    status_detail: Optional[StatusDetail] = field(
        default=None,
        metadata={
            "name": "StatusDetail",
            "type": "Element",
        }
    )

@dataclass(config=ConfigDict(extra='forbid'))
class Advice:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    type: Optional[QName] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/2001/XMLSchema-instance",
        }
    )
    assertion_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "AssertionType",
            "type": "Element",
            "namespace": "urn:be:cin:nippin:memberdata:saml:extension",
        }
    )
    facet: List[Facet] = field(
        default=list,
        metadata={
            "name": "Facet",
            "type": "Element",
            "namespace": "urn:be:cin:nippin:memberdata:saml:extension",
        }
    )


@dataclass(config=ConfigDict(extra='forbid'))
class AttributeStatement:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    attribute: List[Attribute] = field(
        default_factory=list,
        metadata={
            "name": "Attribute",
            "type": "Element",
        }
    )


@dataclass(config=ConfigDict(extra='forbid'))
class Subject:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    name_id: Optional[NameId] = field(
        default=None,
        metadata={
            "name": "NameID",
            "type": "Element",
        }
    )
    subject_confirmation: Optional[SubjectConfirmation] = field(
        default=None,
        metadata={
            "name": "SubjectConfirmation",
            "type": "Element",
        }
    )


@dataclass(config=ConfigDict(extra='forbid'))
class Assertion:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Attribute",
        }
    )
    issue_instant: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "IssueInstant",
            "type": "Attribute",
        }
    )
    version: Optional[float] = field(
        default=None,
        metadata={
            "name": "Version",
            "type": "Attribute",
        }
    )
    issuer: Optional[str] = field(
        default=None,
        metadata={
            "name": "Issuer",
            "type": "Element",
        }
    )
    subject: Optional[Subject] = field(
        default=None,
        metadata={
            "name": "Subject",
            "type": "Element",
        }
    )
    advice: Optional[Advice] = field(
        default=None,
        metadata={
            "name": "Advice",
            "type": "Element",
        }
    )
    attribute_statement: Optional[AttributeStatement] = field(
        default=None,
        metadata={
            "name": "AttributeStatement",
            "type": "Element",
        }
    )


@dataclass(config=ConfigDict(extra='forbid'))
class Response:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:protocol"

    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Attribute",
        }
    )
    in_response_to: Optional[str] = field(
        default=None,
        metadata={
            "name": "InResponseTo",
            "type": "Attribute",
        }
    )
    issue_instant: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "IssueInstant",
            "type": "Attribute",
        }
    )
    version: Optional[float] = field(
        default=None,
        metadata={
            "name": "Version",
            "type": "Attribute",
        }
    )
    issuer: Optional[str] = field(
        default=None,
        metadata={
            "name": "Issuer",
            "type": "Element",
            "namespace": "urn:oasis:names:tc:SAML:2.0:assertion",
        }
    )
    status: Optional[Status] = field(
        default=None,
        metadata={
            "name": "Status",
            "type": "Element",
        }
    )
    assertion: List[Assertion] = field(
        default_factory=list,
        metadata={
            "name": "Assertion",
            "type": "Element",
            "namespace": "urn:oasis:names:tc:SAML:2.0:assertion",
        }
    )

@dataclass(config=ConfigDict(extra='forbid'))
class MemberData:
    response: Response
    transaction_request: str
    transaction_response: str
    soap_request: str
    soap_response: str