from py4j.java_gateway import JavaGateway
from typing import Any, Optional
import datetime
from random import randint
import logging
from io import StringIO
from ..sts.assertion import Assertion
from xsdata.models.datatype import XmlDate, XmlTime
from xsdata_pydantic.bindings import XmlSerializer, XmlParser
from py4j.protocol import Py4JJavaError
from .input_models import Message200, Header200, Header300, Message200KineNoPractitioner, Message200Kine
import tempfile
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class Practitioner(BaseModel):
    nihii: str
    givenname: str
    surname: str

class TooManyRequestsException(Exception):
    pass

class EFactService:
    def __init__(
            self,
            mycarenet_license_username: str,
            mycarenet_license_password: str,
            etk_endpoint: str = "$uddi{uddi:ehealth-fgov-be:business:etkdepot:v1}",
            environment: str = "acc",
            confirm_messages: Optional[bool] = False
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
        self.confirm_messages = confirm_messages

        self.config_validator.setProperty("mycarenet.licence.username", mycarenet_license_username)
        self.config_validator.setProperty("mycarenet.licence.password", mycarenet_license_password)
        self.config_validator.setProperty("endpoint.etk", etk_endpoint)

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

    def send_efact(self, token: str, input_model: Message200KineNoPractitioner):
        practitioner = self.set_configuration_from_token(token)

        message_200 = Message200Kine(
            name_contact=practitioner.surname,
            first_name_contact=practitioner.givenname,
            nummer_derdebetalende=practitioner.nihii,
            nummer_facturerende_instelling=practitioner.nihii,
            **input_model.dict()
        )

        template = str(message_200.to_message200())
        with tempfile.NamedTemporaryFile(suffix='.xml', mode='w', delete=False) as tmp:
            # obviously this is lazy ...
            tmp.write(template)

        fp = tmp.name
        mutuality = "500"



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
                      self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.util.McnConfigUtil.retrievePackageInfo("genericasync." + "invoicing"), False, inputReference)
                  )
        )

        det = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.mapper.DomainBlobMapper.mapBlobToCinBlob(blob)
        blobForXades = self.GATEWAY.jvm.be.ehealth.business.mycarenetcommons.mapper.SendRequestMapper.mapBlobToBlobType(blob)
        xades = self.GATEWAY.jvm.be.ehealth.business.mycarenetcommons.builders.util.BlobUtil.generateXades(blobForXades, "invoicing").getValue()

        post = self.GATEWAY.jvm.be.ehealth.businessconnector.genericasync.builders.BuilderFactory.getRequestObjectBuilder(PROJECT_NAME).buildPostRequest(ci, det, xades)

        logger.info("Send of the post request")
        service = self.GATEWAY.jvm.be.ehealth.businessconnector.genericasync.session.GenAsyncSessionServiceFactory.getGenAsyncService(PROJECT_NAME)

        header = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.util.WsAddressingUtil.createHeader(mutuality, "urn:be:cin:nip:async:generic:post:msg");

        responsePost = service.postRequest(post, header)
        raw_response = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(responsePost)
        logger.info(raw_response)
        logger.info("Call of handler for the post operation")
        self.GATEWAY.jvm.be.ehealth.businessconnector.genericasync.builders.BuilderFactory.getResponseObjectBuilder().handlePostResponse(responsePost)

    def get_messages(self):
        logger.info("Creation of the get")
        msgQuery = self.EHEALTH_JVM.newMsgQuery()
        msgQuery.setInclude(True)
        msgQuery.setMax(200)
        msgQuery.getMessageNames().add("HCPFAC")

        tackQuery = self.EHEALTH_JVM.newQuery()
        tackQuery.setInclude(False)
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
            
        #  validate the get responses ( including check on xades if present)
        self.GATEWAY.jvm.be.ehealth.businessconnector.genericasync.builders.BuilderFactory.getResponseObjectBuilder().handleGetResponse(responseGet)
        logger.info("getMsgResponses")
        for msgResponse in responseGet.getReturn().getMsgResponses():
            logger.info(f"msgResponse: {msgResponse}")
            mappedBlob = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.mapper.DomainBlobMapper.mapToBlob(msgResponse.getDetail())
            unwrappedMessageByteArray = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.builders.BlobBuilderFactory.getBlobBuilder(PROJECT_NAME).checkAndRetrieveContent(mappedBlob)
            decoded = unwrappedMessageByteArray.decode("utf-8")
            logger.info(msgResponse)
            header_200 = Header200.from_str(decoded[:67])
            header_300 = Header300.from_str(decoded[67:227])
            logger.info(header_200.dict())
            logger.info(header_300.dict())
        logger.info("getTAckResponses")
        for tackResponse in responseGet.getReturn().getTAckResponses():
            tackResponseBytes = tackResponse.getTAck().getValue()
            tackResponse = self.GATEWAY.jvm.java.lang.String(tackResponseBytes, "UTF-8")
            logger.info(tackResponse)

        # confirm messages
        if self.confirm_messages:
            self.EHEALTH_JVM.confirmTheseMessages(origin, service, responseGet)
