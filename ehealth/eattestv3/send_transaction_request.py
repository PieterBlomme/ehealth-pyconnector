from pydantic import BaseModel, Field
from typing import List, Optional, Union
from xsdata.models.datatype import XmlDate, XmlTime



class Id2(BaseModel):
    class Meta:
        name = "id"
        namespace = "http://www.ehealth.fgov.be/messageservices/core/v1"

    s: Optional[str] = Field(
        default="ID-KMEHR",
        metadata={
            "name": "S",
            "type": "Attribute",
            "required": True,
        }
    )
    sv: Optional[str] = Field(
        default="1.0",
        metadata={
            "name": "SV",
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



class Cd(BaseModel):
    class Meta:
        name = "cd"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    s: Optional[str] = Field(
        default=None,
        metadata={
            "name": "S",
            "type": "Attribute",
            "required": True,
        }
    )
    sl: Optional[str] = Field(
        default=None,
        metadata={
            "name": "SL",
            "type": "Attribute",
        }
    )
    sv: Optional[str] = Field(
        default=None,
        metadata={
            "name": "SV",
            "type": "Attribute",
            "required": True,
        }
    )
    value: Union[int, str] = Field(
        default="",
        metadata={
            "required": True,
        }
    )



class Id1(BaseModel):
    class Meta:
        name = "id"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    s: Optional[str] = Field(
        default=None,
        metadata={
            "name": "S",
            "type": "Attribute",
            "required": True,
        }
    )
    sl: Optional[str] = Field(
        default=None,
        metadata={
            "name": "SL",
            "type": "Attribute",
            "required": False,
        }
    )
    sv: Optional[str] = Field(
        default="1.0",
        metadata={
            "name": "SV",
            "type": "Attribute",
            "required": True,
        }
    )
    value: str = Field(
        default=""
    )



class Quantity(BaseModel):
    class Meta:
        name = "quantity"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    decimal: Optional[int] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Hcparty(BaseModel):
    class Meta:
        name = "hcparty"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    id: List[Id1] = Field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    cd: Optional[Cd] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    firstname: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    familyname: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    name: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class Text(BaseModel):
    class Meta:
        name = "text"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    l: Optional[str] = Field(
        default="en",
        metadata={
            "name": "L",
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


class Content(BaseModel):
    class Meta:
        name = "content"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    date: Optional[XmlDate] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    cd: Optional[Cd] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    id: Optional[Id1] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    hcparty: Optional[Hcparty] = Field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ehealth.fgov.be/standards/kmehr/schema/v1",
            "required": True,
        }
    )
    text: Optional[Text] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class Insurancymembership(BaseModel):
    class Meta:
        name = "insurancymembership"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    id: Optional[Id1] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    membership: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Sex(BaseModel):
    class Meta:
        name = "sex"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    cd: Optional[Cd] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Standard(BaseModel):
    class Meta:
        name = "standard"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    cd: Optional[Cd] = Field(
        default_factory=lambda: Cd(s="CD-STANDARD", sv="1.35", value="20210120"),
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Unit(BaseModel):
    class Meta:
        name = "unit"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    cd: Optional[Cd] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Author2(BaseModel):
    class Meta:
        name = "author"
        namespace = "http://www.ehealth.fgov.be/messageservices/core/v1"

    hcparty: Optional[Hcparty] = Field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ehealth.fgov.be/standards/kmehr/schema/v1",
            "required": True,
        }
    )



class Author1(BaseModel):
    class Meta:
        name = "author"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    hcparty: Optional[Hcparty] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Cost(BaseModel):
    class Meta:
        name = "cost"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    decimal: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    unit: Optional[Unit] = Field(
        default_factory=lambda: Unit(cd=Cd(s="CD-CURRENCY", sv="1.0", value="EUR")),
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Patient(BaseModel):
    class Meta:
        name = "patient"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    id: Optional[Id1] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    firstname: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    familyname: Optional[str] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    sex: Optional[Sex] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    insurancymembership: Optional[Insurancymembership] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Recipient(BaseModel):
    class Meta:
        name = "recipient"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    hcparty: Optional[Hcparty] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Sender(BaseModel):
    class Meta:
        name = "sender"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    hcparty: Optional[Hcparty] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Request(BaseModel):
    class Meta:
        name = "request"
        namespace = "http://www.ehealth.fgov.be/messageservices/core/v1"

    id: Optional[Id2] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    author: Optional[Author2] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    date: Optional[XmlDate] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    time: Optional[XmlTime] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Header(BaseModel):
    class Meta:
        name = "header"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    standard: Optional[Standard] = Field(
        default_factory=Standard,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    id: Optional[Id1] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    date: Optional[XmlDate] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    time: Optional[XmlTime] = Field(
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
    recipient: Optional[Recipient] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Item(BaseModel):
    class Meta:
        name = "item"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    id: Optional[Id1] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    cd: Optional[Cd] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    content: List[Content] = Field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    quantity: Optional[Quantity] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    cost: Optional[Cost] = Field(
        default=None,
        metadata={
            "type": "Element",
        }
    )



class Transaction(BaseModel):
    class Meta:
        name = "transaction"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    id: Optional[Id1] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    cd: Optional[Cd] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    date: Optional[XmlDate] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    time: Optional[XmlTime] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    author: Optional[Author1] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    iscomplete: Optional[bool] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    isvalidated: Optional[bool] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    item: List[Item] = Field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )



class Folder(BaseModel):
    class Meta:
        name = "folder"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    id: Optional[Id1] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    patient: Optional[Patient] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    transaction: List[Transaction] = Field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )



class Kmehrmessage(BaseModel):
    class Meta:
        name = "kmehrmessage"
        namespace = "http://www.ehealth.fgov.be/messageservices/core/v1"

    header: Optional[Header] = Field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ehealth.fgov.be/standards/kmehr/schema/v1",
            "required": True,
        }
    )
    folder: Optional[Folder] = Field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ehealth.fgov.be/standards/kmehr/schema/v1",
            "required": True,
        }
    )



class SendTransactionRequest(BaseModel):

    message_protocole_schema_version: Optional[str] = Field(
        default="1.34",
        metadata={
            "name": "messageProtocoleSchemaVersion",
            "type": "Attribute",
            "required": True,
        }
    )
    request: Optional[Request] = Field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ehealth.fgov.be/messageservices/core/v1",
            "required": True,
        }
    )
    kmehrmessage: Optional[Kmehrmessage] = Field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ehealth.fgov.be/messageservices/core/v1",
            "required": True,
        }
    )
