import logging
import datetime
from pydantic import BaseModel, Field
from typing import Any, Optional

logger = logging.getLogger(__name__)

class ContentInfo(BaseModel):
    mime_type: str
    title: str

    @classmethod
    def from_jvm(cls, jvm_object: Any) -> 'ContentInfo':
        return cls(
            mime_type=jvm_object.getMimeType(),
            title=jvm_object.getTitle(),
        )
class ContentSpecification(BaseModel):
    application_name: str
    content_type: str
    is_encrypted: bool
    is_important: bool

    @classmethod
    def from_jvm(cls, jvm_object: Any) -> 'ContentSpecification':
        return cls(
            application_name=jvm_object.getApplicationName(),
            content_type=jvm_object.getContentType(),
            is_encrypted=jvm_object.isIsEncrypted(),
            is_important=jvm_object.isIsImportant(),
        )

class MessageInfo(BaseModel):
    expiration_date: str
    publication_date: str

    @classmethod
    def from_jvm(cls, jvm_object: Any) -> 'MessageInfo':
        return cls(
            expiration_date=jvm_object.getExpirationDate().toString(),
            publication_date=jvm_object.getPublicationDate().toString(),
        )

class Sender(BaseModel):
    first_name: Optional[str]
    name: Optional[str]
    id: str
    quality: str
    type: str
    sub_type: Optional[str]
    person_in_organisation: Optional[bool]

    @classmethod
    def from_jvm(cls, jvm_object: Any) -> 'Sender':
        return cls(
            first_name=jvm_object.getFirstName(),
            name=jvm_object.getName(),
            id=jvm_object.getId(),
            quality=jvm_object.getQuality(),
            type=jvm_object.getType(),
            sub_type=jvm_object.getSubType(),
            person_in_organisation=jvm_object.getPersonInOrganisation(),
        )


class Message(BaseModel):
    id: str
    content_info: Any
    content_specification: Any
    message_info: Any
    sender: Any

    @classmethod
    def from_jvm(cls, jvm_object: Any) -> "Message":
        return cls(
            id=jvm_object.getMessageId(),
            content_info=ContentInfo.from_jvm(jvm_object.getContentInfo()),
            content_specification=ContentSpecification.from_jvm(jvm_object.getContentSpecification()),
            message_info=MessageInfo.from_jvm(jvm_object.getMessageInfo()),
            sender=Sender.from_jvm(jvm_object.getSender()),
        )
    
class Acknowledgement(BaseModel):
    read: Optional[datetime.datetime]
    published: Optional[datetime.datetime]
    received: Optional[datetime.datetime]

    @classmethod
    def parse_datetime(cls, jvm_datetime: Any) -> Optional[datetime.datetime]:
        if jvm_datetime is None:
            return None
        str_datetime = jvm_datetime.toString()
        if str_datetime.endswith("Z"):
            str_datetime = str_datetime[:-1] + "+00:00"
        return datetime.datetime.fromisoformat(str_datetime)
    
    @classmethod
    def from_jvm(cls, jvm_object: Any) -> "Acknowledgement":

        return cls(
            read=cls.parse_datetime(jvm_object.getRead()),
            published=cls.parse_datetime(jvm_object.getPublished()),
            received=cls.parse_datetime(jvm_object.getReceived()),
        )

class Annex(BaseModel):
    title: Optional[str]
    content: Optional[bytes]
    mime_type: str

    @classmethod
    def from_jvm(cls, jvm_object: Any) -> "Annex":
        return cls(
            title=jvm_object.getTitle(),
            content=jvm_object.getContent(),
            mime_type=jvm_object.getMimeType(),
        )
    
class FullMessage(Annex):
    is_encrypted: bool
    is_important: bool
    annexes: list[Annex]
    sender: Any
    message_info: Any

    @classmethod
    def from_jvm(cls, jvm_object: Any) -> "FullMessage":
        
        try:
            annexes = [
                Annex.from_jvm(annex)
                for annex in jvm_object.getAnnexList()
            ]
        except Exception:
            annexes = []
            
        return cls(
            title=jvm_object.getDocumentTitle(),
            content=jvm_object.getBody().getContent(),
            mime_type=jvm_object.getOriginal().getMessage().getContentContext().getContent().getDocument().getMimeType(),
            is_encrypted=jvm_object.isEncrypted(),
            is_important=jvm_object.isImportant(),
            annexes=annexes,
            sender=Sender.from_jvm(jvm_object.getOriginal().getSender()),
            message_info=MessageInfo.from_jvm(jvm_object.getOriginal().getMessageInfo()),
        )