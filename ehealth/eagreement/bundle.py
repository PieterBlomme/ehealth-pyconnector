from pydantic import BaseModel, Field, ConfigDict

from typing import List, Optional, Union
from xsdata.models.datatype import XmlDate, XmlDateTime



class AuthoredOn(BaseModel):
    class Meta:
        name = "authoredOn"
        namespace = "http://hl7.org/fhir"

    value: Optional[XmlDate] = Field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


class ContentType(BaseModel):
    class Meta:
        name = "contentType"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


class Created(BaseModel):
    class Meta:
        name = "created"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


class Data(BaseModel):
    class Meta:
        name = "data"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


class Display(BaseModel):
    class Meta:
        name = "display"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
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
        }
    )


class Focal(BaseModel):
    class Meta:
        name = "focal"
        namespace = "http://hl7.org/fhir"

    value: Optional[bool] = Field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )

class PreAuthRef(BaseModel):
    class Meta:
        name = "preAuthRef"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
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
        }
    )


class Intent(BaseModel):
    class Meta:
        name = "intent"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
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
        }
    )


class Sequence(BaseModel):
    class Meta:
        name = "sequence"
        namespace = "http://hl7.org/fhir"

    value: Optional[int] = Field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


class ServicedDate(BaseModel):
    class Meta:
        name = "servicedDate"
        namespace = "http://hl7.org/fhir"

    value: Optional[XmlDate] = Field(
        default=None,
        metadata={
            "type": "Attribute",
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
        }
    )


class Timestamp(BaseModel):
    class Meta:
        name = "timestamp"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


class Title(BaseModel):
    class Meta:
        name = "title"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
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
        }
    )


class Value(BaseModel):
    class Meta:
        name = "value"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )

class ValueCode(BaseModel):
    class Meta:
        name = "valueCode"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )

class ValueString(BaseModel):
    class Meta:
        name = "valueString"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


class A(BaseModel):
    class Meta:
        name = "a"
        namespace = "http://www.w3.org/1999/xhtml"

    href: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    name: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    value: str = Field(
        default=""
    )


class Binary(BaseModel):
    class Meta:
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    content_type: Optional[ContentType] = Field(
        default=None,
        metadata={
            "name": "contentType",
            "type": "Element",
        }
    )
    data: Optional[Data] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class BillablePeriod(BaseModel):
    class Meta:
        name = "billablePeriod"
        namespace = "http://hl7.org/fhir"

    start: Optional[Start] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )

class Code(BaseModel):
    class Meta:
        name = "code"
        namespace = "http://hl7.org/fhir"

    value: Optional[Union[str, int]] = Field(
        default=None,
        metadata={
            "type": "Attribute",
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
        }
    )
    code: Optional["Code"] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    display: Optional[Display] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )

class NestedCode(BaseModel):
    class Meta:
        name = "code"
        namespace = "http://hl7.org/fhir"

    coding: Optional[Coding] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )

class Coverage(BaseModel):
    class Meta:
        name = "coverage"
        namespace = "http://hl7.org/fhir"

    display: Optional[Display] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class Enterer(BaseModel):
    class Meta:
        name = "enterer"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = Field(
        default=None,
        metadata={
            "type": "Element",
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
        }
    )

class Identifier0(BaseModel):
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

class Assigner(BaseModel):
    class Meta:
        name = "assigner"
        namespace = "http://hl7.org/fhir"

    identifier: Optional[Identifier0] = Field(
        default=None,
        metadata={
            "type": "Element",
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
    assigner: Optional[Assigner] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class MetaType(BaseModel):
    class Meta:
        name = "meta"
        namespace = "http://hl7.org/fhir"

    profile: Optional[Profile] = Field(
        default_factory=lambda: Profile("http://www.mycarenet.be/standards/fhir/StructureDefinition/be-eagreementdemand"),
        metadata={
            "type": "Element",
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
        }
    )


class Provider(BaseModel):
    class Meta:
        name = "provider"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class QuantityQuantity(BaseModel):
    class Meta:
        name = "quantityQuantity"
        namespace = "http://hl7.org/fhir"

    value: Optional[Value] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class Referral(BaseModel):
    class Meta:
        name = "referral"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class Requester(BaseModel):
    class Meta:
        name = "requester"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = Field(
        default=None,
        metadata={
            "type": "Element",
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
        }
    )


class Subject(BaseModel):
    class Meta:
        name = "subject"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class ValueAttachment(BaseModel):
    class Meta:
        name = "valueAttachment"
        namespace = "http://hl7.org/fhir"

    content_type: Optional[ContentType] = Field(
        default=None,
        metadata={
            "name": "contentType",
            "type": "Element",
        }
    )
    data: Optional[Data] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    title: Optional[Title] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class ValueReference(BaseModel):
    class Meta:
        name = "valueReference"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class Span(BaseModel):
    class Meta:
        name = "span"
        namespace = "http://www.w3.org/1999/xhtml"

    style: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    content: List[object] = Field(
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


class Category(BaseModel):
    class Meta:
        name = "category"
        namespace = "http://hl7.org/fhir"

    coding: Optional[Coding] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )

class Contained(BaseModel):
    class Meta:
        name = "contained"
        namespace = "http://hl7.org/fhir"

    binary: Optional[Binary] = Field(
        default=None,
        metadata={
            "name": "Binary",
            "type": "Element",
        }
    )


class Destination(BaseModel):
    class Meta:
        name = "destination"
        namespace = "http://hl7.org/fhir"

    name: Optional[Name] = Field(
        default_factory=lambda: Name(value="MyCareNet"),
        metadata={
            "type": "Element",
        }
    )
    endpoint: Optional[Endpoint] = Field(
        default_factory=lambda: Endpoint("MyCareNet"),
        metadata={
            "type": "Element",
        }
    )


class Insurance(BaseModel):
    class Meta:
        name = "insurance"
        namespace = "http://hl7.org/fhir"

    sequence: Optional[Sequence] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    focal: Optional[Focal] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )

    coverage: Optional[Coverage] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )

    preAuthRef: Optional[PreAuthRef] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class Priority(BaseModel):
    class Meta:
        name = "priority"
        namespace = "http://hl7.org/fhir"

    coding: Optional[Coding] = Field(
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
        }
    )


