from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from xsdata.models.datatype import XmlDate, XmlDateTime

__NAMESPACE__ = "http://hl7.org/fhir"


class Assigner(BaseModel):
    class Meta:
        name = "assigner"
        namespace = "http://hl7.org/fhir"

    identifier: Optional["Identifier"] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class Diagnostics(BaseModel):
    class Meta:
        name = "diagnostics"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class Location(BaseModel):
    class Meta:
        name = "location"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
     

class Created(BaseModel):
    class Meta:
        name = "created"
        namespace = "http://hl7.org/fhir"

    value: Optional[XmlDateTime] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )



class End(BaseModel):
    class Meta:
        name = "end"
        namespace = "http://hl7.org/fhir"

    value: Optional[XmlDate] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )



class Endpoint(BaseModel):
    class Meta:
        name = "endpoint"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )



class Family(BaseModel):
    class Meta:
        name = "family"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )



class FullUrl(BaseModel):
    class Meta:
        name = "fullUrl"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )



class Gender(BaseModel):
    class Meta:
        name = "gender"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )



class Given(BaseModel):
    class Meta:
        name = "given"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )



class Id(BaseModel):
    class Meta:
        name = "id"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )



class ItemSequence(BaseModel):
    class Meta:
        name = "itemSequence"
        namespace = "http://hl7.org/fhir"

    value: Optional[int] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )



class Mode(BaseModel):
    class Meta:
        name = "mode"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )



class Outcome(BaseModel):
    class Meta:
        name = "outcome"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )



class PreAuthRef(BaseModel):
    class Meta:
        name = "preAuthRef"
        namespace = "http://hl7.org/fhir"

    value: Optional[int] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )



class Profile(BaseModel):
    class Meta:
        name = "profile"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )



class Reference(BaseModel):
    class Meta:
        name = "reference"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class Severity(BaseModel):
    class Meta:
        name = "severity"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class Relation(BaseModel):
    class Meta:
        name = "relation"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )



class Start(BaseModel):
    class Meta:
        name = "start"
        namespace = "http://hl7.org/fhir"

    value: Optional[XmlDate] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )



class Status(BaseModel):
    class Meta:
        name = "status"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )



class System(BaseModel):
    class Meta:
        name = "system"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )



class Timestamp(BaseModel):
    class Meta:
        name = "timestamp"
        namespace = "http://hl7.org/fhir"

    value: Optional[XmlDateTime] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )



class Total(BaseModel):
    class Meta:
        name = "total"
        namespace = "http://hl7.org/fhir"

    value: Optional[int] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )



class Url(BaseModel):
    class Meta:
        name = "url"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )



class Use(BaseModel):
    class Meta:
        name = "use"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )



class Value(BaseModel):
    class Meta:
        name = "value"
        namespace = "http://hl7.org/fhir"

    value: Optional[int] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )



class Coding(BaseModel):
    class Meta:
        name = "coding"
        namespace = "http://hl7.org/fhir"

    system: Optional[System] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    code: Optional["Code"] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Focus(BaseModel):
    class Meta:
        name = "focus"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Identifier(BaseModel):
    class Meta:
        name = "identifier"
        namespace = "http://hl7.org/fhir"

    system: Optional[System] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    value: Optional[Value] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    value_attribute: Optional[str] = Field(
        default=None,
        metadata={
            "name": "value",
            "type": "Attribute",
        }
    )
    assigner: Optional[Assigner] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class Insurer(BaseModel):
    class Meta:
        name = "insurer"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Link(BaseModel):
    class Meta:
        name = "link"
        namespace = "http://hl7.org/fhir"

    relation: Optional[Relation] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    url: Optional[Url] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class MetaType(BaseModel):
    class Meta:
        name = "meta"
        namespace = "http://hl7.org/fhir"

    profile: Optional[Profile] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Name(BaseModel):
    class Meta:
        name = "name"
        namespace = "http://hl7.org/fhir"

    family: Optional[Family] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    given: Optional[Given] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )



