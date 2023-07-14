from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import List, Optional, Union
from xsdata.models.datatype import XmlDate, XmlDateTime


@dataclass
class Assigner:
    class Meta:
        name = "assigner"
        namespace = "http://hl7.org/fhir"

    identifier: Optional["Identifier"] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class AuthoredOn:
    class Meta:
        name = "authoredOn"
        namespace = "http://hl7.org/fhir"

    value: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class ContentType:
    class Meta:
        name = "contentType"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Created:
    class Meta:
        name = "created"
        namespace = "http://hl7.org/fhir"

    value: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Data:
    class Meta:
        name = "data"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Display:
    class Meta:
        name = "display"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
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
        }
    )


@dataclass
class Focal:
    class Meta:
        name = "focal"
        namespace = "http://hl7.org/fhir"

    value: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
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
        }
    )


@dataclass
class Intent:
    class Meta:
        name = "intent"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
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
        }
    )


@dataclass
class Sequence:
    class Meta:
        name = "sequence"
        namespace = "http://hl7.org/fhir"

    value: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class ServicedDate:
    class Meta:
        name = "servicedDate"
        namespace = "http://hl7.org/fhir"

    value: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Attribute",
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
        }
    )


@dataclass
class Title:
    class Meta:
        name = "title"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
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
        }
    )


@dataclass
class Value:
    class Meta:
        name = "value"
        namespace = "http://hl7.org/fhir"

    value: Optional[Union[str, int]] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class ValueString:
    class Meta:
        name = "valueString"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class A:
    class Meta:
        name = "a"
        namespace = "http://www.w3.org/1999/xhtml"

    href: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    value: str = field(
        default=""
    )


@dataclass
class Binary:
    class Meta:
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    content_type: Optional[ContentType] = field(
        default=None,
        metadata={
            "name": "contentType",
            "type": "Element",
        }
    )
    data: Optional[Data] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class BillablePeriod:
    class Meta:
        name = "billablePeriod"
        namespace = "http://hl7.org/fhir"

    start: Optional[Start] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )

@dataclass
class Code:
    class Meta:
        name = "code"
        namespace = "http://hl7.org/fhir"

    value: Optional[Union[str, int]] = field(
        default=None,
        metadata={
            "type": "Attribute",
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
        }
    )
    code: Optional["Code"] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    display: Optional[Display] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )

@dataclass
class NestedCode:
    class Meta:
        name = "code"
        namespace = "http://hl7.org/fhir"

    coding: Optional[Coding] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )

@dataclass
class Coverage:
    class Meta:
        name = "coverage"
        namespace = "http://hl7.org/fhir"

    display: Optional[Display] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class Enterer:
    class Meta:
        name = "enterer"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = field(
        default=None,
        metadata={
            "type": "Element",
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
    assigner: Optional[Assigner] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class MetaType:
    class Meta:
        name = "meta"
        namespace = "http://hl7.org/fhir"

    profile: Optional[Profile] = field(
        default=Profile("http://www.mycarenet.be/standards/fhir/StructureDefinition/be-eagreementdemand"),
        metadata={
            "type": "Element",
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
        }
    )


@dataclass
class Provider:
    class Meta:
        name = "provider"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class QuantityQuantity:
    class Meta:
        name = "quantityQuantity"
        namespace = "http://hl7.org/fhir"

    value: Optional[Value] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class Referral:
    class Meta:
        name = "referral"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class Requester:
    class Meta:
        name = "requester"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = field(
        default=None,
        metadata={
            "type": "Element",
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
        }
    )


@dataclass
class Subject:
    class Meta:
        name = "subject"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class ValueAttachment:
    class Meta:
        name = "valueAttachment"
        namespace = "http://hl7.org/fhir"

    content_type: Optional[ContentType] = field(
        default=None,
        metadata={
            "name": "contentType",
            "type": "Element",
        }
    )
    data: Optional[Data] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    title: Optional[Title] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class ValueReference:
    class Meta:
        name = "valueReference"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class Span:
    class Meta:
        name = "span"
        namespace = "http://www.w3.org/1999/xhtml"

    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "a",
                    "type": A,
                },
                {
                    "type": str,
                    "default": "",
                },
            ),
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
        }
    )

