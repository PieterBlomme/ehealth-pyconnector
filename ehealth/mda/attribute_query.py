from pydantic import BaseModel, Field
from typing import List, Optional
from xsdata.models.datatype import XmlDateTime


class Dimension(BaseModel):
    class Meta:
        namespace = ""

    id: str = Field(
        metadata={
            "type": "Attribute",
        }
    )
    value: str = Field(
        default=""
    )


class Issuer(BaseModel):
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    value: str
    format: Optional[str] = Field(
        default="urn:be:cin:nippin:nihii11",
        metadata={
            "name": "Format",
            "type": "Attribute",
        }
    )


class NameId(BaseModel):
    class Meta:
        name = "NameID"
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    value: str
    format: Optional[str] = Field(
        default="urn:be:fgov:person:ssin",
        metadata={
            "name": "Format",
            "type": "Attribute",
        }
    )


class SubjectConfirmationData(BaseModel):
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    not_before: XmlDateTime = Field(
        metadata={
            "name": "NotBefore",
            "type": "Attribute",
        }
    )
    not_on_or_after: XmlDateTime = Field(
        metadata={
            "name": "NotOnOrAfter",
            "type": "Attribute",
        }
    )


class Facet(BaseModel):
    class Meta:
        namespace = "urn:be:cin:nippin:memberdata:saml:extension"

    id: str = Field(
        metadata={
            "type": "Attribute",
        }
    )
    dimensions: List[Dimension] = Field(
        default_factory=list,
        metadata={
            "name": "Dimension",
            "type": "Element",
            "namespace": "",
        }
    )


class SubjectConfirmation(BaseModel):
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    subject_confirmation_data: SubjectConfirmationData = Field(
        metadata={
            "name": "SubjectConfirmationData",
            "type": "Element",
        }
    )
    method: Optional[str] = Field(
        default="urn:be:cin:nippin:memberIdentification",
        metadata={
            "name": "Method",
            "type": "Attribute",
        }
    )

class Subject(BaseModel):
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    name_id: NameId = Field(
        metadata={
            "name": "NameID",
            "type": "Element",
        }
    )
    subject_confirmation: SubjectConfirmation = Field(
        metadata={
            "name": "SubjectConfirmation",
            "type": "Element",
        }
    )


class Extensions(BaseModel):
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:protocol"

    facets: List[Facet] = Field(
        default_factory=list,
        metadata={
            "name": "Facet",
            "type": "Element",
            "namespace": "urn:be:cin:nippin:memberdata:saml:extension",
        }
    )
    type: Optional[str] = Field(
        default="ext:ExtensionsType",
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/2001/XMLSchema-instance",
        }
    )

class AttributeQuery(BaseModel):
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:protocol"


    issue_instant: XmlDateTime = Field(
        metadata={
            "name": "IssueInstant",
            "type": "Attribute",
        }
    )
    id: str = Field(
        metadata={
            "name": "ID",
            "type": "Attribute",
        }
    )
    issuer: Issuer = Field(
        metadata={
            "name": "Issuer",
            "type": "Element",
            "namespace": "urn:oasis:names:tc:SAML:2.0:assertion",
        }
    )
    extensions: Extensions = Field(
        metadata={
            "name": "Extensions",
            "type": "Element",
        }
    )
    subject: Subject = Field(
        metadata={
            "name": "Subject",
            "type": "Element",
            "namespace": "urn:oasis:names:tc:SAML:2.0:assertion",
        }
    )
    version: Optional[float] = Field(
        default=2.0,
        metadata={
            "name": "Version",
            "type": "Attribute",
        }
    )