class Patient2(BaseModel):
    class Meta:
        name = "patient"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Practitioner2(BaseModel):
    class Meta:
        name = "practitioner"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class PreAuthPeriod(BaseModel):
    class Meta:
        name = "preAuthPeriod"
        namespace = "http://hl7.org/fhir"

    start: Optional[Start] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    end: Optional[End] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Receiver(BaseModel):
    class Meta:
        name = "receiver"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Requestor(BaseModel):
    class Meta:
        name = "requestor"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Search(BaseModel):
    class Meta:
        name = "search"
        namespace = "http://hl7.org/fhir"

    mode: Optional[Mode] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Sender(BaseModel):
    class Meta:
        name = "sender"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Source(BaseModel):
    class Meta:
        name = "source"
        namespace = "http://hl7.org/fhir"

    endpoint: Optional[Endpoint] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Organization(BaseModel):
    class Meta:
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    meta: Optional[MetaType] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    identifier: Optional[Identifier] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    name: Optional[Name] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Patient1(BaseModel):
    class Meta:
        name = "Patient"
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    meta: Optional[MetaType] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    identifier: Optional[Identifier] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    name: Optional[Name] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    gender: Optional[Gender] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Practitioner1(BaseModel):
    class Meta:
        name = "Practitioner"
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    meta: Optional[MetaType] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    identifier: Optional[Identifier] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    name: Optional[Name] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Category(BaseModel):
    class Meta:
        name = "category"
        namespace = "http://hl7.org/fhir"

    coding: Optional[Coding] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Code(BaseModel):
    class Meta:
        name = "code"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    coding: Optional[Coding] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )



class Destination(BaseModel):
    class Meta:
        name = "destination"
        namespace = "http://hl7.org/fhir"

    endpoint: Optional[Endpoint] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    receiver: Optional[Receiver] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Entry(BaseModel):
    class Meta:
        name = "entry"
        namespace = "http://hl7.org/fhir"

    full_url: Optional[FullUrl] = Field(
        default=None,
        metadata={
            "name": "fullUrl",
            "type": "Element",
            "required": True,
        }
    )
    resource: Optional["Resource"] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    search: Optional[Search] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )



class ProductOrService(BaseModel):
    class Meta:
        name = "productOrService"
        namespace = "http://hl7.org/fhir"

    coding: Optional[Coding] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class SubType(BaseModel):
    class Meta:
        name = "subType"
        namespace = "http://hl7.org/fhir"

    coding: Optional[Coding] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class Reason(BaseModel):
    class Meta:
        name = "reason"
        namespace = "http://hl7.org/fhir"

    coding: Optional[Coding] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class TypeType(BaseModel):
    class Meta:
        name = "type"
        namespace = "http://hl7.org/fhir"

    coding: Optional[Coding] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )



class Bundle(BaseModel):
    class Meta:
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    meta: Optional[MetaType] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    type: Optional[TypeType] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    total: Optional[Total] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    link: Optional[Link] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    timestamp: Optional[Timestamp] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    entry: List[Entry] = Field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )


class Text(BaseModel):
    class Meta:
        name = "text"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class Details(BaseModel):
    class Meta:
        name = "details"
        namespace = "http://hl7.org/fhir"

    coding: Optional[Coding] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    text: Optional[Text] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class PractitionerRole(BaseModel):
    class Meta:
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    meta: Optional[MetaType] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    practitioner: Optional[Practitioner2] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    code: Optional[Code] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Adjudication(BaseModel):
    class Meta:
        name = "adjudication"
        namespace = "http://hl7.org/fhir"

    category: Optional[Category] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )

    reason: Optional[Reason] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class EventCoding(BaseModel):
    class Meta:
        name = "eventCoding"
        namespace = "http://hl7.org/fhir"

    system: Optional[System] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    code: Optional[Code] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class Expression(BaseModel):
    class Meta:
        name = "expression"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class Issue(BaseModel):
    class Meta:
        name = "issue"
        namespace = "http://hl7.org/fhir"

    severity: Optional[Severity] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    code: Optional[Code] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    details: Optional[Details] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    expression: Optional[Expression] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    diagnostics: Optional[Diagnostics] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    location: List[Location] = Field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )


