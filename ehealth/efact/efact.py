from py4j.java_gateway import JavaGateway
from typing import Any, Optional, List, Union
import base64
from uuid import uuid4
from random import randint
import logging
from io import StringIO
from ..sts.assertion import Assertion
from xsdata.models.datatype import XmlDate, XmlTime
from xsdata_pydantic.bindings import XmlSerializer, XmlParser
from py4j.protocol import Py4JJavaError
from .input_models import Record80, Header200, Header300, Footer95, Footer96, ErrorMessage, Header300Refusal, Record10, Record90, Record20, Record50, Record52, Record51, Record91, Record92
from .input_models_kine import Message200KineNoPractitioner, Message200Kine
import tempfile
from pydantic import BaseModel
from pydantic import Extra
from pydantic.dataclasses import dataclass
from unidecode import unidecode
import sentry_sdk

logger = logging.getLogger(__name__)

class Practitioner(BaseModel):
    nihii: str
    givenname: str
    surname: str

class TooManyRequestsException(Exception):
    pass

class Config:
    extra = Extra.forbid

@dataclass(config=Config)
class Message:
    reference: str
    base64_hash: str
    errors: List[ErrorMessage]
    reden_weigering: Optional[str] = None
    percentage_fouten: Optional[float] = None
    settlements: Optional[List[Union[Record91, Record92]]] = None

