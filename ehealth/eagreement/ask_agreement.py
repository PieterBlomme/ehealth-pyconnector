from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import List, Optional
from xsdata.models.datatype import XmlDateTime, XmlDate
from pydantic import ConfigDict

__NAMESPACE__ = "http://hl7.org/fhir"


@dataclass
class Created:
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

@dataclass
class End:
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

@dataclass
class Endpoint:
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

@dataclass
class Expression:
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

@dataclass
class Family:
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


@dataclass
class FullUrl:
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


@dataclass
class Gender:
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


@dataclass
class Given:
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


@dataclass
class Id:
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


@dataclass
class ItemSequence:
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


@dataclass
class Outcome:
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


@dataclass
class PreAuthRef:
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


@dataclass
class Profile:
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


@dataclass
class Reference:
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

@dataclass
class Severity:
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

@dataclass
class Start:
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

@dataclass
class Status:
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


@dataclass
class System:
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

@dataclass
class Text:
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

@dataclass
class Timestamp:
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


@dataclass
class Use:
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


@dataclass
class Value:
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


@dataclass
class Coding:
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


@dataclass
class Focus:
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


@dataclass
class Identifier:
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


@dataclass
class Insurer:
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


@dataclass
class MetaType:
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


@dataclass
class Name:
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


@dataclass
class Patient2:
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


@dataclass
class Practitioner2:
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

@dataclass
class PreAuthPeriod:
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

@dataclass
class Receiver:
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


@dataclass
class Requestor:
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


@dataclass
class Sender:
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


@dataclass
class Source:
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


@dataclass
class Organization:
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


@dataclass
class Patient1:
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


@dataclass
class Practitioner1:
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


@dataclass
class Category:
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


@dataclass
class Code:
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


@dataclass
class Destination:
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


@dataclass
class ProductOrService:
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


@dataclass
class Reason:
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


@dataclass
class SubType:
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


@dataclass
class TypeType:
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

@dataclass
class Details:
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

@dataclass
class PractitionerRole:
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


@dataclass
class Adjudication:
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


@dataclass
class EventCoding:
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


@dataclass
class Issue:
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

@dataclass
class Response:
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


@dataclass
class MessageHeader:
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


@dataclass
class AddItem:
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


@dataclass
class ClaimResponse:
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

@dataclass
class OperationOutcome:
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

@dataclass
class Resource:
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


@dataclass
class Entry:
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


@dataclass
class Bundle:
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

@dataclass(config=ConfigDict(extra='forbid'))
class Response:
    response: Bundle
    transaction_request: str
    transaction_response: str
    soap_request: str
    soap_response: str