from py4j.java_gateway import JavaGateway
import logging
import datetime
import tempfile
import uuid
from typing import List, Optional, Tuple
from pydantic import BaseModel, root_validator
from io import StringIO
from ..sts.assertion import Assertion
from xsdata.models.datatype import XmlDateTime
from xsdata_pydantic.bindings import XmlSerializer, XmlParser
from .bundle import (
    Bundle, Entry, FullUrl, Resource, MessageHeader, MetaType, Profile, Timestamp,
    EventCoding, Destination, Sender, Source, Focus, System, Code, Endpoint,
    Reference, Organization, Id, Identifier, TypeType, Value, Coding
)

logger = logging.getLogger(__name__)


class AbstractEAgreementService:
    def __init__(
            self,
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

    def set_configuration_from_token(self, token: str):
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
        return nihii
    
class EAgreementService(AbstractEAgreementService):
    def __init__(
            self,
            mycarenet_license_username: str,
            mycarenet_license_password: str,
            etk_endpoint: str = "$uddi{uddi:ehealth-fgov-be:business:etkdepot:v1}",
            environment: str = "acc",
    ):
        super().__init__(environment=environment)
    
        # set up required configuration        
        self.config_validator.setProperty("mycarenet.licence.username", mycarenet_license_username)
        self.config_validator.setProperty("mycarenet.licence.password", mycarenet_license_password)
        self.config_validator.setProperty("endpoint.etk", etk_endpoint)

    def render_bundle(
        self
        ):
        id_ = str(uuid.uuid4())
        id2_ = str(uuid.uuid4())
        now = datetime.datetime.now()

        message_header = Entry(
                    full_url=FullUrl("urn:uuid:MessageHeader"),
                    resource=Resource(
                        message_header=MessageHeader(
                            id=Id(id2_),
                            meta=MetaType(Profile("http://www.mycarenet.be/standards/fhir/StructureDefinition/be-messageheader")),
                            event_coding=EventCoding(
                                system=System("http://www.mycarenet.be/fhir/CodeSystem/message-events"),
                                code=Code("claim-ask")
                            ),
                            source=Source(Endpoint("urn:uuid:Organization1")),
                            sender=Sender(Reference("Organization/Organization1")),
                            focus=Focus(Reference("Claim/Claim1")),            
                        )
                    )
                )
        
        organization = Entry(
                    full_url=FullUrl("urn:uuid:Organization1"),
                    resource=Resource(
                        organization=Organization(
                            id=Id("Organization1"),
                            meta=MetaType(Profile("http://www.mycarenet.be/standards/fhir/StructureDefinition/be-organization")),
                            identifier=Identifier(
                                system=System("https://www.ehealth.fgov.be/standards/fhir/NamingSystem/nihdi"),
                                value=Value("71000436000")
                            ),
                            type=TypeType(
                                EventCoding(
                                    system=System("https://www.ehealth.fgov.be/standards/fhir/CodeSystem/cd-hcparty"),
                                    code=Code(value="orghospital")
                                )
                            )
                        )
                    )
                )
        
        bundle = Bundle(
            id=Id(id_),
            timestamp=Timestamp(XmlDateTime.from_datetime(now)),
            type=TypeType(value="message"),
            entry=[
                message_header,
                organization,
            ]
        )
        
        serializer = XmlSerializer()
        serializer.config.pretty_print = True
        serializer.config.xml_declaration = True
        ns_map = {
            "samlp": "urn:oasis:names:tc:SAML:2.0:protocol",
            "saml": "urn:oasis:names:tc:SAML:2.0:assertion",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "ext": "urn:be:cin:nippin:memberdata:saml:extension"
        }
        return serializer.render(bundle, ns_map), id_
    
    def ask_agreement(
        self, 
        token: str,
        bundleLocation: str,
        patientNiss: str = "72070539942"
        ) -> str:
        template, id_ = self.render_bundle()
        responseBuilder = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreement.builders.ResponseObjectBuilderFactory.getResponseObjectBuilder()

        logger.info(template)
        with open(bundleLocation, "rb") as f:
            bundle = f.read()
        # bundle = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorIOUtils.getResourceAsString(bundleLocation).getBytes(
        #     self.GATEWAY.jvm.be.ehealth.technicalconnector.enumeration.Charset.UTF_8.getName()
        #     )
        self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.dump(bundle)

        patientInfo = self.GATEWAY.jvm.be.ehealth.business.common.domain.Patient()
        patientInfo.setInss(patientNiss)

        # input reference and AttributeQuery ID must match
        inputReference = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.domain.InputReference(id_)
        askRequest = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreement.builders.RequestObjectBuilderFactory.getEncryptedRequestObjectBuilder().buildAskAgreementRequest(
            self.is_test, 
            inputReference, 
            patientInfo, 
            self.GATEWAY.jvm.org.joda.time.DateTime(), 
            bundle
            )
        raw_request = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(askRequest)
        # logger.info(raw_request)

        service = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreement.session.AgreementSessionServiceFactory.getAgreementService()
        serviceResponse = service.askAgreement(askRequest.getRequest())
        response = responseBuilder.handleAskAgreementResponse(serviceResponse, askRequest)
        signVerifResult = response.getSignatureVerificationResult()
        for entry in signVerifResult.getErrors():
            self.GATEWAY.jvm.org.junit.Assert.assertTrue("Errors found in the signature verification",
                  entry.getValue().isValid())
        logger.info(self.GATEWAY.jvm.java.lang.String(response.getBusinessResponse(), "UTF-8"))
        return ""