class Response(BaseModel):
    class Meta:
        name = "response"
        namespace = "http://hl7.org/fhir"

    identifier: Optional[Identifier] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    code: Optional[Code] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class MessageHeader(BaseModel):
    class Meta:
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    meta: Optional[MetaType] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    event_coding: Optional[EventCoding] = Field(
        default=None,
        metadata={
            "name": "eventCoding",
            "type": "Element",
            "required": True,
        }
    )
    destination: Optional[Destination] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    sender: Optional[Sender] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    source: Optional[Source] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    response: Optional[Response] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    focus: Optional[Focus] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class AddItem(BaseModel):
    class Meta:
        name = "addItem"
        namespace = "http://hl7.org/fhir"

    item_sequence: Optional[ItemSequence] = Field(
        default=None,
        metadata={
            "name": "itemSequence",
            "type": "Element",
            "required": True,
        }
    )
    product_or_service: Optional[ProductOrService] = Field(
        default=None,
        metadata={
            "name": "productOrService",
            "type": "Element",
            "required": True,
        }
    )
    adjudication: Optional[Adjudication] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class ClaimResponse(BaseModel):
    class Meta:
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    meta: Optional[MetaType] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    status: Optional[Status] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    type: Optional[TypeType] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    sub_type: Optional[SubType] = Field(
        default=None,
        metadata={
            "name": "subType",
            "type": "Element",
            "required": True,
        }
    )
    use: Optional[Use] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    patient: Optional[Patient2] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    created: Optional[Created] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    insurer: Optional[Insurer] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    requestor: Optional[Requestor] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    outcome: Optional[Outcome] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    pre_auth_ref: Optional[PreAuthRef] = Field(
        default=None,
        metadata={
            "name": "preAuthRef",
            "type": "Element",
            "required": True,
        }
    )
    pre_auth_period: Optional[PreAuthPeriod] = Field(
        default=None,
        metadata={
            "name": "preAuthPeriod",
            "type": "Element",
            "required": True,
        }
    )
    add_item: Optional[AddItem] = Field(
        default=None,
        metadata={
            "name": "addItem",
            "type": "Element",
            "required": True,
        }
    )



class OperationOutcome(BaseModel):
    class Meta:
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    meta: Optional[MetaType] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    issue: List[Issue] = Field(
        default_factory=list,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class Resource(BaseModel):
    class Meta:
        name = "resource"
        namespace = "http://hl7.org/fhir"

    operation_outcome: Optional[OperationOutcome] = Field(
        default=None,
        metadata={
            "name": "OperationOutcome",
            "type": "Element",
        }
    )

    claim_response: Optional[ClaimResponse] = Field(
        default=None,
        metadata={
            "name": "ClaimResponse",
            "type": "Element",
        }
    )
    practitioner_role: Optional[PractitionerRole] = Field(
        default=None,
        metadata={
            "name": "PractitionerRole",
            "type": "Element",
        }
    )
    practitioner: Optional[Practitioner1] = Field(
        default=None,
        metadata={
            "name": "Practitioner",
            "type": "Element",
        }
    )
    patient: Optional[Patient1] = Field(
        default=None,
        metadata={
            "name": "Patient",
            "type": "Element",
        }
    )
    organization: Optional[Organization] = Field(
        default=None,
        metadata={
            "name": "Organization",
            "type": "Element",
        }
    )
    bundle: Optional[Bundle] = Field(
        default=None,
        metadata={
            "name": "Bundle",
            "type": "Element",
        }
    )
    message_header: Optional[MessageHeader] = Field(
        default=None,
        metadata={
            "name": "MessageHeader",
            "type": "Element",
        }
    )


class Response(BaseModel):
    model_config = ConfigDict(extra='forbid')
    response: Bundle
    transaction_request: str
    transaction_response: str
    soap_request: str
    soap_response: str