from pydantic import BaseModel, ConfigDict
from xsdata_pydantic.fields import field

from typing import List, Optional
from xsdata.models.datatype import XmlDateTime


class ProfessionCode(BaseModel):
    model_config = ConfigDict(defer_build=True)

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


class ProfessionFriendlyName(BaseModel):
    model_config = ConfigDict(defer_build=True)

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


class StatusCode(BaseModel):
    model_config = ConfigDict(defer_build=True)

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

    status_code: Optional["StatusCode"] = field(
        default=None,
        metadata={
            "name": "StatusCode",
            "type": "Element",
        }
    )
    
class Profession(BaseModel):
    model_config = ConfigDict(defer_build=True)

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
    nihii: Optional[int] = field(
        default=None,
        metadata={
            "name": "NIHII",
            "type": "Element",
        }
    )


class Status(BaseModel):
    model_config = ConfigDict(defer_build=True)

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

    status_message: Optional[str] = field(
        default=None,
        metadata={
            "name": "StatusMessage",
            "type": "Element",
            "required": True,
        }
    )
    
class HealthCareProfessional(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        namespace = "urn:be:fgov:ehealth:aa:complextype:v1"

    ssin: Optional[int] = field(
        default=None,
        metadata={
            "name": "SSIN",
            "type": "Element",
        }
    )
    last_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LastName",
            "type": "Element",
            "required": True,
        }
    )
    first_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FirstName",
            "type": "Element",
            "required": True,
        }
    )
    middle_names: Optional[str] = field(
        default=None,
        metadata={
            "name": "MiddleNames",
            "type": "Element",
            "required": True,
        }
    )
    language: Optional[str] = field(
        default=None,
        metadata={
            "name": "Language",
            "type": "Element",
            "required": True,
        }
    )
    gender: Optional[str] = field(
        default=None,
        metadata={
            "name": "Gender",
            "type": "Element",
            "required": True,
        }
    )
    birth_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "BirthDate",
            "type": "Element",
            "required": True,
        }
    )
    death_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "DeathDate",
            "type": "Element",
        }
    )
    profession: Optional[Profession] = field(
        default=None,
        metadata={
            "name": "Profession",
            "type": "Element",
            "required": True,
        }
    )


class SearchProfessionalsResponse(BaseModel):
    model_config = ConfigDict(extra='forbid', defer_build=True)

    class Meta:
        namespace = "urn:be:fgov:ehealth:addressbook:protocol:v1"

    offset: Optional[int] = field(
        default=None,
        metadata={
            "name": "Offset",
            "type": "Attribute",
            "required": True,
        }
    )
    max_elements: Optional[int] = field(
        default=None,
        metadata={
            "name": "MaxElements",
            "type": "Attribute",
            "required": True,
        }
    )
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
    health_care_professional: List[HealthCareProfessional] = field(
        default_factory=list,
        metadata={
            "name": "HealthCareProfessional",
            "type": "Element",
            "namespace": "urn:be:fgov:ehealth:aa:complextype:v1",
            "min_occurs": 1,
        }
    )