class P(BaseModel):
    class Meta:
        name = "p"
        namespace = "http://www.w3.org/1999/xhtml"

    style: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    content: List[object] = Field(
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


class Td(BaseModel):
    class Meta:
        name = "td"
        namespace = "http://www.w3.org/1999/xhtml"

    content: List[object] = Field(
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


class EventCoding(BaseModel):
    class Meta:
        name = "eventCoding"
        namespace = "http://hl7.org/fhir"

    system: Optional[System] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    code: Optional[Code] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class TypeType(BaseModel):
    class Meta:
        name = "type"
        namespace = "http://hl7.org/fhir"

    coding: Optional[EventCoding] = Field(
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
    
class Item(BaseModel):
    class Meta:
        name = "item"
        namespace = "http://hl7.org/fhir"

    sequence: Optional[Sequence] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    product_or_service: Optional[ProductOrService] = Field(
        default=None,
        metadata={
            "name": "productOrService",
            "type": "Element",
        }
    )
    serviced_date: Optional[ServicedDate] = Field(
        default=None,
        metadata={
            "name": "servicedDate",
            "type": "Element",
        }
    )


class SupportingInfo(BaseModel):
    class Meta:
        name = "supportingInfo"
        namespace = "http://hl7.org/fhir"

    sequence: Optional[Sequence] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    category: Optional[Category] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    code: Optional[NestedCode] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    value_attachment: Optional[ValueAttachment] = Field(
        default=None,
        metadata={
            "name": "valueAttachment",
            "type": "Element",
        }
    )
    value_reference: Optional[ValueReference] = Field(
        default=None,
        metadata={
            "name": "valueReference",
            "type": "Element",
        }
    )
    value_string: Optional[ValueString] = Field(
        default=None,
        metadata={
            "name": "valueString",
            "type": "Element",
        }
    )
    reference: Optional[Reference] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class Blockquote(BaseModel):
    class Meta:
        name = "blockquote"
        namespace = "http://www.w3.org/1999/xhtml"

    p: List[P] = Field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )


class Tr(BaseModel):
    class Meta:
        name = "tr"
        namespace = "http://www.w3.org/1999/xhtml"

    td: List[Union[str, int, Td, XmlDate, bool]] = Field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )


class Table(BaseModel):
    class Meta:
        name = "table"
        namespace = "http://www.w3.org/1999/xhtml"

    class_value: Optional[str] = Field(
        default=None,
        metadata={
            "name": "class",
            "type": "Attribute",
        }
    )
    tr: List[Tr] = Field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )


class ValueCoding(BaseModel):
    class Meta:
        name = "valueCoding"
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

class Div(BaseModel):
    class Meta:
        name = "div"
        namespace = "http://www.w3.org/1999/xhtml"

    style: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    p: List[P] = Field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    div: Optional["Div"] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    blockquote: List[Blockquote] = Field(
        default_factory=list,
        metadata={
            "type": "Element",
            "sequential": True,
        }
    )
    h3: List[str] = Field(
        default_factory=list,
        metadata={
            "type": "Element",
            "sequential": True,
        }
    )
    table: List[Table] = Field(
        default_factory=list,
        metadata={
            "type": "Element",
            "sequential": True,
        }
    )
    hr: Optional[object] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )

class Parameter(BaseModel):
    class Meta:
        name = "parameter"
        namespace = "http://hl7.org/fhir"

    name: Optional[Name] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    value_coding: Optional[ValueCoding] = Field(
        default=None,
        metadata={
            "name": "valueCoding",
            "type": "Element",
        }
    )
    value_code: Optional[ValueCode] = Field(
        default=None,
        metadata={
            "name": "valueCode",
            "type": "Element",
        }
    )
    value_reference: Optional[ValueReference] = Field(
        default=None,
        metadata={
            "name": "valueReference",
            "type": "Element",
        }
    )
    value_string: Optional[ValueString] = Field(
        default=None,
        metadata={
            "name": "valueString",
            "type": "Element",
        }
    )


