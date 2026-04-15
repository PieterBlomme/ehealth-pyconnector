
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Union
from xml.etree.ElementTree import QName
from xsdata.models.datatype import XmlDate, XmlDateTime

class Dimension(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = ""

    model_config = ConfigDict(defer_build=True)

    id: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    value: str = Field(
        default=""
    )

class AttributeValue(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    model_config = ConfigDict(defer_build=True)

    type: Optional[QName] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/2001/XMLSchema-instance",
        }
    )
    value: Union[str, bool, XmlDate] = Field(
        default=""
    )

class NameId(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        name = "NameID"
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    model_config = ConfigDict(defer_build=True)

    format: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Format",
            "type": "Attribute",
        }
    )
    value: Optional[str] = Field(
        default=None
    )

class SubjectConfirmationData(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    model_config = ConfigDict(defer_build=True)

    not_before: Optional[XmlDateTime] = Field(
        default=None,
        metadata={
            "name": "NotBefore",
            "type": "Attribute",
        }
    )
    not_on_or_after: Optional[XmlDateTime] = Field(
        default=None,
        metadata={
            "name": "NotOnOrAfter",
            "type": "Attribute",
        }
    )

class StatusCode(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:protocol"

    model_config = ConfigDict(defer_build=True)

    value: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Attribute",
        }
    )
    status_code: Optional["StatusCode"] = Field(
        default=None,
        metadata={
            "name": "StatusCode",
            "type": "Element",
        }
    )

class Facet(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:be:cin:nippin:memberdata:saml:extension"

    model_config = ConfigDict(defer_build=True)

    id: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    dimension: List[Dimension] = Field(
        default_factory=list,
        metadata={
            "name": "Dimension",
            "type": "Element",
            "namespace": "",
        }
    )

class Attribute(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    model_config = ConfigDict(defer_build=True)

    name: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
        }
    )
    attribute_value: List[AttributeValue] = Field(
        default=list,
        metadata={
            "name": "AttributeValue",
            "type": "Element",
        }
    )

class SubjectConfirmation(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    model_config = ConfigDict(defer_build=True)

    method: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Method",
            "type": "Attribute",
        }
    )
    subject_confirmation_data: Optional[SubjectConfirmationData] = Field(
        default=None,
        metadata={
            "name": "SubjectConfirmationData",
            "type": "Element",
        }
    )

class Detail(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:be:cin:types:v1"

    model_config = ConfigDict(defer_build=True)

    detail_code: Optional[str] = Field(
        default=None,
        metadata={
            "name": "DetailCode",
            "type": "Element",
        }
    )
    detail_source: Optional[str] = Field(
        default=None,
        metadata={
            "name": "DetailSource",
            "type": "Element",
        }
    )
    location: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Location",
            "type": "Element",
        }
    )
    message: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Message",
            "type": "Element",
        }
    )
class Details(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:be:cin:types:v1"

    model_config = ConfigDict(defer_build=True)

    detail: List[Detail] = Field(
        default=list,
        metadata={
            "name": "Detail",
            "type": "Element",
        }
    )
    
class Fault(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = ""

    model_config = ConfigDict(defer_build=True)

    type: Optional[QName] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/2001/XMLSchema-instance",
        }
    )
    fault_code: Optional[str] = Field(
        default=None,
        metadata={
            "name": "FaultCode",
            "type": "Element",
            "namespace": "urn:be:cin:types:v1",
        }
    )
    fault_source: Optional[str] = Field(
        default=None,
        metadata={
            "name": "FaultSource",
            "type": "Element",
            "namespace": "urn:be:cin:types:v1",
        }
    )
    message: Optional[object] = Field(
        default=None,
        metadata={
            "name": "Message",
            "type": "Element",
            "namespace": "urn:be:cin:types:v1",
        }
    )
    details: Optional[Details] = Field(
        default=None,
        metadata={
            "name": "Details",
            "type": "Element",
            "namespace": "urn:be:cin:types:v1",
        }
    )
    
