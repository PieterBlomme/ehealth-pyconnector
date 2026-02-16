from py4j.java_gateway import JavaGateway
from typing import Any, Optional, List, Union, Callable
import datetime
import base64
import re
from uuid import uuid4
import logging
from io import StringIO
from ..sts.assertion import Assertion
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata_pydantic.bindings import XmlParser
from py4j.protocol import Py4JJavaError
from .input_models import Record80, Header200, Header300, Footer95, Footer96, ErrorMessage, Header300Refusal, Record10, Record90, Record20, Record50, Record52, Record51, Record91, Record92
from .input_models_kine import Message200KineNoPractitioner, Message200Kine
import tempfile
from pydantic import BaseModel, ConfigDict
from unidecode import unidecode
import sentry_sdk
from ehealth.utils.callbacks import storage_callback, CallMetadata, CallType, ServiceType

logger = logging.getLogger(__name__)

class Practitioner(BaseModel):
    nihii: str
    givenname: str
    surname: str

class TooManyRequestsException(Exception):
    pass

class TACK(BaseModel):
    base64_hash: str
    reference: str
    type: Optional[str] = "Tack"
    value: Optional[bool] = True

class Message(BaseModel):
    model_config = ConfigDict(extra='forbid')
    reference: str
    base64_hash: str
    raw: str
    errors: List[ErrorMessage]
    reden_weigering: Optional[str] = None
    percentage_fouten: Optional[float] = None
    settlements: Optional[List[Union[Record91, Record92]]] = None
    type: Optional[str] = "message"

class Response(BaseModel):
    model_config = ConfigDict(extra='forbid')
    inputReference: str
    transaction_request: str
    transaction_response: str
    soap_request: str
    soap_response: str
    message: Optional[Message] = None


