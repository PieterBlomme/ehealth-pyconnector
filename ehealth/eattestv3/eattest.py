from py4j.java_gateway import JavaGateway
from typing import Any
import uuid
import logging
from .input_models import Practitioner
from io import StringIO
from ..sts.assertion import Assertion
from xsdata_pydantic.bindings import XmlParser

logger = logging.getLogger(__name__)

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
            )
    
    def verify_result(self, response: Any):
        signVerifResult = response.getSignatureVerificationResult()
        for entry in signVerifResult.getErrors():
            self.GATEWAY.jvm.org.junit.Assert.assertTrue("Errors found in the signature verification",
                entry.getValue().isValid())
                
    def send_attestation(self, token: str):
        practitioner = self.set_configuration_from_token(token)

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