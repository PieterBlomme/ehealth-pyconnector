from typing import List, Optional, Union
from xsdata.models.datatype import XmlDate, XmlTime
from pydantic import BaseModel, ConfigDict
from xsdata_pydantic.fields import field



class Cd(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "cd"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    s: Optional[str] = field(
        default=None,
        metadata={
            "name": "S",
            "type": "Attribute",
            "required": True,
        }
    )
    sv: Optional[float] = field(
        default=None,
        metadata={
            "name": "SV",
            "type": "Attribute",
            "required": True,
        }
    )
    value: Union[int, str] = field(
        default="",
        metadata={
            "required": True,
        }
    )



class Description(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "description"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    l: Optional[str] = field(
        default=None,
        metadata={
            "name": "L",
            "type": "Attribute",
            "required": True,
        }
    )
    

class Error(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "error"
        namespace = "http://www.ehealth.fgov.be/messageservices/core/v1"

    cd: Optional[Cd] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ehealth.fgov.be/standards/kmehr/schema/v1",
            "required": True,
        }
    )
    description: Optional[Description] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ehealth.fgov.be/standards/kmehr/schema/v1",
            "required": True,
        }
    )
    url: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ehealth.fgov.be/standards/kmehr/schema/v1",
            "required": True,
        }
    )


class Acknowledge(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "acknowledge"
        namespace = "http://www.ehealth.fgov.be/messageservices/core/v1"

    iscomplete: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    error: Optional[Error] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Id2(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "id"
        namespace = "http://www.ehealth.fgov.be/messageservices/core/v1"

    s: Optional[str] = field(
        default=None,
        metadata={
            "name": "S",
            "type": "Attribute",
            "required": True,
        }
    )
    sv: Optional[float] = field(
        default=None,
        metadata={
            "name": "SV",
            "type": "Attribute",
            "required": True,
        }
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "required": True,
        }
    )



class Id1(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "id"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    s: Optional[str] = field(
        default=None,
        metadata={
            "name": "S",
            "type": "Attribute",
            "required": True,
        }
    )
    sv: Optional[float] = field(
        default=None,
        metadata={
            "name": "SV",
            "type": "Attribute",
            "required": True,
        }
    )
    value: Optional[int] = field(
        default=None,
        metadata={
            "required": True,
        }
    )



class Quantity(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "quantity"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    decimal: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Text(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "text"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    l: Optional[str] = field(
        default=None,
        metadata={
            "name": "L",
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



class Content(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "content"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    cd: Optional[Cd] = field(
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



class Hcparty(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "hcparty"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    id: List[Id1] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )
    cd: Optional[Cd] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    firstname: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    familyname: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )


class Insurancymembership(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "insurancymembership"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    id: Optional[Id1] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    membership: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class Sex(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "sex"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    cd: Optional[Cd] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Standard(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "standard"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    cd: Optional[Cd] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Unit(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "unit"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    cd: Optional[Cd] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Author2(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "author"
        namespace = "http://www.ehealth.fgov.be/messageservices/core/v1"

    hcparty: Optional[Hcparty] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ehealth.fgov.be/standards/kmehr/schema/v1",
            "required": True,
        }
    )



class Author1(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "author"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    hcparty: Optional[Hcparty] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Cost(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "cost"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    decimal: Optional[float] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    unit: Optional[Unit] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Patient(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "patient"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    id: Optional[Id1] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    firstname: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    familyname: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    sex: Optional[Sex] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    insurancymembership: Optional[Insurancymembership] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class Recipient(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "recipient"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    hcparty: Optional[Hcparty] = field(
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
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    hcparty: Optional[Hcparty] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Request(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "request"
        namespace = "http://www.ehealth.fgov.be/messageservices/core/v1"

    id: Optional[Id2] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    author: Optional[Author2] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    time: Optional[XmlTime] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Header(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "header"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    standard: Optional[Standard] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    id: Optional[Id1] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    time: Optional[XmlTime] = field(
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
    recipient: Optional[Recipient] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    

class Lifecycle(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "lifecycle"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    cd: Optional[Cd] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )


class Item(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "item"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    id: Optional[Id1] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    cd: Optional[Cd] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    content: List[Content] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    author: Optional[Author1] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    quantity: Optional[Quantity] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    cost: Optional[Cost] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    lifecycle: Optional[Lifecycle] = field(
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
        namespace = "http://www.ehealth.fgov.be/messageservices/core/v1"

    id: Optional[Id2] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    author: Optional[Author2] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    time: Optional[XmlTime] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    request: Optional[Request] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )



class Transaction(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "transaction"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    id: Optional[Id1] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    cd: Optional[Cd] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    time: Optional[XmlTime] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    author: Optional[Author1] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    iscomplete: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    isvalidated: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    item: List[Item] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )



class Folder(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "folder"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    id: Optional[Id1] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    patient: Optional[Patient] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    transaction: List[Transaction] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )



class Kmehrmessage(BaseModel):
    model_config = ConfigDict(defer_build=True)

    class Meta:
        name = "kmehrmessage"
        namespace = "http://www.ehealth.fgov.be/messageservices/core/v1"

    header: Optional[Header] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ehealth.fgov.be/standards/kmehr/schema/v1",
            "required": True,
        }
    )
    folder: Optional[Folder] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ehealth.fgov.be/standards/kmehr/schema/v1",
            "required": True,
        }
    )



class SendTransactionResponse(BaseModel):
    model_config = ConfigDict(extra='forbid', defer_build=True)

    class Meta:
        namespace = "http://www.ehealth.fgov.be/messageservices/protocol/v1"

    message_protocole_schema_version: Optional[float] = field(
        default=None,
        metadata={
            "name": "messageProtocoleSchemaVersion",
            "type": "Attribute",
            "required": True,
        }
    )
    response: Optional[Response] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ehealth.fgov.be/messageservices/core/v1",
            "required": True,
        }
    )
    acknowledge: Optional[Acknowledge] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ehealth.fgov.be/messageservices/core/v1",
            "required": True,
        }
    )
    kmehrmessage: Optional[Kmehrmessage] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ehealth.fgov.be/messageservices/core/v1",
            "required": True,
        }
    )

class EAttestV3(BaseModel):
    model_config = ConfigDict(extra='forbid', defer_build=True)

    response: SendTransactionResponse
    transaction_request: str
    transaction_response: str
    soap_request: str
    soap_response: str