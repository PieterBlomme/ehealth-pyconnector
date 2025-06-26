from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import List, Optional
from xsdata.models.datatype import XmlDateTime


@dataclass
class Description:
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
            "required": True,
        }
    )
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@dataclass
class HealthCareAdditionalInformation:
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    type: Optional[str] = field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Attribute",
            "required": True,
        }
    )
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@dataclass
class ProfessionCode:
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    authentic_source: Optional[str] = field(
        default=None,
        metadata={
            "name": "authenticSource",
            "type": "Attribute",
            "required": True,
        }
    )
    type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@dataclass
class ProfessionFriendlyName:
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
            "required": True,
        }
    )
    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@dataclass
class StatusCode:
    class Meta:
        namespace = "urn:be:fgov:ehealth:commons:core:v2"

    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class Country:
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    isocode: Optional[str] = field(
        default=None,
        metadata={
            "name": "ISOCode",
            "type": "Element",
            "required": True,
        }
    )
    description: List[Description] = field(
        default_factory=list,
        metadata={
            "name": "Description",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass
class Municipality:
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    zip_code: Optional[int] = field(
        default=None,
        metadata={
            "name": "ZipCode",
            "type": "Element",
            "required": True,
        }
    )
    description: Optional[Description] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Profession:
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    profession_code: Optional[ProfessionCode] = field(
        default=None,
        metadata={
            "name": "ProfessionCode",
            "type": "Element",
            "required": True,
        }
    )
    profession_friendly_name: List[ProfessionFriendlyName] = field(
        default_factory=list,
        metadata={
            "name": "ProfessionFriendlyName",
            "type": "Element",
            "min_occurs": 1,
        }
    )
    nihii: Optional[str] = field(
        default=None,
        metadata={
            "name": "NIHII",
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Street:
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    description: Optional[Description] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Status:
    class Meta:
        namespace = "urn:be:fgov:ehealth:commons:core:v2"

    status_code: Optional[StatusCode] = field(
        default=None,
        metadata={
            "name": "StatusCode",
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Address:
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    type: Optional[str] = field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Attribute",
            "required": True,
        }
    )
    street: Optional[Street] = field(
        default=None,
        metadata={
            "name": "Street",
            "type": "Element",
            "required": True,
        }
    )
    house_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "HouseNumber",
            "type": "Element",
            "required": True,
        }
    )
    municipality: Optional[Municipality] = field(
        default=None,
        metadata={
            "name": "Municipality",
            "type": "Element",
            "required": True,
        }
    )
    country: Optional[Country] = field(
        default=None,
        metadata={
            "name": "Country",
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class ProfessionalInformation:
    class Meta:
        namespace = "urn:be:fgov:ehealth:addressbook:core:v1"

    profession: Optional[Profession] = field(
        default=None,
        metadata={
            "name": "Profession",
            "type": "Element",
            "namespace": "urn:be:fgov:ehealth:aa:complextype:v1",
            "required": True,
        }
    )
    address: Optional[Address] = field(
        default=None,
        metadata={
            "name": "Address",
            "type": "Element",
            "namespace": "urn:be:fgov:ehealth:aa:complextype:v1",
            "required": True,
        }
    )
    health_care_additional_information: Optional[HealthCareAdditionalInformation] = field(
        default=None,
        metadata={
            "name": "HealthCareAdditionalInformation",
            "type": "Element",
            "namespace": "urn:be:fgov:ehealth:aa:complextype:v1",
            "required": True,
        }
    )


@dataclass
class IndividualContactInformation:
    class Meta:
        namespace = "urn:be:fgov:ehealth:addressbook:protocol:v1"

    last_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastName",
            "type": "Element",
            "namespace": "urn:be:fgov:ehealth:aa:complextype:v1",
            "required": True,
        }
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FirstName",
            "type": "Element",
            "namespace": "urn:be:fgov:ehealth:aa:complextype:v1",
            "required": True,
        }
    )
    middle_names: Optional[str] = field(
        default=None,
        metadata={
            "name": "MiddleNames",
            "type": "Element",
            "namespace": "urn:be:fgov:ehealth:aa:complextype:v1",
            "required": True,
        }
    )
    language: Optional[str] = field(
        default=None,
        metadata={
            "name": "Language",
            "type": "Element",
            "namespace": "urn:be:fgov:ehealth:aa:complextype:v1",
            "required": True,
        }
    )
    gender: Optional[str] = field(
        default=None,
        metadata={
            "name": "Gender",
            "type": "Element",
            "namespace": "urn:be:fgov:ehealth:aa:complextype:v1",
            "required": True,
        }
    )
    birth_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "BirthDate",
            "type": "Element",
            "namespace": "urn:be:fgov:ehealth:aa:complextype:v1",
            "required": True,
        }
    )
    professional_information: Optional[ProfessionalInformation] = field(
        default=None,
        metadata={
            "name": "ProfessionalInformation",
            "type": "Element",
            "namespace": "urn:be:fgov:ehealth:addressbook:core:v1",
            "required": True,
        }
    )


@dataclass
class GetProfessionalContactInfoResponse:
    class Meta:
        namespace = "urn:be:fgov:ehealth:addressbook:protocol:v1"

    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
            "required": True,
        }
    )
    issue_instant: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "IssueInstant",
            "type": "Attribute",
            "required": True,
        }
    )
    status: Optional[Status] = field(
        default=None,
        metadata={
            "name": "Status",
            "type": "Element",
            "namespace": "urn:be:fgov:ehealth:commons:core:v2",
            "required": True,
        }
    )
    individual_contact_information: Optional[IndividualContactInformation] = field(
        default=None,
        metadata={
            "name": "IndividualContactInformation",
            "type": "Element",
            "required": True,
        }
    )
