from pydantic import BaseModel, Field

from typing import List, Optional
from xsdata.models.datatype import XmlDateTime


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

    status_code: Optional["StatusCode"] = Field(
        default=None,
        metadata={
            "name": "StatusCode",
            "type": "Element",
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
    nihii: Optional[int] = Field(
        default=None,
        metadata={
            "name": "NIHII",
            "type": "Element",
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

    status_message: Optional[str] = Field(
        default=None,
        metadata={
            "name": "StatusMessage",
            "type": "Element",
            "required": True,
        }
    )
    
class HealthCareProfessional(BaseModel):
    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    ssin: Optional[int] = Field(
        default=None,
        metadata={
            "name": "SSIN",
            "type": "Element",
        }
    )
    last_name: Optional[str] = Field(
        default=None,
        metadata={
            "name": "LastName",
            "type": "Element",
            "required": True,
        }
    )
    first_name: Optional[str] = Field(
        default=None,
        metadata={
            "name": "FirstName",
            "type": "Element",
            "required": True,
        }
    )
    middle_names: Optional[str] = Field(
        default=None,
        metadata={
            "name": "MiddleNames",
            "type": "Element",
            "required": True,
        }
    )
    language: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Language",
            "type": "Element",
            "required": True,
        }
    )
    gender: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Gender",
            "type": "Element",
            "required": True,
        }
    )
    birth_date: Optional[str] = Field(
        default=None,
        metadata={
            "name": "BirthDate",
            "type": "Element",
            "required": True,
        }
    )
    death_date: Optional[str] = Field(
        default=None,
        metadata={
            "name": "DeathDate",
            "type": "Element",
        }
    )
    profession: Optional[Profession] = Field(
        default=None,
        metadata={
            "name": "Profession",
            "type": "Element",
            "required": True,
        }
    )


class SearchProfessionalsResponse(BaseModel):
    class Meta:
        namespace = "urn:be:fgov:ehealth:addressbook:protocol:v1"

    offset: Optional[int] = Field(
        default=None,
        metadata={
            "name": "Offset",
            "type": "Attribute",
            "required": True,
        }
    )
    max_elements: Optional[int] = Field(
        default=None,
        metadata={
            "name": "MaxElements",
            "type": "Attribute",
            "required": True,
        }
    )
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
    health_care_professional: List[HealthCareProfessional] = Field(
        default_factory=list,
        metadata={
            "name": "HealthCareProfessional",
            "type": "Element",
            "namespace": "urn:be:fgov:ehealth:aa:complextype:v1",
            "min_occurs": 1,
        }
    )