class StatusDetail(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:protocol"

    model_config = ConfigDict(defer_build=True)

    fault: Optional[Fault] = Field(
        default=None,
        metadata={
            "name": "Fault",
            "type": "Element",
            "namespace": "",
        }
    )

    fault_with_namespace: Optional[Fault] = Field(
        default=None,
        metadata={
            "name": "Fault",
            "type": "Element",
            "namespace": "urn:be:cin:types:v1",
        }
    )
class Status(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:protocol"

    model_config = ConfigDict(defer_build=True)

    status_code: Optional[StatusCode] = Field(
        default=None,
        metadata={
            "name": "StatusCode",
            "type": "Element",
        }
    )
    
    status_detail: Optional[StatusDetail] = Field(
        default=None,
        metadata={
            "name": "StatusDetail",
            "type": "Element",
        }
    )

class Advice(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    model_config = ConfigDict(defer_build=True)

    type: Optional[QName] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/2001/XMLSchema-instance",
        }
    )
    assertion_type: Optional[str] = Field(
        default=None,
        metadata={
            "name": "AssertionType",
            "type": "Element",
            "namespace": "urn:be:cin:nippin:memberdata:saml:extension",
        }
    )
    facet: List[Facet] = Field(
        default=list,
        metadata={
            "name": "Facet",
            "type": "Element",
            "namespace": "urn:be:cin:nippin:memberdata:saml:extension",
        }
    )

class AttributeStatement(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    model_config = ConfigDict(defer_build=True)

    attribute: List[Attribute] = Field(
        default_factory=list,
        metadata={
            "name": "Attribute",
            "type": "Element",
        }
    )

class Subject(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    model_config = ConfigDict(defer_build=True)

    name_id: Optional[NameId] = Field(
        default=None,
        metadata={
            "name": "NameID",
            "type": "Element",
        }
    )
    subject_confirmation: Optional[SubjectConfirmation] = Field(
        default=None,
        metadata={
            "name": "SubjectConfirmation",
            "type": "Element",
        }
    )

class Assertion(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    model_config = ConfigDict(defer_build=True)

    id: Optional[str] = Field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Attribute",
        }
    )
    issue_instant: Optional[XmlDateTime] = Field(
        default=None,
        metadata={
            "name": "IssueInstant",
            "type": "Attribute",
        }
    )
    version: Optional[Union[str, float]] = Field(
        default=None,
        metadata={
            "name": "Version",
            "type": "Attribute",
        }
    )
    issuer: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Issuer",
            "type": "Element",
        }
    )
    subject: Optional[Subject] = Field(
        default=None,
        metadata={
            "name": "Subject",
            "type": "Element",
        }
    )
    advice: Optional[Advice] = Field(
        default=None,
        metadata={
            "name": "Advice",
            "type": "Element",
        }
    )
    attribute_statement: Optional[AttributeStatement] = Field(
        default=None,
        metadata={
            "name": "AttributeStatement",
            "type": "Element",
        }
    )

class Response(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:protocol"

    model_config = ConfigDict(defer_build=True)

    id: Optional[str] = Field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Attribute",
        }
    )
    in_response_to: Optional[str] = Field(
        default=None,
        metadata={
            "name": "InResponseTo",
            "type": "Attribute",
        }
    )
    issue_instant: Optional[XmlDateTime] = Field(
        default=None,
        metadata={
            "name": "IssueInstant",
            "type": "Attribute",
        }
    )
    version: Optional[Union[str, float]] = Field(
        default=None,
        metadata={
            "name": "Version",
            "type": "Attribute",
        }
    )
    issuer: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Issuer",
            "type": "Element",
            "namespace": "urn:oasis:names:tc:SAML:2.0:assertion",
        }
    )
    status: Optional[Status] = Field(
        default=None,
        metadata={
            "name": "Status",
            "type": "Element",
        }
    )
    assertion: List[Assertion] = Field(
        default_factory=list,
        metadata={
            "name": "Assertion",
            "type": "Element",
            "namespace": "urn:oasis:names:tc:SAML:2.0:assertion",
        }
    )

class MemberData(BaseModel):
    model_config = ConfigDict(defer_build=True)
    response: Response
    transaction_request: str
    transaction_response: str
    soap_request: str
    soap_response: str