@dataclass
class Contained:
    class Meta:
        name = "contained"
        namespace = "http://hl7.org/fhir"

    binary: Optional[Binary] = field(
        default=None,
        metadata={
            "name": "Binary",
            "type": "Element",
        }
    )


@dataclass
class Destination:
    class Meta:
        name = "destination"
        namespace = "http://hl7.org/fhir"

    name: Optional[Name] = field(
        default=Name(value="MyCareNet"),
        metadata={
            "type": "Element",
        }
    )
    endpoint: Optional[Endpoint] = field(
        default=Endpoint("MyCareNet"),
        metadata={
            "type": "Element",
        }
    )


@dataclass
class Insurance:
    class Meta:
        name = "insurance"
        namespace = "http://hl7.org/fhir"

    sequence: Optional[Sequence] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    focal: Optional[Focal] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    coverage: Optional[Coverage] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class Priority:
    class Meta:
        name = "priority"
        namespace = "http://hl7.org/fhir"

    coding: Optional[Coding] = field(
        default=None,
        metadata={
            "type": "Element",
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
        }
    )


@dataclass
class P:
    class Meta:
        name = "p"
        namespace = "http://www.w3.org/1999/xhtml"

    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "b",
                    "type": str,
                },
                {
                    "name": "a",
                    "type": A,
                },
                {
                    "type": str,
                    "default": "",
                },
                {
                    "name": "span",
                    "type": Span,
                },
            ),
        }
    )


@dataclass
class Td:
    class Meta:
        name = "td"
        namespace = "http://www.w3.org/1999/xhtml"

    content: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
            "choices": (
                {
                    "name": "span",
                    "type": Union[Span, str],
                },
                {
                    "type": str,
                    "default": "",
                },
                {
                    "name": "b",
                    "type": str,
                },
                {
                    "name": "code",
                    "type": str,
                },
            ),
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
        }
    )
    code: Optional[Code] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class TypeType:
    class Meta:
        name = "type"
        namespace = "http://hl7.org/fhir"

    coding: Optional[EventCoding] = field(
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
class Item:
    class Meta:
        name = "item"
        namespace = "http://hl7.org/fhir"

    sequence: Optional[Sequence] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    product_or_service: Optional[ProductOrService] = field(
        default=None,
        metadata={
            "name": "productOrService",
            "type": "Element",
        }
    )
    serviced_date: Optional[ServicedDate] = field(
        default=None,
        metadata={
            "name": "servicedDate",
            "type": "Element",
        }
    )


@dataclass
class SupportingInfo:
    class Meta:
        name = "supportingInfo"
        namespace = "http://hl7.org/fhir"

    sequence: Optional[Sequence] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    category: Optional[Category] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    code: Optional[Code] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    value_attachment: Optional[ValueAttachment] = field(
        default=None,
        metadata={
            "name": "valueAttachment",
            "type": "Element",
        }
    )
    value_reference: Optional[ValueReference] = field(
        default=None,
        metadata={
            "name": "valueReference",
            "type": "Element",
        }
    )
    value_string: Optional[ValueString] = field(
        default=None,
        metadata={
            "name": "valueString",
            "type": "Element",
        }
    )
    reference: Optional[Reference] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class Blockquote:
    class Meta:
        name = "blockquote"
        namespace = "http://www.w3.org/1999/xhtml"

    p: List[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class Tr:
    class Meta:
        name = "tr"
        namespace = "http://www.w3.org/1999/xhtml"

    td: List[Union[str, int, Td, XmlDate, bool]] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class Table:
    class Meta:
        name = "table"
        namespace = "http://www.w3.org/1999/xhtml"

    class_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    tr: List[Tr] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class Div:
    class Meta:
        name = "div"
        namespace = "http://www.w3.org/1999/xhtml"

    style: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    p: List[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    div: Optional["Div"] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    blockquote: List[Blockquote] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "sequential": True,
        }
    )
    h3: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "sequential": True,
        }
    )
    table: List[Table] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "sequential": True,
        }
    )
    hr: Optional[object] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class Text:
    class Meta:
        name = "text"
        namespace = "http://hl7.org/fhir"

    status: Optional[Status] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    div: Optional[Div] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/1999/xhtml",
        }
    )


