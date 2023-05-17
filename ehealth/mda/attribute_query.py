from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import List, Optional
from xsdata.models.datatype import XmlDateTime


@dataclass
class Dimension:
    class Meta:
        namespace = ""

    id: str = field(
        metadata={
            "type": "Attribute",
        }
    )
    value: str = field(
        default=""
    )


@dataclass
class Issuer:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    value: str
    format: Optional[str] = field(
        default="urn:be:cin:nippin:nihii11",
        metadata={
            "name": "Format",
            "type": "Attribute",
        }
    )


@dataclass
class NameId:
    class Meta:
        name = "NameID"
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    value: str
    format: Optional[str] = field(
        default="urn:be:fgov:person:ssin",
        metadata={
            "name": "Format",
            "type": "Attribute",
        }
    )


@dataclass
class SubjectConfirmationData:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    not_before: XmlDateTime = field(
        metadata={
            "name": "NotBefore",
            "type": "Attribute",
        }
    )
    not_on_or_after: XmlDateTime = field(
        metadata={
            "name": "NotOnOrAfter",
            "type": "Attribute",
        }
    )


@dataclass
class Facet:
    class Meta:
        namespace = "urn:be:cin:nippin:memberdata:saml:extension"

    id: str = field(
        metadata={
            "type": "Attribute",
        }
    )
    dimensions: List[Dimension] = field(
        default_factory=list,
        metadata={
            "name": "Dimension",
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass
class SubjectConfirmation:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    subject_confirmation_data: SubjectConfirmationData = field(
        metadata={
            "name": "SubjectConfirmationData",
            "type": "Element",
        }
    )
    method: Optional[str] = field(
        default="urn:be:cin:nippin:memberIdentification",
        metadata={
            "name": "Method",
            "type": "Attribute",
        }
    )

@dataclass
class Subject:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:assertion"

    name_id: NameId = field(
        metadata={
            "name": "NameID",
            "type": "Element",
        }
    )
    subject_confirmation: SubjectConfirmation = field(
        metadata={
            "name": "SubjectConfirmation",
            "type": "Element",
        }
    )


@dataclass
class Extensions:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:protocol"

    facets: List[Facet] = field(
        default_factory=list,
        metadata={
            "name": "Facet",
            "type": "Element",
            "namespace": "urn:be:cin:nippin:memberdata:saml:extension",
        }
    )
    type: Optional[str] = field(
        default="ext:ExtensionsType",
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/2001/XMLSchema-instance",
        }
    )

@dataclass
class AttributeQuery:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:2.0:protocol"


    issue_instant: XmlDateTime = field(
        metadata={
            "name": "IssueInstant",
            "type": "Attribute",
        }
    )
    id: str = field(
        metadata={
            "name": "ID",
            "type": "Attribute",
        }
    )
    issuer: Issuer = field(
        metadata={
            "name": "Issuer",
            "type": "Element",
            "namespace": "urn:oasis:names:tc:SAML:2.0:assertion",
        }
    )
    extensions: Extensions = field(
        metadata={
            "name": "Extensions",
            "type": "Element",
        }
    )
    subject: Subject = field(
        metadata={
            "name": "Subject",
            "type": "Element",
            "namespace": "urn:oasis:names:tc:SAML:2.0:assertion",
        }
    )
    version: Optional[float] = field(
        default=2.0,
        metadata={
            "name": "Version",
            "type": "Attribute",
        }
    )