class EFactService:
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
        if environment == "acc":
            self.config_validator.setProperty("endpoint.genericasync.invoicing.v1", "https://pilot.mycarenet.be:9443/mycarenet-ws/async/generic/hcpfac")
        else:
            self.config_validator.setProperty("endpoint.genericasync.invoicing.v1", "https://prod.mycarenet.be:9443/mycarenet-ws/async/generic/hcpfac")


    def set_configuration_from_token(self, token: str) -> Practitioner:
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
        self.config_validator.setProperty("mycarenet.default.careprovider.nihii.value", nihii)
        self.config_validator.setProperty("mycarenet.default.careprovider.nihii.quality", quality)
        self.config_validator.setProperty("mycarenet.default.careprovider.physicalperson.ssin", ssin)
        self.config_validator.setProperty("mycarenet.default.careprovider.physicalperson.name", f"{givenname} {surname}")
        return Practitioner(
                nihii=nihii,
                givenname=givenname,
                surname=surname,
            )
    
    def verify_result(self, response: Any):
        signVerifResult = response.getSignatureVerificationResult()
        for entry in signVerifResult.getErrors():
            self.GATEWAY.jvm.org.junit.Assert.assertTrue("Errors found in the signature verification",
                entry.getValue().isValid())

    def send_efact(self, token: str, input_model: Message200KineNoPractitioner,
                   callback_fn: Optional[Callable] = storage_callback
                   ) -> Response:
        timestamp = datetime.datetime.now()
        meta = CallMetadata(
            type=ServiceType.EFACT,
            timestamp=timestamp,
            call_type=CallType.UNENCRYPTED_REQUEST,
            mutuality=input_model.nummer_ziekenfonds,
            efact_reference=input_model.reference
        )

        practitioner = self.set_configuration_from_token(token)

        # name_contact should be max 45 characters
        name_contact = practitioner.surname
        if len(name_contact) > 45:
            logger.warning(f"Name contact {name_contact} is longer than 45 characters")
            name_contact = name_contact[:45]
        # first name should be max 24 characters
        first_name_contact = practitioner.givenname
        if len(first_name_contact) > 24:
            logger.warning(f"First name contact {first_name_contact} is longer than 24 characters")
            first_name_contact = first_name_contact[:24]

        message_200 = Message200Kine(
            name_contact=name_contact,
            first_name_contact=first_name_contact,
            nummer_derdebetalende=practitioner.nihii,
            nummer_facturerende_instelling=practitioner.nihii,
            **input_model.model_dump()
        )
        for patient_block in message_200.patient_blocks:
            patient_block.nummer_facturerende_instelling = message_200.nummer_facturerende_instelling

        template = str(message_200.to_message200())
        callback_fn(template.encode("utf-8"), meta)

        # Sending unicode characters will mess up
        # the character count, ofcourse ...
        template = unidecode(template)
        with tempfile.NamedTemporaryFile(suffix='.xml', mode='w', delete=False) as tmp:
            # obviously this is lazy ...
            tmp.write(template)

        fp = tmp.name
        mutuality = message_200.nummer_ziekenfonds

        ConnectorIOUtils = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorIOUtils
        PROJECT_NAME = "invoicing"
        contentBytes = ConnectorIOUtils.getBytes(ConnectorIOUtils.getResourceAsStream(fp))
        bbuilder = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.builders.BlobBuilderFactory.getBlobBuilder(PROJECT_NAME)
        blob = bbuilder.build(contentBytes)
        blob.setMessageName("HCPFAC")

        ci = (self.GATEWAY.getCommontInputMapper()
              .map(
                  self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.builders.RequestBuilderFactory
                  .getCommonBuilder("invoicing")
                  .createCommonInput(
                      self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.util.McnConfigUtil.retrievePackageInfo("genericasync." + "invoicing"), self.is_test, input_model.reference)
                  )
        )

        det = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.mapper.DomainBlobMapper.mapBlobToCinBlob(blob)
        blobForXades = self.GATEWAY.jvm.be.ehealth.business.mycarenetcommons.mapper.SendRequestMapper.mapBlobToBlobType(blob)
        xades = self.GATEWAY.jvm.be.ehealth.business.mycarenetcommons.builders.util.BlobUtil.generateXades(blobForXades, "invoicing").getValue()

        post = self.GATEWAY.jvm.be.ehealth.businessconnector.genericasync.builders.BuilderFactory.getRequestObjectBuilder(PROJECT_NAME).buildPostRequest(ci, det, xades)

        logger.info("Send of the post request")

        raw_request = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(post).encode("utf-8")
        inputReference = re.search('<InputReference>(.*)</InputReference>', raw_request.decode("utf-8")).group(1)
        logger.info(f"inputReference: {inputReference}")

        callback_fn(raw_request, meta.set_call_type(CallType.ENCRYPTED_REQUEST))

        service = self.GATEWAY.jvm.be.ehealth.businessconnector.genericasync.session.GenAsyncSessionServiceFactory.getGenAsyncService(PROJECT_NAME)

        header = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.util.WsAddressingUtil.createHeader(mutuality, "urn:be:cin:nip:async:generic:post:msg")

        responsePost = service.postRequest(post, header)
        raw_response = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(responsePost)
        callback_fn(raw_response, meta.set_call_type(CallType.UNENCRYPTED_RESPONSE))

        logger.info("Call of handler for the post operation")
        self.GATEWAY.jvm.be.ehealth.businessconnector.genericasync.builders.BuilderFactory.getResponseObjectBuilder().handlePostResponse(responsePost)

        return Response(
            transaction_request=template,
            transaction_response="",
            soap_request="",
            soap_response=raw_response,
            inputReference=inputReference
        )
    
    @classmethod
    def message_to_object_refusal(cls, decoded: str, base64_hash: str,) -> Message:
        logger.info("mapping refusal")
        # this is a super weird mapping ...
        header_200 = Header200.from_str(decoded[:67])
        header_300 = Header300Refusal.from_str(decoded[67:677])
        logger.info(header_200.reference)
        message = Message(
                    raw=decoded,
                    reference=header_200.reference,
                    base64_hash=base64_hash,
                    errors=[],
                )
        if header_300.refusal_type == "01":
            message.reden_weigering = "Blokkerende fouten"
        elif header_300.refusal_type == "02":
            message.reden_weigering = "Aantal fouten > 5%"
        
        message.percentage_fouten = int(header_300.percentage_errors) / 100.0
        
        logger.info(len(decoded))
        start_record = 677
        errors = []
        message.settlements = []

        while True:
            rec = decoded[start_record:start_record+800]
            logger.info(rec[:2])
            start_record += 800
            if len(rec) == 0:
                break
            else:
                assert len(rec) == 800

            if rec.startswith("95"):
                footer95 = Footer95.from_str(rec)
                errors.extend(footer95.errors())
            elif rec.startswith("96"):
                footer96 = Footer96.from_str(rec)
                errors.extend(footer96.errors())
            elif rec.startswith("10"):
                errors.extend(Record10.errors_from_str(rec))
            elif rec.startswith("20"):
                errors.extend(Record20.errors_from_str(rec))
            elif rec.startswith("50"):
                errors.extend(Record50.errors_from_str(rec))
            elif rec.startswith("51"):
                errors.extend(Record51.errors_from_str(rec))
            elif rec.startswith("52"):
                errors.extend(Record52.errors_from_str(rec))
            elif rec.startswith("80"):
                errors.extend(Record80.errors_from_str(rec))
            elif rec.startswith("90"):
                errors.extend(Record90.errors_from_str(rec))
            elif rec.startswith("91"):
                settlement = Record91.from_str(rec)
                message.settlements.append(settlement)
                logger.info(f"settlement: {settlement}")
            elif rec.startswith("92"):
                settlement = Record92.from_str(rec)
                message.settlements.append(settlement)
                logger.info(f"settlement: {settlement}")
            else:
                # TODO map others to responses
                raise Exception(f"Part of message could not be mapped: {rec}")

        message.errors = errors
        return message
    
    @classmethod
    def message_to_object(cls, decoded: str, base64_hash: str, reference: str) -> Message:
        if decoded[:6] in ("920099", "920900", "920098"):
            # note: 920900 is final acceptance
            # but follows refusal
            return cls.message_to_object_refusal(decoded, base64_hash)
        
        errors = []
        logger.info(f"Length decoded: {len(decoded)}")
        header_200 = Header200.from_str(decoded[:67])
        errors.extend(header_200.errors())

        if not decoded.startswith("931000"):
            # in the case of a 931000
            # the structure is different but
            # there's no meaningful inforomation
            # so just skip
            header_300 = Header300.from_str(decoded[67:227])
            errors.extend(header_300.errors())
        start_record = 227
        while True:
            rec = decoded[start_record:start_record+350]
            start_record += 350
            if len(rec) == 0:
                break
            else:
                if len(rec) != 350:
                    sentry_sdk.capture_message(f"Message type {decoded[:6]} has record of length {len(rec)}: rec")
                    # artificially extend to len 350
                    rec = rec.ljust(350)

            if rec.startswith("95"):
                footer95 = Footer95.from_str(rec)
                errors.extend(footer95.errors())
            elif rec.startswith("96"):
                footer96 = Footer96.from_str(rec)
                errors.extend(footer96.errors())
            else:
                # TODO map others to responses
                logger.warning(f"Part of message could not be mapped: {rec} for type {decoded[:6]}")
                sentry_sdk.capture_message(f"Part of message could not be mapped: {decoded}")

        return Message(
                    raw=decoded,
                    reference=reference,
                    base64_hash=base64_hash,
                    errors=errors
                )

    def get_messages(self, token: str, callback_fn: Optional[Callable] = storage_callback):
        self.set_configuration_from_token(token)
        logger.info("Creation of the get")
        msgQuery = self.EHEALTH_JVM.newMsgQuery()
        msgQuery.setInclude(True)
        msgQuery.setMax(200)
        msgQuery.getMessageNames().add("HCPFAC")
        msgQuery.getMessageNames().add("HCPAFD")
        msgQuery.getMessageNames().add("HCPVWR")

        tackQuery = self.EHEALTH_JVM.newQuery()
        tackQuery.setInclude(True)
        tackQuery.setMax(100)
        logger.info("Send of the get request")

        PROJECT_NAME = "invoicing"
        packageInfo = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.util.McnConfigUtil.retrievePackageInfo("genericasync." + PROJECT_NAME)
        commonBuilder = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.builders.RequestBuilderFactory.getCommonBuilder(PROJECT_NAME)
        service = self.GATEWAY.jvm.be.ehealth.businessconnector.genericasync.session.GenAsyncSessionServiceFactory.getGenAsyncService(PROJECT_NAME)
        origin = self.EHEALTH_JVM.getCommontInputMapper().map(commonBuilder.createOrigin(packageInfo))
        responseGetHeader = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.util.WsAddressingUtil.createHeader(None, "urn:be:cin:nip:async:generic:get:query")
        
        try:
            get_request = self.GATEWAY.jvm.be.ehealth.businessconnector.genericasync.builders.BuilderFactory.getRequestObjectBuilder(PROJECT_NAME).buildGetRequest(origin, msgQuery, tackQuery)
            raw_request = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(get_request).encode("utf-8")
            meta = CallMetadata(
                type=ServiceType.ASYNC_MESSAGES_EFACT,
                timestamp=datetime.datetime.now(),
                call_type=CallType.UNENCRYPTED_REQUEST,
            )
            callback_fn(raw_request, meta)

            responseGet = service.getRequest(
                get_request,
                responseGetHeader
                )
        except Py4JJavaError as e:
            if "Not enough time" in e.java_exception.getMessage():
                raise TooManyRequestsException
            else:
                raise e
        
        #  validate the get responses ( including check on xades if present)
        # self.GATEWAY.jvm.be.ehealth.businessconnector.genericasync.builders.BuilderFactory.getResponseObjectBuilder().handleGetResponse(responseGet)
        logger.info("getMsgResponses")

        messages = []

        for msgResponse in responseGet.getReturn().getMsgResponses():
            raw_message = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(msgResponse)
            reference = re.search('<InputReference>(.*)</InputReference>', raw_message).group(1)
            logger.info(f"Received message with reference: {reference}")

            # separate timestamp per request
            timestamp = datetime.datetime.now()            
            xades = msgResponse.getXadesT().getValue()
            meta = CallMetadata(
                type=ServiceType.ASYNC_MESSAGES_EFACT,
                timestamp=timestamp,
                call_type=CallType.XADES_RESPONSE,
            )
            callback_fn(xades, meta)

            detail = msgResponse.getDetail()
            hash = detail.getHashValue()
            base64_hash = base64.b64encode(hash).decode('utf8')
            mappedBlob = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.mapper.DomainBlobMapper.mapToBlob(detail)
            unwrappedMessageByteArray = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.builders.BlobBuilderFactory.getBlobBuilder(PROJECT_NAME).checkAndRetrieveContent(mappedBlob)
            decoded = unwrappedMessageByteArray.decode("utf-8")
            
            try:
                message_object = self.message_to_object(decoded, base64_hash, reference)
                messages.append(message_object)
                meta = CallMetadata(
                    type=ServiceType.ASYNC_MESSAGES_EFACT,
                    timestamp=timestamp,
                    call_type=CallType.UNENCRYPTED_RESPONSE,
                    efact_reference=message_object.reference
                )
            except Exception as e:
                logger.exception(e)
                logger.info(f"Failed to convert message with hash {base64_hash}")
                sentry_sdk.capture_message(f"Part of message could not be mapped: {decoded}")
                with open(f"{uuid4()}.txt", "w") as f:
                    f.write(decoded)
                meta = CallMetadata(
                    type=ServiceType.ASYNC_MESSAGES_EFACT,
                    timestamp=timestamp,
                    call_type=CallType.UNENCRYPTED_RESPONSE,
                )
            callback_fn(unwrappedMessageByteArray, meta)

        logger.info("getTAckResponses")
        for tackResponse in responseGet.getReturn().getTAckResponses():

            # separate timestamp per request
            timestamp = datetime.datetime.now()
            
            xades = tackResponse.getXadesT().getValue()
            meta = CallMetadata(
                type=ServiceType.ASYNC_MESSAGES_EFACT,
                timestamp=timestamp,
                call_type=CallType.XADES_RESPONSE,
            )
            callback_fn(xades, meta)
            # just always confirm TAck messages, I guess
            tack = tackResponse.getTAck()
            tackAppliesTo = tack.getAppliesTo()
            tackReference = tackAppliesTo.replace("urn:nip:reference:input:", "")
            tackResponseBytes = tack.getValue()
            logger.info(f"Received Tack message with reference: {tackReference}")

            base64_hash = base64.b64encode(tackResponseBytes).decode('utf8')
            
            messages.append(TACK(
                reference=tackReference,
                base64_hash=base64_hash
            ))

            meta = CallMetadata(
                type=ServiceType.ASYNC_MESSAGES_EFACT_TACK,
                timestamp=timestamp,
                call_type=CallType.UNENCRYPTED_RESPONSE,
            )
            callback_fn(tackResponseBytes, meta)

            # self.confirm_message(token, base64_hash, tack=True)
        return messages


    def confirm_message(self, token: str, base64_hash: str, tack: bool = False):
        self.set_configuration_from_token(token)

        hash = base64.b64decode(base64_hash)
        logger.info(hash)

        PROJECT_NAME = "invoicing"
        packageInfo = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.util.McnConfigUtil.retrievePackageInfo("genericasync." + PROJECT_NAME)
        commonBuilder = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.builders.RequestBuilderFactory.getCommonBuilder(PROJECT_NAME)
        service = self.GATEWAY.jvm.be.ehealth.businessconnector.genericasync.session.GenAsyncSessionServiceFactory.getGenAsyncService(PROJECT_NAME)
        origin = self.EHEALTH_JVM.getCommontInputMapper().map(commonBuilder.createOrigin(packageInfo))
        if not tack:
            logger.info(f"confirming message with hash {hash}")
            self.EHEALTH_JVM.confirmMessage(origin, service, hash)
        else:
            logger.info(f"confirming TAck message with hash {hash}")
            self.EHEALTH_JVM.confirmTAckMessage(origin, service, hash)
