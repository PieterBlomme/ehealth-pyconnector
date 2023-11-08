from py4j.java_gateway import JavaGateway
import uuid

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

    def send_attestation(self):
        with open("/home/pieter/repos/ehealth-pyconnector/java/config/examples/mycarenet/attestv3/requests/mha-request-detail.xml", "rb") as f:
            kmehrmessage = f.read()

        inputReference = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.domain.InputReference(str(uuid.uuid4()))
        purpose = (self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.domain.Attribute.builder()
                                                .key("urn:be:cin:nippin:purpose")
                                                .value("some purpose")
                                                .build())
        attemptNbr = (self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.domain.Attribute.builder()
                                                .key("urn:be:cin:nippin:attemptNbr")
                                                .value(1)
                                                .build())
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
                                .commonInputAttributes(
                                    self.GATEWAY.jvm.java.util.Arrays.asList(self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.domain.Attribute.builder()
                                                .key("urn:be:cin:nippin:purpose")
                                                .value("some purpose")
                                                .build()),
                                        self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.domain.Attribute.builder()
                                                .key("urn:be:cin:nippin:attemptNbr")
                                                .value(1)
                                                .build()
                                                )
                                .build())       
        attestBuilderRequest = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.attestv3.builders.RequestObjectBuilderFactory.getRequestObjectBuilder().buildSendAttestationRequest(
            send_attest_request
        )
        sendAttestationResponse = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.attestv3.session.AttestSessionServiceFactory.getAttestService().sendAttestation(attestBuilderRequest.getSendAttestationRequest())

        attestResponse = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.attestv3.builders.ResponseObjectBuilderFactory.getResponseObjectBuilder().handleSendAttestionResponse(sendAttestationResponse, attestBuilderRequest);
    
        import logging
        logging.info(attestResponse)
        signatureVerificationResult = attestResponse.getSignatureVerificationResult()
        logging.info(signatureVerificationResult)
        # Assert.assertTrue("Errors found in the signature verification", signatureVerificationResult.isValid());
        # String expectedResponse = ConnectorIOUtils.getResourceAsString("/examples/mycarenet/attestv3/responses/mha-response-detail-" + inputReference + ".xml");
        # XmlAsserter.assertSimilar(expectedResponse, new String(attestResponse.getBusinessResponse(), UTF_8.name()));