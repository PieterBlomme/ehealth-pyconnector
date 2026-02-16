from pydantic import BaseModel, ConfigDict
from xsdata_pydantic.fields import field
from typing import List, Optional
from xsdata.models.datatype import XmlDateTime, XmlDate

__NAMESPACE__ = "http://hl7.org/fhir"


class Created(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "created"
        namespace = "http://hl7.org/fhir"

    value: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )

class End(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "end"
        namespace = "http://hl7.org/fhir"

    value: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )

class Endpoint(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "endpoint"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )

class Expression(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "expression"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )

class Family(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "family"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class FullUrl(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "fullUrl"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class Gender(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "gender"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class Given(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "given"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class Id(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "id"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class ItemSequence(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "itemSequence"
        namespace = "http://hl7.org/fhir"

    value: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class Outcome(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "outcome"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class PreAuthRef(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "preAuthRef"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class Profile(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "profile"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class Reference(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "reference"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )

class Severity(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "severity"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )

class Start(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "start"
        namespace = "http://hl7.org/fhir"

    value: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )

class Status(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "status"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class System(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "system"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )

class Text(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "text"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )

class Timestamp(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "timestamp"
        namespace = "http://hl7.org/fhir"

    value: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class Use(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "use"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class Value(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "value"
        namespace = "http://hl7.org/fhir"

    value: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class Coding(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "coding"
        namespace = "http://hl7.org/fhir"

    system: Optional[System] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    code: Optional["Code"] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class Focus(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "focus"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class Identifier(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "identifier"
        namespace = "http://hl7.org/fhir"

    system: Optional[System] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    value: Optional[Value] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    value_attribute: Optional[str] = field(
        default=None,
        metadata={
            "name": "value",
            "type": "Attribute",
        }
    )


class Insurer(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "insurer"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class MetaType(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "meta"
        namespace = "http://hl7.org/fhir"

    profile: Optional[Profile] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class Name(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "name"
        namespace = "http://hl7.org/fhir"

    family: Optional[Family] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    given: Optional[Given] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


class Patient2(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "patient"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class Practitioner2(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "practitioner"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )

class PreAuthPeriod(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "preAuthPeriod"
        namespace = "http://hl7.org/fhir"

    start: Optional[Start] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    end: Optional[End] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )

class Receiver(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "receiver"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class Requestor(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "requestor"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class Sender(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "sender"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class Source(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "source"
        namespace = "http://hl7.org/fhir"

    endpoint: Optional[Endpoint] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class Organization(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    meta: Optional[MetaType] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    identifier: Optional[Identifier] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class Patient1(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "Patient"
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    meta: Optional[MetaType] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    identifier: Optional[Identifier] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    gender: Optional[Gender] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class Practitioner1(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "Practitioner"
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    meta: Optional[MetaType] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    identifier: Optional[Identifier] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class Category(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "category"
        namespace = "http://hl7.org/fhir"

    coding: Optional[Coding] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class Code(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "code"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    coding: Optional[Coding] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class Destination(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "destination"
        namespace = "http://hl7.org/fhir"

    endpoint: Optional[Endpoint] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    receiver: Optional[Receiver] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class ProductOrService(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "productOrService"
        namespace = "http://hl7.org/fhir"

    coding: Optional[Coding] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class Reason(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "reason"
        namespace = "http://hl7.org/fhir"

    coding: Optional[Coding] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class SubType(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "subType"
        namespace = "http://hl7.org/fhir"

    coding: Optional[Coding] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class TypeType(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "type"
        namespace = "http://hl7.org/fhir"

    coding: Optional[Coding] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )

class Details(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "details"
        namespace = "http://hl7.org/fhir"

    coding: Optional[Coding] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    text: Optional[Text] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )

class PractitionerRole(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    meta: Optional[MetaType] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    practitioner: Optional[Practitioner2] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    code: Optional[Code] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class Adjudication(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "adjudication"
        namespace = "http://hl7.org/fhir"

    category: Optional[Category] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    reason: Optional[Reason] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class EventCoding(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "eventCoding"
        namespace = "http://hl7.org/fhir"

    system: Optional[System] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    code: Optional[Code] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class Issue(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "issue"
        namespace = "http://hl7.org/fhir"

    severity: Optional[Severity] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    code: Optional[Code] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    details: Optional[Details] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    expression: Optional[Expression] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )

class Response(BaseModel):
    model_config = ConfigDict(extra='forbid', defer_build=True)

    class Meta:
        name = "response"
        namespace = "http://hl7.org/fhir"

    identifier: Optional[Identifier] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    code: Optional[Code] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class MessageHeader(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    meta: Optional[MetaType] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    event_coding: Optional[EventCoding] = field(
        default=None,
        metadata={
            "name": "eventCoding",
            "type": "Element",
            "required": True,
        }
    )
    destination: Optional[Destination] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    sender: Optional[Sender] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    source: Optional[Source] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    response: Optional[Response] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    focus: Optional[Focus] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class AddItem(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "addItem"
        namespace = "http://hl7.org/fhir"

    item_sequence: Optional[ItemSequence] = field(
        default=None,
        metadata={
            "name": "itemSequence",
            "type": "Element",
            "required": True,
        }
    )
    product_or_service: Optional[ProductOrService] = field(
        default=None,
        metadata={
            "name": "productOrService",
            "type": "Element",
            "required": True,
        }
    )
    adjudication: Optional[Adjudication] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class ClaimResponse(BaseModel):
    model_config = ConfigDict(extra='forbid', defer_build=True)

    class Meta:
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    meta: Optional[MetaType] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    status: Optional[Status] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    type: Optional[TypeType] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    sub_type: Optional[SubType] = field(
        default=None,
        metadata={
            "name": "subType",
            "type": "Element",
            "required": True,
        }
    )
    use: Optional[Use] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    patient: Optional[Patient2] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    created: Optional[Created] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    insurer: Optional[Insurer] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    requestor: Optional[Requestor] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    outcome: Optional[Outcome] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    pre_auth_ref: Optional[PreAuthRef] = field(
        default=None,
        metadata={
            "name": "preAuthRef",
            "type": "Element",
            "required": True,
        }
    )
    pre_auth_period: Optional[PreAuthPeriod] = field(
        default=None,
        metadata={
            "name": "preAuthPeriod",
            "type": "Element",
            "required": True,
        }
    )
    add_item: Optional[AddItem] = field(
        default=None,
        metadata={
            "name": "addItem",
            "type": "Element",
            "required": True,
        }
    )

class OperationOutcome(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    meta: Optional[MetaType] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    issue: List[Issue] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "required": True,
        }
    )

class Resource(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "resource"
        namespace = "http://hl7.org/fhir"

    operation_outcome: Optional[OperationOutcome] = field(
        default=None,
        metadata={
            "name": "OperationOutcome",
            "type": "Element",
        }
    )

    claim_response: Optional[ClaimResponse] = field(
        default=None,
        metadata={
            "name": "ClaimResponse",
            "type": "Element",
        }
    )
    patient: Optional[Patient1] = field(
        default=None,
        metadata={
            "name": "Patient",
            "type": "Element",
        }
    )
    practitioner_role: Optional[PractitionerRole] = field(
        default=None,
        metadata={
            "name": "PractitionerRole",
            "type": "Element",
        }
    )
    practitioner: Optional[Practitioner1] = field(
        default=None,
        metadata={
            "name": "Practitioner",
            "type": "Element",
        }
    )
    organization: Optional[Organization] = field(
        default=None,
        metadata={
            "name": "Organization",
            "type": "Element",
        }
    )
    message_header: Optional[MessageHeader] = field(
        default=None,
        metadata={
            "name": "MessageHeader",
            "type": "Element",
        }
    )


class Entry(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "entry"
        namespace = "http://hl7.org/fhir"

    full_url: Optional[FullUrl] = field(
        default=None,
        metadata={
            "name": "fullUrl",
            "type": "Element",
            "required": True,
        }
    )
    resource: Optional[Resource] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class Bundle(BaseModel):
    model_config = ConfigDict(extra='forbid', defer_build=True)

    class Meta:
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    meta: Optional[MetaType] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    type: Optional[TypeType] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    timestamp: Optional[Timestamp] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    entry: List[Entry] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )
