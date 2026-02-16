from pydantic import BaseModel, Field

from typing import List, Optional
from xsdata.models.datatype import XmlDateTime


class Description(BaseModel):
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    lang: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
            "required": True,
        }
    )
    value: str = Field(
        default="",
        metadata={
            "required": True,
        }
    )


class HealthCareAdditionalInformation(BaseModel):
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    type: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Attribute",
            "required": True,
        }
    )
    value: str = Field(
        default="",
        metadata={
            "required": True,
        }
    )


class ProfessionCode(BaseModel):
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    authentic_source: Optional[str] = Field(
        default=None,
        metadata={
            "name": "authenticSource",
            "type": "Attribute",
            "required": True,
        }
    )
    type: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    value: str = Field(
        default="",
        metadata={
            "required": True,
        }
    )


class ProfessionFriendlyName(BaseModel):
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    lang: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
            "required": True,
        }
    )
    value: str = Field(
        default="",
        metadata={
            "required": True,
        }
    )


class StatusCode(BaseModel):
    class Meta:
        namespace = "urn:be:fgov:ehealth:commons:core:v2"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Attribute",
            "required": True,
        }
    )


class Country(BaseModel):
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    isocode: Optional[str] = Field(
        default=None,
        metadata={
            "name": "ISOCode",
            "type": "Element",
            "required": True,
        }
    )
    description: List[Description] = Field(
        default_factory=list,
        metadata={
            "name": "Description",
            "type": "Element",
            "min_occurs": 1,
        }
    )


class Municipality(BaseModel):
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    zip_code: Optional[int] = Field(
        default=None,
        metadata={
            "name": "ZipCode",
            "type": "Element",
            "required": True,
        }
    )
    description: Optional[Description] = Field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "required": True,
        }
    )


class Profession(BaseModel):
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    profession_code: Optional[ProfessionCode] = Field(
        default=None,
        metadata={
            "name": "ProfessionCode",
            "type": "Element",
            "required": True,
        }
    )
    profession_friendly_name: List[ProfessionFriendlyName] = Field(
        default_factory=list,
        metadata={
            "name": "ProfessionFriendlyName",
            "type": "Element",
            "min_occurs": 1,
        }
    )
    nihii: Optional[str] = Field(
        default=None,
        metadata={
            "name": "NIHII",
            "type": "Element",
            "required": True,
        }
    )


class Street(BaseModel):
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    description: Optional[Description] = Field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "required": True,
        }
    )


class Status(BaseModel):
    class Meta:
        namespace = "urn:be:fgov:ehealth:commons:core:v2"

    status_code: Optional[StatusCode] = Field(
        default=None,
        metadata={
            "name": "StatusCode",
            "type": "Element",
            "required": True,
        }
    )


class Address(BaseModel):
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    type: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Attribute",
            "required": True,
        }
    )
    street: Optional[Street] = Field(
        default=None,
        metadata={
            "name": "Street",
            "type": "Element",
            "required": True,
        }
    )
    house_number: Optional[str] = Field(
        default=None,
        metadata={
            "name": "HouseNumber",
            "type": "Element",
            "required": True,
        }
    )
    municipality: Optional[Municipality] = Field(
        default=None,
        metadata={
            "name": "Municipality",
            "type": "Element",
            "required": True,
        }
    )
    country: Optional[Country] = Field(
        default=None,
        metadata={
            "name": "Country",
            "type": "Element",
            "required": True,
        }
    )


class ProfessionalInformation(BaseModel):
    class Meta:
        namespace = "urn:be:fgov:ehealth:addressbook:core:v1"

    profession: Optional[Profession] = Field(
        default=None,
        metadata={
            "name": "Profession",
            "type": "Element",
            "namespace": "urn:be:fgov:ehealth:aa:complextype:v1",
            "required": True,
        }
    )
    address: Optional[Address] = Field(
        default=None,
        metadata={
            "name": "Address",
            "type": "Element",
            "namespace": "urn:be:fgov:ehealth:aa:complextype:v1",
            "required": True,
        }
    )
    health_care_additional_information: Optional[HealthCareAdditionalInformation] = Field(
        default=None,
        metadata={
            "name": "HealthCareAdditionalInformation",
            "type": "Element",
            "namespace": "urn:be:fgov:ehealth:aa:complextype:v1",
            "required": True,
        }
    )


class IndividualContactInformation(BaseModel):
    class Meta:
        namespace = "urn:be:fgov:ehealth:addressbook:protocol:v1"

    last_name: Optional[str] = Field(
        default=None,
        metadata={
            "name": "LastName",
            "type": "Element",
            "namespace": "urn:be:fgov:ehealth:aa:complextype:v1",
            "required": True,
        }
    )
    first_name: Optional[str] = Field(
        default=None,
        metadata={
            "name": "FirstName",
            "type": "Element",
            "namespace": "urn:be:fgov:ehealth:aa:complextype:v1",
            "required": True,
        }
    )
    middle_names: Optional[str] = Field(
        default=None,
        metadata={
            "name": "MiddleNames",
            "type": "Element",
            "namespace": "urn:be:fgov:ehealth:aa:complextype:v1",
            "required": True,
        }
    )
    language: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Language",
            "type": "Element",
            "namespace": "urn:be:fgov:ehealth:aa:complextype:v1",
            "required": True,
        }
    )
    gender: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Gender",
            "type": "Element",
            "namespace": "urn:be:fgov:ehealth:aa:complextype:v1",
            "required": True,
        }
    )
    birth_date: Optional[str] = Field(
        default=None,
        metadata={
            "name": "BirthDate",
            "type": "Element",
            "namespace": "urn:be:fgov:ehealth:aa:complextype:v1",
            "required": True,
        }
    )
    professional_information: Optional[ProfessionalInformation] = Field(
        default=None,
        metadata={
            "name": "ProfessionalInformation",
            "type": "Element",
            "namespace": "urn:be:fgov:ehealth:addressbook:core:v1",
            "required": True,
        }
    )


class GetProfessionalContactInfoResponse(BaseModel):
    class Meta:
        namespace = "urn:be:fgov:ehealth:addressbook:protocol:v1"

    id: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Attribute",
            "required": True,
        }
    )
    issue_instant: Optional[XmlDateTime] = Field(
        default=None,
        metadata={
            "name": "IssueInstant",
            "type": "Attribute",
            "required": True,
        }
    )
    status: Optional[Status] = Field(
        default=None,
        metadata={
            "name": "Status",
            "type": "Element",
            "namespace": "urn:be:fgov:ehealth:commons:core:v2",
            "required": True,
        }
    )
    individual_contact_information: Optional[IndividualContactInformation] = Field(
        default=None,
        metadata={
            "name": "IndividualContactInformation",
            "type": "Element",
            "required": True,
        }
    )