@dataclass(config=Config)
class Response:
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
            # TODO double check in production
            self.config_validator.setProperty("endpoint.genericasync.eagreement.v1", "https://services.ehealth.fgov.be/MyCareNet/hcpfac/v1")


    def set_configuration_from_token(self, token: str) -> Practitioner:
        # TODO copy paste from MDA
        parser = XmlParser()
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

    def send_efact(self, token: str, input_model: Message200KineNoPractitioner) -> Response:
        practitioner = self.set_configuration_from_token(token)

        message_200 = Message200Kine(
            name_contact=practitioner.surname,
            first_name_contact=practitioner.givenname,
            nummer_derdebetalende=practitioner.nihii,
            nummer_facturerende_instelling=practitioner.nihii,
            **input_model.dict()
        )

        template = str(message_200.to_message200())
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

        inputReference = self.GATEWAY.jvm.be.ehealth.technicalconnector.idgenerator.IdGeneratorFactory.getIdGenerator().generateId()
        ci = (self.GATEWAY.getCommontInputMapper()
              .map(
                  self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.builders.RequestBuilderFactory
                  .getCommonBuilder("invoicing")
                  .createCommonInput(
                      self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.util.McnConfigUtil.retrievePackageInfo("genericasync." + "invoicing"), self.is_test, inputReference)
                  )
        )

        det = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.mapper.DomainBlobMapper.mapBlobToCinBlob(blob)
        blobForXades = self.GATEWAY.jvm.be.ehealth.business.mycarenetcommons.mapper.SendRequestMapper.mapBlobToBlobType(blob)
        xades = self.GATEWAY.jvm.be.ehealth.business.mycarenetcommons.builders.util.BlobUtil.generateXades(blobForXades, "invoicing").getValue()

        post = self.GATEWAY.jvm.be.ehealth.businessconnector.genericasync.builders.BuilderFactory.getRequestObjectBuilder(PROJECT_NAME).buildPostRequest(ci, det, xades)

        logger.info("Send of the post request")
        service = self.GATEWAY.jvm.be.ehealth.businessconnector.genericasync.session.GenAsyncSessionServiceFactory.getGenAsyncService(PROJECT_NAME)

        header = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.util.WsAddressingUtil.createHeader(mutuality, "urn:be:cin:nip:async:generic:post:msg")

        responsePost = service.postRequest(post, header)
        raw_response = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(responsePost)
        logger.info(raw_response)
        logger.info("Call of handler for the post operation")
        self.GATEWAY.jvm.be.ehealth.businessconnector.genericasync.builders.BuilderFactory.getResponseObjectBuilder().handlePostResponse(responsePost)

        return Response(
            transaction_request=template,
            transaction_response="",
            soap_request="",
            soap_response=raw_response
        )
    
    def message_to_object_refusal(self, decoded: str, base64_hash: str) -> Response:
        logger.info("mapping refusal")
        # this is a super weird mapping ...
        header_200 = Header200.from_str(decoded[:67])
        header_300 = Header300Refusal.from_str(decoded[67:677])
        logger.info(header_200.reference)
        message = Message(
                    reference=header_200.reference,
                    base64_hash=base64_hash,
                    errors=[],
                )
        if header_300.refusal_type == "01":
            message.reden_weigering = "Blokkerende fouten"
        else:
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
        return Response(
                transaction_request="",
                transaction_response=decoded,
                soap_request="",
                soap_response="",
                message=message
            )
    
    def message_to_object(self, decoded: str, base64_hash: str) -> Response:
        if decoded[:6] in ("920099", "920900"):
            # note: 920900 is final acceptance
            # but follows refusal
            return self.message_to_object_refusal(decoded, base64_hash)
        
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

        
        if decoded[:6] != "920098":
            start_record = 227
            while True:
                rec = decoded[start_record:start_record+350]
                start_record += 350
                if len(rec) == 0:
                    break
                else:
                    assert len(rec) == 350, f"len(rec) is {len(rec)}"

                if rec.startswith("95"):
                    footer95 = Footer95.from_str(rec)
                    errors.extend(footer95.errors())
                elif rec.startswith("96"):
                    footer96 = Footer96.from_str(rec)
                    errors.extend(footer96.errors())
                else:
                    # TODO map others to responses
                    logger.warning(f"Part of message could not be mapped: {rec}")
                    sentry_sdk.capture_message(f"Part of message could not be mapped: {decoded}")

        return Response(
                transaction_request="",
                transaction_response=decoded,
                soap_request="",
                soap_response="",
                message=Message(
                    reference=header_200.reference,
                    base64_hash=base64_hash,
                    errors=errors
                )
            )

    def get_messages(self, token: str):
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
            responseGet = service.getRequest(
                self.GATEWAY.jvm.be.ehealth.businessconnector.genericasync.builders.BuilderFactory.getRequestObjectBuilder(PROJECT_NAME).buildGetRequest(origin, msgQuery, tackQuery), 
                responseGetHeader
                )
        except Py4JJavaError as e:
            if "Not enough time" in e.java_exception.getMessage():
                raise TooManyRequestsException
            else:
                raise e
            
        #  validate the get responses ( including check on xades if present)
        self.GATEWAY.jvm.be.ehealth.businessconnector.genericasync.builders.BuilderFactory.getResponseObjectBuilder().handleGetResponse(responseGet)
        logger.info("getMsgResponses")

        messages = []

        for msgResponse in responseGet.getReturn().getMsgResponses():
            detail = msgResponse.getDetail()
            hash = detail.getHashValue()
            base64_hash = base64.b64encode(hash).decode('utf8')
            logger.info(f"hash: {base64_hash}")
            mappedBlob = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.mapper.DomainBlobMapper.mapToBlob(detail)
            unwrappedMessageByteArray = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.builders.BlobBuilderFactory.getBlobBuilder(PROJECT_NAME).checkAndRetrieveContent(mappedBlob)
            decoded = unwrappedMessageByteArray.decode("utf-8")
            try:
                messages.append(self.message_to_object(decoded, base64_hash))
            except Exception as e:
                logger.info(f"Failed to convert message with hash {base64_hash}")
                sentry_sdk.capture_message(f"Part of message could not be mapped: {decoded}")
                with open(f"{uuid4()}.txt", "w") as f:
                    f.write(decoded)

        logger.info("getTAckResponses")
        for tackResponse in responseGet.getReturn().getTAckResponses():
            # just always confirm TAck messages, I guess
            tackResponseBytes = tackResponse.getTAck().getValue()
            base64_hash = base64.b64encode(tackResponseBytes).decode('utf8')
            logger.info(f"hash: {base64_hash}")
            self.confirm_message(token, base64_hash, tack=True)
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