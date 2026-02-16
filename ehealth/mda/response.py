from pydantic import BaseModel, ConfigDict
from xsdata_pydantic.fields import field
from typing import List, Optional, Union
from xml.etree.ElementTree import QName
from xsdata.models.datatype import XmlDate, XmlDateTime

class Dimension(BaseModel):
    model_config = ConfigDict(extra='forbid', defer_build=True)
    
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


class AttributeValue(BaseModel):
    model_config = ConfigDict(extra='forbid', defer_build=True)
    
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


class NameId(BaseModel):
    model_config = ConfigDict(extra='forbid', defer_build=True)
    
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


class SubjectConfirmationData(BaseModel):
    model_config = ConfigDict(extra='forbid', defer_build=True)
    
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


class StatusCode(BaseModel):
    model_config = ConfigDict(extra='forbid', defer_build=True)
    
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

class Facet(BaseModel):
    model_config = ConfigDict(extra='forbid', defer_build=True)
    
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


class Attribute(BaseModel):
    model_config = ConfigDict(extra='forbid', defer_build=True)
    
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
        default_factory=list,
        metadata={
            "name": "AttributeValue",
            "type": "Element",
        }
    )


class SubjectConfirmation(BaseModel):
    model_config = ConfigDict(extra='forbid', defer_build=True)
    
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

class Detail(BaseModel):
    model_config = ConfigDict(defer_build=True)

class Details(BaseModel):
    model_config = ConfigDict(defer_build=True)

class Fault(BaseModel):
    model_config = ConfigDict(defer_build=True)

class StatusDetail(BaseModel):
    model_config = ConfigDict(defer_build=True)

class Status(BaseModel):
    model_config = ConfigDict(extra='forbid', defer_build=True)
    
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

class Advice(BaseModel):
    model_config = ConfigDict(extra='forbid', defer_build=True)
    
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
        default_factory=list,
        metadata={
            "name": "Facet",
            "type": "Element",
            "namespace": "urn:be:cin:nippin:memberdata:saml:extension",
        }
    )


class AttributeStatement(BaseModel):
    model_config = ConfigDict(extra='forbid', defer_build=True)
    
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    attribute: List[Attribute] = field(
        default_factory=list,
        metadata={
            "name": "Attribute",
            "type": "Element",
        }
    )


class Subject(BaseModel):
    model_config = ConfigDict(extra='forbid', defer_build=True)
    
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


class Assertion(BaseModel):
    model_config = ConfigDict(extra='forbid', defer_build=True)
    
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


class Response(BaseModel):
    model_config = ConfigDict(extra='forbid', defer_build=True)
    
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

class MemberData(BaseModel):
    model_config = ConfigDict(extra='forbid', defer_build=True)
    
    response: Response
    transaction_request: str
    transaction_response: str
    soap_request: str
    soap_response: str