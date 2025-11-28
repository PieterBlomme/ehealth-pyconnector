from py4j.java_gateway import JavaGateway
from typing import Any, Optional, Callable, Literal
import logging
from io import StringIO
from ..sts.assertion import Assertion
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata_pydantic.bindings import XmlParser
from ehealth.utils.callbacks import storage_callback, CallMetadata, CallType, ServiceType

from .types import Message, Acknowledgement, FullMessage

logger = logging.getLogger(__name__)

class EHBoxService:
    def __init__(
            self,
            mycarenet_license_username: str,
            mycarenet_license_password: str,
            etk_endpoint: str = "$uddi{uddi:ehealth-fgov-be:business:etkdepot:v1}",
            environment: str = "acc",
    ):
        self.GATEWAY = JavaGateway()
        self.EHEALTH_JVM = self.GATEWAY.entry_point

        # set up required configuration
        self.config_validator = self.EHEALTH_JVM.getConfigValidator()
        self.config_validator.setProperty("environment", environment)
        if environment == "acc":
            self.is_test = True
        else:
            self.is_test = False

        self.config_validator.setProperty("mycarenet.licence.username", mycarenet_license_username)
        self.config_validator.setProperty("mycarenet.licence.password", mycarenet_license_password)
        self.config_validator.setProperty("endpoint.etk", etk_endpoint)
        self.config_validator.setProperty("endpoint.eattestv3", "$uddi{uddi:ehealth-fgov-be:business:mycareneteattest:v3}")

    def set_configuration_from_token(self, token: str) -> None:
        # TODO copy paste from MDA
        parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
        token_pydantic = parser.parse(StringIO(token), Assertion)
        
        surname = None
        givenname = None
        nihii = None
        ssin = None
        quality = None
                                     
        for attribute in token_pydantic.attribute_statement.attribute:
            if attribute.attribute_name == 'urn:be:fgov:ehealth:1.0:certificateholder:person:ssin':
                ssin = attribute.attribute_value
            elif attribute.attribute_name.startswith('urn:be:fgov:person:ssin:ehealth:1.0:nihii'):
                nihii = attribute.attribute_value
            elif attribute.attribute_name  == 'urn:be:fgov:person:ssin:ehealth:1.0:givenname':
                givenname = attribute.attribute_value
            elif attribute.attribute_name  == 'urn:be:fgov:person:ssin:ehealth:1.0:surname':
                surname = attribute.attribute_value
            elif attribute.attribute_name.startswith('urn:be:fgov:person:ssin:ehealth:1.0:fpsph'):
                if attribute.attribute_value:
                    quality = attribute.attribute_name.split(':')[-2]

        logger.info(f"Name: {givenname} {surname}, SSIN {ssin}, NIHII {nihii}, quality {quality}")
        self.config_validator.setProperty("ehbox.application.name", "Sophia")
    
    def get_messages(self, token: str, inbox: Optional[str] = "INBOX") -> list[Message]:
        self.set_configuration_from_token(token)

        service = self.GATEWAY.jvm.be.ehealth.businessconnector.ehbox.v3.session.ServiceFactory.getEhealthBoxServiceV3()

        request_builder = self.GATEWAY.jvm.be.ehealth.businessconnector.ehbox.v3.builders.impl.RequestBuilderImpl()
        request = request_builder.createAllEhboxesMessagesListRequest(inbox)

        allEhboxesMessagesList = service.getAllEhboxesMessagesList(request).getMessages()
        logger.info(f"Received {len(allEhboxesMessagesList)} messages")

        return [Message.from_jvm(message) for message in allEhboxesMessagesList]
    
    def get_message_acknowledgement(self, token: str, message_id: str) -> list[Acknowledgement]:
        self.set_configuration_from_token(token)

        service = self.GATEWAY.jvm.be.ehealth.businessconnector.ehbox.v3.session.ServiceFactory.getEhealthBoxServiceV3()
        request_builder = self.GATEWAY.jvm.be.ehealth.businessconnector.ehbox.v3.builders.impl.RequestBuilderImpl()
        request = request_builder.createGetMessageAcknowledgmentsStatusRequest(message_id)
        response = service.getMessageAcknowledgmentsStatusRequest(request)
        return [Acknowledgement.from_jvm(ack) for ack in response.getAcknowledgmentsStatus().getRows()]
    
    def get_full_message(self, token: str, message_id: str) -> Message:
        self.set_configuration_from_token(token)

        service = self.GATEWAY.jvm.be.ehealth.businessconnector.ehbox.v3.session.ServiceFactory.getEhealthBoxServiceV3()

        request_builder = self.GATEWAY.jvm.be.ehealth.businessconnector.ehbox.v3.builders.impl.RequestBuilderImpl()
        request = request_builder.createGetFullMessageRequest(message_id)

        fullMessage = service.getFullMessage(request)

        inboxMessage = self.GATEWAY.jvm.be.ehealth.businessconnector.ehbox.v3.builders.BuilderFactory.getConsultationMessageBuilder().buildFullMessage(fullMessage)
        return FullMessage.from_jvm(inboxMessage)
    
    def move_message(
            self, 
            token: str,
            message_id: str,
            source_inbox: str,
            destination_inbox: str,
        ):
        self.set_configuration_from_token(token)

        service = self.GATEWAY.jvm.be.ehealth.businessconnector.ehbox.v3.session.ServiceFactory.getEhealthBoxServiceV3()

        request_builder = self.GATEWAY.jvm.be.ehealth.businessconnector.ehbox.v3.builders.impl.RequestBuilderImpl()

        request = request_builder.createMoveMessageRequest(
            source_inbox,
            destination_inbox,
            self.EHEALTH_JVM.createMessageIdList(message_id)
        )

        response = service.moveMessage(request)
        logger.info(f"Message moved, response: {response.getStatus().getCode()}"
    )

    def delete_message(
            self, 
            token: str,
            message_id: str,
            inbox: Optional[str] = "SENTBOX",
        ):
        self.set_configuration_from_token(token)

        service = self.GATEWAY.jvm.be.ehealth.businessconnector.ehbox.v3.session.ServiceFactory.getEhealthBoxServiceV3()

        request_builder = self.GATEWAY.jvm.be.ehealth.businessconnector.ehbox.v3.builders.impl.RequestBuilderImpl()
    
        request = request_builder.createDeleteMessageRequest(
            inbox,
            self.EHEALTH_JVM.createMessageIdList(message_id)
        )

        response = service.deleteMessage(request)
        logger.info(f"Message deleted, response: {response.getStatus().getCode()}"
    )
    def send_message(
            self, 
            token: str,
            id: str,
            mimeType: str,
            filename: str,
            title: str,
            content: bytes,
            quality_type: Literal["DOCTOR_NIHII", "DOCTOR_SSIN", "PHYSIOTHERAPIST_NIHII", "PHYSIOTHERAPY_SSIN"],
            is_important: Optional[bool] = False,
            is_encrypted: Optional[bool] = True,
            use_received_receipt: Optional[bool] = False,
            use_publication_receipt: Optional[bool] = False,
            use_read_receipt: Optional[bool] = False,
        ):
        self.set_configuration_from_token(token)

        service = self.GATEWAY.jvm.be.ehealth.businessconnector.ehbox.v3.session.ServiceFactory.getEhealthBoxServiceV3()

        if quality_type.endswith("SSIN"):
            if quality_type.startswith("DOCTOR"):
                destination_quality = self.GATEWAY.jvm.be.ehealth.businessconnector.ehbox.api.utils.QualityType.DOCTOR_SSIN
            elif quality_type.startswith("PHYSIOTHERAPIST"):
                destination_quality = self.GATEWAY.jvm.be.ehealth.businessconnector.ehbox.api.utils.QualityType.PHYSIOTHERAPIST_SSIN
        else:
            if quality_type.startswith("DOCTOR"):
                destination_quality = self.GATEWAY.jvm.be.ehealth.businessconnector.ehbox.api.utils.QualityType.DOCTOR_NIHII
            elif quality_type.startswith("PHYSIOTHERAPIST"):
                destination_quality = self.GATEWAY.jvm.be.ehealth.businessconnector.ehbox.api.utils.QualityType.PHYSIOTHERAPIST_NIHII

        logger.info(f"Using NIHII {id} as destination with quality {destination_quality}")
        destination = self.GATEWAY.jvm.be.ehealth.businessconnector.ehbox.api.domain.Addressee(id, destination_quality)
        logger.info(f"Destination: {destination}")

        message = self.EHEALTH_JVM.createEmptyDocumentMessage()
        logger.info(dir(message))
        document = self.GATEWAY.jvm.be.ehealth.businessconnector.ehbox.api.domain.Document()

        document.setFilename(filename)
        document.setMimeType(mimeType)
        document.setTitle(title)
        document.setContent(content)
        message.setBody(document)
        message.getDestinations().add(destination)
        message.setEncrypted(is_encrypted)
        message.setImportant(is_important)
        message.setUseReceivedReceipt(use_received_receipt)
        message.setUsePublicationReceipt(use_publication_receipt)
        message.setUseReadReceipt(use_read_receipt)

        logger.info(message)

        request = self.GATEWAY.jvm.be.ehealth.businessconnector.ehbox.v3.builders.BuilderFactory.getSendMessageBuilder().buildMessage(message)
        logger.info(self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(request))

        response = service.sendMessage(request)
        logger.info(f"Message sent, response: {response}")