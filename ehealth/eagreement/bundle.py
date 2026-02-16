from pydantic import BaseModel, ConfigDict
from xsdata_pydantic.fields import field

from typing import List, Optional, Union
from xsdata.models.datatype import XmlDate, XmlDateTime



class AuthoredOn(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "authoredOn"
        namespace = "http://hl7.org/fhir"

    value: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


class ContentType(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "contentType"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


class Created(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "created"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


class Data(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "data"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


class Display(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "display"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
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
        }
    )


class Focal(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "focal"
        namespace = "http://hl7.org/fhir"

    value: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
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
        }
    )


class Intent(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "intent"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
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
        }
    )


class Sequence(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "sequence"
        namespace = "http://hl7.org/fhir"

    value: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


class ServicedDate(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "servicedDate"
        namespace = "http://hl7.org/fhir"

    value: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Attribute",
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
        }
    )


class Timestamp(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "timestamp"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


class Title(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "title"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
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
        }
    )


class Value(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "value"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )

class ValueCode(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "valueCode"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )

class ValueString(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "valueString"
        namespace = "http://hl7.org/fhir"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


class A(BaseModel):
    model_config = ConfigDict(defer_build=True)

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


class Binary(BaseModel):
    model_config = ConfigDict(defer_build=True)

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


class BillablePeriod(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "billablePeriod"
        namespace = "http://hl7.org/fhir"

    start: Optional[Start] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )

class Code(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "code"
        namespace = "http://hl7.org/fhir"

    value: Optional[Union[str, int]] = field(
        default=None,
        metadata={
            "type": "Attribute",
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

class NestedCode(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "code"
        namespace = "http://hl7.org/fhir"

    coding: Optional[Coding] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )

class Coverage(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "coverage"
        namespace = "http://hl7.org/fhir"

    display: Optional[Display] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class Enterer(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "enterer"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = field(
        default=None,
        metadata={
            "type": "Element",
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
        }
    )

class Identifier0(BaseModel):
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

class Assigner(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "assigner"
        namespace = "http://hl7.org/fhir"

    identifier: Optional[Identifier0] = field(
        default=None,
        metadata={
            "type": "Element",
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
    assigner: Optional[Assigner] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class MetaType(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "meta"
        namespace = "http://hl7.org/fhir"

    profile: Optional[Profile] = field(
        default_factory=lambda: Profile("http://www.mycarenet.be/standards/fhir/StructureDefinition/be-eagreementdemand"),
        metadata={
            "type": "Element",
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
        }
    )


class Provider(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "provider"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class QuantityQuantity(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "quantityQuantity"
        namespace = "http://hl7.org/fhir"

    value: Optional[Value] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class Referral(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "referral"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class Requester(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "requester"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = field(
        default=None,
        metadata={
            "type": "Element",
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
        }
    )


class Subject(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "subject"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class ValueAttachment(BaseModel):
    model_config = ConfigDict(defer_build=True)

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


class ValueReference(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "valueReference"
        namespace = "http://hl7.org/fhir"

    reference: Optional[Reference] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class Span(BaseModel):
    model_config = ConfigDict(defer_build=True)

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


class Category(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "category"
        namespace = "http://hl7.org/fhir"

    coding: Optional[Coding] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )

class Contained(BaseModel):
    model_config = ConfigDict(defer_build=True)

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


class Destination(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "destination"
        namespace = "http://hl7.org/fhir"

    name: Optional[Name] = field(
        default_factory=lambda: Name(value="MyCareNet"),
        metadata={
            "type": "Element",
        }
    )
    endpoint: Optional[Endpoint] = field(
        default_factory=lambda: Endpoint("MyCareNet"),
        metadata={
            "type": "Element",
        }
    )


class Insurance(BaseModel):
    model_config = ConfigDict(defer_build=True)

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

    preAuthRef: Optional[PreAuthRef] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class Priority(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "priority"
        namespace = "http://hl7.org/fhir"

    coding: Optional[Coding] = field(
        default=None,
        metadata={
            "type": "Element",
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
        }
    )


class P(BaseModel):
    model_config = ConfigDict(defer_build=True)

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


class Td(BaseModel):
    model_config = ConfigDict(defer_build=True)

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


class EventCoding(BaseModel):
    model_config = ConfigDict(defer_build=True)

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


class TypeType(BaseModel):
    model_config = ConfigDict(defer_build=True)

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
    
class Item(BaseModel):
    model_config = ConfigDict(defer_build=True)

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


class SupportingInfo(BaseModel):
    model_config = ConfigDict(defer_build=True)

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
    code: Optional[NestedCode] = field(
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


class Blockquote(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "blockquote"
        namespace = "http://www.w3.org/1999/xhtml"

    p: List[P] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )


class Tr(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "tr"
        namespace = "http://www.w3.org/1999/xhtml"

    td: List[Union[str, int, Td, XmlDate, bool]] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )


class Table(BaseModel):
    model_config = ConfigDict(defer_build=True)

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


class ValueCoding(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "valueCoding"
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

class Div(BaseModel):
    model_config = ConfigDict(defer_build=True)

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

class Parameter(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "parameter"
        namespace = "http://hl7.org/fhir"

    name: Optional[Name] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    value_coding: Optional[ValueCoding] = field(
        default=None,
        metadata={
            "name": "valueCoding",
            "type": "Element",
        }
    )
    value_code: Optional[ValueCode] = field(
        default=None,
        metadata={
            "name": "valueCode",
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


class Text(BaseModel):
    model_config = ConfigDict(defer_build=True)

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


class Claim(BaseModel):
    model_config = ConfigDict(defer_build=True)

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


class Parameters(BaseModel):
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
    parameter: List[Parameter] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
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
        default_factory=Destination,
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


class Organization(BaseModel):
    model_config = ConfigDict(defer_build=True)

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


class Patient1(BaseModel):
    model_config = ConfigDict(defer_build=True)

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


class PractitionerRole(BaseModel):
    model_config = ConfigDict(defer_build=True)

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


class Practitioner1(BaseModel):
    model_config = ConfigDict(defer_build=True)

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


class ServiceRequest(BaseModel):
    model_config = ConfigDict(defer_build=True)

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
    code: Optional[NestedCode] = field(
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


class Resource(BaseModel):
    model_config = ConfigDict(defer_build=True)

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
    
    parameters: Optional[Parameters] = field(
        default=None,
        metadata={
            "name": "Parameters",
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
        }
    )
    resource: Optional[Resource] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class Bundle(BaseModel):
    model_config = ConfigDict(extra='forbid', defer_build=True)

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
        default_factory=MetaType,
        metadata={
            "type": "Element",
        }
    )
    type: Optional[TypeType] = field(
        default_factory=TypeType,
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