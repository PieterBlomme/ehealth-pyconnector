
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Union
from xsdata.models.datatype import XmlDate, XmlTime

class Cd(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        name = "cd"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    model_config = ConfigDict(defer_build=True)

    s: Optional[str] = Field(
        default=None,
        metadata={
            "name": "S",
            "type": "Attribute",
            "required": True,
        }
    )
    sv: Optional[Union[str, float]] = Field(
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

class Description(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        name = "description"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    model_config = ConfigDict(defer_build=True)

    l: Optional[str] = Field(
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

    model_config = ConfigDict(defer_build=True)

    cd: Optional[Cd] = Field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ehealth.fgov.be/standards/kmehr/schema/v1",
            "required": True,
        }
    )
    description: Optional[Description] = Field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ehealth.fgov.be/standards/kmehr/schema/v1",
            "required": True,
        }
    )
    url: Optional[str] = Field(
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

    model_config = ConfigDict(defer_build=True)

    iscomplete: Optional[bool] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    error: Optional[Error] = Field(
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

    model_config = ConfigDict(defer_build=True)

    s: Optional[str] = Field(
        default=None,
        metadata={
            "name": "S",
            "type": "Attribute",
            "required": True,
        }
    )
    sv: Optional[Union[str, float]] = Field(
        default=None,
        metadata={
            "name": "SV",
            "type": "Attribute",
            "required": True,
        }
    )
    value: Optional[str] = Field(
        default=None,
        metadata={
            "required": True,
        }
    )

class Cd(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        name = "cd"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    model_config = ConfigDict(defer_build=True)

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
    sv: Optional[Union[str, float]] = Field(
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
    model_config = ConfigDict(defer_build=True)
    class Meta:
        name = "id"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    model_config = ConfigDict(defer_build=True)

    s: Optional[str] = Field(
        default=None,
        metadata={
            "name": "S",
            "type": "Attribute",
            "required": True,
        }
    )
    sv: Optional[Union[str, float]] = Field(
        default=None,
        metadata={
            "name": "SV",
            "type": "Attribute",
            "required": True,
        }
    )
    value: Optional[Union[str, int]] = Field(
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

    model_config = ConfigDict(defer_build=True)

    decimal: Optional[Union[str, int]] = Field(
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

    model_config = ConfigDict(defer_build=True)

    l: Optional[str] = Field(
        default=None,
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
    model_config = ConfigDict(defer_build=True)
    class Meta:
        name = "content"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    model_config = ConfigDict(defer_build=True)

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
    text: Optional[Text] = Field(
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

    model_config = ConfigDict(defer_build=True)

    id: List[Id1] = Field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
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

class Insurancymembership(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        name = "insurancymembership"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    model_config = ConfigDict(defer_build=True)

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
    model_config = ConfigDict(defer_build=True)
    class Meta:
        name = "sex"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    model_config = ConfigDict(defer_build=True)

    cd: Optional[Cd] = Field(
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

    model_config = ConfigDict(defer_build=True)

    cd: Optional[Cd] = Field(
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

    model_config = ConfigDict(defer_build=True)

    cd: Optional[Cd] = Field(
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

    model_config = ConfigDict(defer_build=True)

    hcparty: Optional[Hcparty] = Field(
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

    model_config = ConfigDict(defer_build=True)

    hcparty: Optional[Hcparty] = Field(
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

    model_config = ConfigDict(defer_build=True)

    decimal: Optional[Union[str, float]] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    unit: Optional[Unit] = Field(
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

    model_config = ConfigDict(defer_build=True)

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
    model_config = ConfigDict(defer_build=True)
    class Meta:
        name = "recipient"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    model_config = ConfigDict(defer_build=True)

    hcparty: Optional[Hcparty] = Field(
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

    model_config = ConfigDict(defer_build=True)

    hcparty: Optional[Hcparty] = Field(
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

    model_config = ConfigDict(defer_build=True)

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
    model_config = ConfigDict(defer_build=True)
    class Meta:
        name = "header"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    model_config = ConfigDict(defer_build=True)

    standard: Optional[Standard] = Field(
        default=None,
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
    
class Lifecycle(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        name = "lifecycle"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    model_config = ConfigDict(defer_build=True)

    cd: Optional[Cd] = Field(
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

    model_config = ConfigDict(defer_build=True)

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
    author: Optional[Author1] = Field(
        default=None,
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
    lifecycle: Optional[Lifecycle] = Field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )

class Response(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        name = "response"
        namespace = "http://www.ehealth.fgov.be/messageservices/core/v1"

    model_config = ConfigDict(defer_build=True)

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
    request: Optional[Request] = Field(
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

    model_config = ConfigDict(defer_build=True)

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
    model_config = ConfigDict(defer_build=True)
    class Meta:
        name = "folder"
        namespace = "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"

    model_config = ConfigDict(defer_build=True)

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
    model_config = ConfigDict(defer_build=True)
    class Meta:
        name = "kmehrmessage"
        namespace = "http://www.ehealth.fgov.be/messageservices/core/v1"

    model_config = ConfigDict(defer_build=True)

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

class SendTransactionResponse(BaseModel):
    model_config = ConfigDict(defer_build=True)
    class Meta:
        namespace = "http://www.ehealth.fgov.be/messageservices/protocol/v1"

    model_config = ConfigDict(defer_build=True)

    message_protocole_schema_version: Optional[Union[str, float]] = Field(
        default=None,
        metadata={
            "name": "messageProtocoleSchemaVersion",
            "type": "Attribute",
            "required": True,
        }
    )
    response: Optional[Response] = Field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.ehealth.fgov.be/messageservices/core/v1",
            "required": True,
        }
    )
    acknowledge: Optional[Acknowledge] = Field(
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

class EAttestV3(BaseModel):
    model_config = ConfigDict(defer_build=True)

    response: SendTransactionResponse
    transaction_request: str
    transaction_response: str
    soap_request: str
    soap_response: str