class Text(BaseModel):
    class Meta:
        name = "text"
        namespace = "http://hl7.org/fhir"

    status: Optional[Status] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    div: Optional[Div] = Field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.w3.org/1999/xhtml",
        }
    )


class Claim(BaseModel):
    class Meta:
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    meta: Optional[MetaType] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    text: Optional[Text] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    status: Optional[Status] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    type: Optional[TypeType] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    sub_type: Optional[SubType] = Field(
        default=None,
        metadata={
            "name": "subType",
            "type": "Element",
        }
    )
    use: Optional[Use] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    patient: Optional[Patient2] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    billable_period: Optional[BillablePeriod] = Field(
        default=None,
        metadata={
            "name": "billablePeriod",
            "type": "Element",
        }
    )
    created: Optional[Created] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    enterer: Optional[Enterer] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    provider: Optional[Provider] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    priority: Optional[Priority] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    referral: Optional[Referral] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    supporting_info: List[SupportingInfo] = Field(
        default_factory=list,
        metadata={
            "name": "supportingInfo",
            "type": "Element",
        }
    )
    insurance: Optional[Insurance] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    item: Optional[Item] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class Parameters(BaseModel):
    class Meta:
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    parameter: List[Parameter] = Field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )

class MessageHeader(BaseModel):
    class Meta:
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    meta: Optional[MetaType] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    text: Optional[Text] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    event_coding: Optional[EventCoding] = Field(
        default=None,
        metadata={
            "name": "eventCoding",
            "type": "Element",
        }
    )
    destination: Optional[Destination] = Field(
        default_factory=Destination,
        metadata={
            "type": "Element",
        }
    )
    sender: Optional[Sender] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    source: Optional[Source] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    focus: Optional[Focus] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class Organization(BaseModel):
    class Meta:
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    meta: Optional[MetaType] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    text: Optional[Text] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    identifier: Optional[Identifier] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    type: Optional[TypeType] = Field(
        default=None,
        metadata={
            "type": "Element",
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
        }
    )
    meta: Optional[MetaType] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    text: Optional[Text] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    identifier: Optional[Identifier] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    name: Optional[Name] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    gender: Optional[Gender] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class PractitionerRole(BaseModel):
    class Meta:
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    meta: Optional[MetaType] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    text: Optional[Text] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    practitioner: Optional[Practitioner2] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    code: Optional[NestedCode] = Field(
        default=None,
        metadata={
            "type": "Element",
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
        }
    )
    meta: Optional[MetaType] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    text: Optional[Text] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    identifier: Optional[Identifier] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    name: Optional[Name] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class ServiceRequest(BaseModel):
    class Meta:
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    meta: Optional[MetaType] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    text: Optional[Text] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    contained: Optional[Contained] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    identifier: Optional[Identifier] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    status: Optional[Status] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    intent: Optional[Intent] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    category: Optional[Category] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    code: Optional[NestedCode] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    quantity_quantity: Optional[QuantityQuantity] = Field(
        default=None,
        metadata={
            "name": "quantityQuantity",
            "type": "Element",
        }
    )
    subject: Optional[Subject] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    authored_on: Optional[AuthoredOn] = Field(
        default=None,
        metadata={
            "name": "authoredOn",
            "type": "Element",
        }
    )
    requester: Optional[Requester] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    supporting_info: Optional[SupportingInfo] = Field(
        default=None,
        metadata={
            "name": "supportingInfo",
            "type": "Element",
        }
    )


class Resource(BaseModel):
    class Meta:
        name = "resource"
        namespace = "http://hl7.org/fhir"

    claim: Optional[Claim] = Field(
        default=None,
        metadata={
            "name": "Claim",
            "type": "Element",
        }
    )
    
    parameters: Optional[Parameters] = Field(
        default=None,
        metadata={
            "name": "Parameters",
            "type": "Element",
        }
    )

    service_request: Optional[ServiceRequest] = Field(
        default=None,
        metadata={
            "name": "ServiceRequest",
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
    practitioner_role: Optional[PractitionerRole] = Field(
        default=None,
        metadata={
            "name": "PractitionerRole",
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
    message_header: Optional[MessageHeader] = Field(
        default=None,
        metadata={
            "name": "MessageHeader",
            "type": "Element",
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
        }
    )
    resource: Optional[Resource] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class Bundle(BaseModel):
    class Meta:
        namespace = "http://hl7.org/fhir"

    id: Optional[Id] = Field(
        default=None,
        metadata={
            "name": "id",
            "type": "Element",
        }
    )
    meta: Optional[MetaType] = Field(
        default_factory=MetaType,
        metadata={
            "type": "Element",
        }
    )
    type: Optional[TypeType] = Field(
        default_factory=TypeType,
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
        }
    )