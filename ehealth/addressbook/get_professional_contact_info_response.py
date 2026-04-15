
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Union
from xsdata.models.datatype import XmlDateTime

class Description(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    model_config = ConfigDict(defer_build=True)

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
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    model_config = ConfigDict(defer_build=True)

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
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    model_config = ConfigDict(defer_build=True)

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
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    model_config = ConfigDict(defer_build=True)

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
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:be:fgov:ehealth:commons:core:v2"

    model_config = ConfigDict(defer_build=True)

    value: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Attribute",
            "required": True,
        }
    )

class Country(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    model_config = ConfigDict(defer_build=True)

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
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    model_config = ConfigDict(defer_build=True)

    zip_code: Optional[Union[str, int]] = Field(
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
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    model_config = ConfigDict(defer_build=True)

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
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    model_config = ConfigDict(defer_build=True)

    description: Optional[Description] = Field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "required": True,
        }
    )

class Status(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:be:fgov:ehealth:commons:core:v2"

    model_config = ConfigDict(defer_build=True)

    status_code: Optional[StatusCode] = Field(
        default=None,
        metadata={
            "name": "StatusCode",
            "type": "Element",
            "required": True,
        }
    )

class Address(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    model_config = ConfigDict(defer_build=True)

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
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:be:fgov:ehealth:addressbook:core:v1"

    model_config = ConfigDict(defer_build=True)

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
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:be:fgov:ehealth:addressbook:protocol:v1"

    model_config = ConfigDict(defer_build=True)

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
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "urn:be:fgov:ehealth:addressbook:protocol:v1"

    model_config = ConfigDict(defer_build=True)

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
