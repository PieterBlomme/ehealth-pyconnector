from py4j.java_gateway import JavaGateway
from typing import Any
import datetime
from random import randint
import logging
from .input_models import Practitioner
from io import StringIO
from ..sts.assertion import Assertion
from xsdata.models.datatype import XmlDate, XmlTime
from xsdata_pydantic.bindings import XmlSerializer, XmlParser
from pydantic import BaseModel
from .send_transaction_request import (
    SendTransactionRequest,
    Request,
    Id2,
    Author2,
    Hcparty,
    Id1, Cd
)

logger = logging.getLogger(__name__)

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

class EAttestV3Service:
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
                ssin=ssin
            )
    
    def verify_result(self, response: Any):
        signVerifResult = response.getSignatureVerificationResult()
        for entry in signVerifResult.getErrors():
            self.GATEWAY.jvm.org.junit.Assert.assertTrue("Errors found in the signature verification",
                entry.getValue().isValid())
    
    def render_request(self, practitioner: Practitioner):
        random_n14 = random_with_N_digits(14)
        now = datetime.datetime.now().replace(microsecond=0)
        return Request(
            id=Id2(value=f"{practitioner.nihii}.{random_n14}"),
            author=Author2(
                hcparty=Hcparty(
                    id=[
                        Id1(s="ID-HCPARTY", value=practitioner.nihii),
                        Id1(s="INSS", value=practitioner.ssin),                        
                    ],
                    cd=Cd(s="CD-HCPARTY", sv="1.14", value="persphysiotherapist"),
                    firstname=practitioner.givenname,
                    familyname=practitioner.surname
                )
            ),
            date=XmlDate.from_date(now),
            time=XmlTime.from_time(now),
        )

    @classmethod
    def serialize_template(cls, bundle: BaseModel):
        serializer = XmlSerializer()
        serializer.config.pretty_print = True
        # serializer.config.xml_declaration = True
        ns_map = {
            "" : "",
            "xmlns": "http://www.ehealth.fgov.be/messageservices/protocol/v1",
            "msgws": "http://www.ehealth.fgov.be/messageservices/core/v1",
            "kmehr": "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"
        }
        return serializer.render(bundle, ns_map)
    
    def send_attestation(self, token: str):
        practitioner = self.set_configuration_from_token(token)
        kmehrmessage = SendTransactionRequest(
            request=self.render_request(practitioner)
        )
        template = self.serialize_template(kmehrmessage)
        logger.info(template)
        return

        with open("/home/pieter/repos/ehealth-pyconnector/java/config/examples/mycarenet/attestv3/requests/mha-request-detail.xml", "rb") as f:
            kmehrmessage = f.read()

        inputReference = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.domain.InputReference("01-KIN-EMEH")

        # inputAttrs = self.GATEWAY.jvm.java.util.Arrays.asList(purpose, attemptNbr)
        send_attest_request = (self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.attestv3.builders.SendAttestationRequestInput
                               .builder()
                               .isTest(self.is_test)
                               .inputReference(inputReference)
                               .kmehrmessage(kmehrmessage)
                                .patientSsin(self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.domain.Ssin("72070539942"))
                                .referenceDate(self.GATEWAY.jvm.java.time.LocalDateTime.now())
                                .messageVersion("3.0")
                                .issuer("some issuer")
                                .commonInputAttributes(self.EHEALTH_JVM.commonInputAttributes())
                                .build())       
        attestBuilderRequest = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.attestv3.builders.RequestObjectBuilderFactory.getRequestObjectBuilder().buildSendAttestationRequest(
            send_attest_request
        )
        sendAttestationResponse = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.attestv3.session.AttestSessionServiceFactory.getAttestService().sendAttestation(attestBuilderRequest.getSendAttestationRequest())

        attestResponse = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.attestv3.builders.ResponseObjectBuilderFactory.getResponseObjectBuilder().handleSendAttestionResponse(sendAttestationResponse, attestBuilderRequest);
        self.verify_result(attestResponse)
        response_string = self.GATEWAY.jvm.java.lang.String(attestResponse.getBusinessResponse(), "UTF-8")
        logger.info(response_string)