@dataclass
class Claim:
    class Meta:
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    meta: Optional[MetaType] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    text: Optional[Text] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    status: Optional[Status] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    type: Optional[TypeType] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    sub_type: Optional[SubType] = field(
        default=None,
        metadata={
            "name": "subType",
            "type": "Element",
        }
    )
    use: Optional[Use] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    patient: Optional[Patient2] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    billable_period: Optional[BillablePeriod] = field(
        default=None,
        metadata={
            "name": "billablePeriod",
            "type": "Element",
        }
    )
    created: Optional[Created] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    enterer: Optional[Enterer] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    provider: Optional[Provider] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    priority: Optional[Priority] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    referral: Optional[Referral] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    supporting_info: List[SupportingInfo] = field(
        default_factory=list,
        metadata={
            "name": "supportingInfo",
            "type": "Element",
        }
    )
    insurance: Optional[Insurance] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    item: Optional[Item] = field(
        default=None,
        metadata={
            "type": "Element",
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
        }
    )
    meta: Optional[MetaType] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    text: Optional[Text] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    event_coding: Optional[EventCoding] = field(
        default=None,
        metadata={
            "name": "eventCoding",
            "type": "Element",
        }
    )
    destination: Optional[Destination] = field(
        default=Destination(),
        metadata={
            "type": "Element",
        }
    )
    sender: Optional[Sender] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    source: Optional[Source] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    focus: Optional[Focus] = field(
        default=None,
        metadata={
            "type": "Element",
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
        }
    )
    meta: Optional[MetaType] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    text: Optional[Text] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    identifier: Optional[Identifier] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    type: Optional[TypeType] = field(
        default=None,
        metadata={
            "type": "Element",
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
        }
    )
    meta: Optional[MetaType] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    text: Optional[Text] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    identifier: Optional[Identifier] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    gender: Optional[Gender] = field(
        default=None,
        metadata={
            "type": "Element",
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
        }
    )
    meta: Optional[MetaType] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    text: Optional[Text] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    practitioner: Optional[Practitioner2] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    code: Optional[NestedCode] = field(
        default=None,
        metadata={
            "type": "Element",
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
        }
    )
    meta: Optional[MetaType] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    text: Optional[Text] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    identifier: Optional[Identifier] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class ServiceRequest:
    class Meta:
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    meta: Optional[MetaType] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    text: Optional[Text] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    contained: Optional[Contained] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    identifier: Optional[Identifier] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    status: Optional[Status] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    intent: Optional[Intent] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    category: Optional[Category] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    code: Optional[Code] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    quantity_quantity: Optional[QuantityQuantity] = field(
        default=None,
        metadata={
            "name": "quantityQuantity",
            "type": "Element",
        }
    )
    subject: Optional[Subject] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    authored_on: Optional[AuthoredOn] = field(
        default=None,
        metadata={
            "name": "authoredOn",
            "type": "Element",
        }
    )
    requester: Optional[Requester] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    supporting_info: Optional[SupportingInfo] = field(
        default=None,
        metadata={
            "name": "supportingInfo",
            "type": "Element",
        }
    )


@dataclass
class Resource:
    class Meta:
        name = "resource"
        namespace = "http://hl7.org/fhir"

    claim: Optional[Claim] = field(
        default=None,
        metadata={
            "name": "Claim",
            "type": "Element",
        }
    )
    service_request: Optional[ServiceRequest] = field(
        default=None,
        metadata={
            "name": "ServiceRequest",
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
    practitioner_role: Optional[PractitionerRole] = field(
        default=None,
        metadata={
            "name": "PractitionerRole",
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
        }
    )
    resource: Optional[Resource] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


@dataclass
class Bundle:
    class Meta:
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = field(
        default=None,
        metadata={
            "name": "id",
            "type": "Element",
        }
    )
    meta: Optional[MetaType] = field(
        default=MetaType(),
        metadata={
            "type": "Element",
        }
    )
    type: Optional[TypeType] = field(
        default=TypeType(),
        metadata={
            "type": "Element",
        }
    )
    timestamp: Optional[Timestamp] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    entry: List[Entry] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
