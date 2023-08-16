import logging
from io import StringIO
from typing import Any, Callable
from xsdata_pydantic.bindings import XmlParser
from .input_models import Patient, AskAgreementInputModel
from .ask_agreement import Bundle as AskResponseBundle, Response as AskResponse
from .consult_agreement import Bundle as ConsultResponseBundle, Response as ConsultResponse
from .eagreement_base import AbstractEAgreementService

logger = logging.getLogger(__name__)

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
    
    def get_service(self):
        return self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreement.session.AgreementSessionServiceFactory.getAgreementService()
    
    def get_response_builder(self):
        return self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreement.builders.ResponseObjectBuilderFactory.getResponseObjectBuilder()
    
    def verify_result(self, response: Any):
        signVerifResult = response.getSignatureVerificationResult()
        for entry in signVerifResult.getErrors():
            self.GATEWAY.jvm.org.junit.Assert.assertTrue("Errors found in the signature verification",
                  entry.getValue().isValid())
    

    def convert_response_to_pydantic(self, response: any, target_class: Callable):
        parser = XmlParser()
        response_string = self.GATEWAY.jvm.java.lang.String(response.getBusinessResponse(), "UTF-8")
        try:
            return parser.parse(StringIO(response_string), target_class)  
        except:
            logger.error(response_string)
            raise
    
    def ask_agreement(
        self, 
        token: str,
        input_model: AskAgreementInputModel
        ) -> str:
        practitioner = self.set_configuration_from_token(token)

        template, id_ = self.render_ask_or_extend_agreement_bundle(
            practitioner=practitioner,
            input_model=input_model
        )
        request = self.redundant_template_render(
            template=template,
            patient_ssin=input_model.patient.ssin,
            id_=id_,
            builder_func=self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreement.builders.RequestObjectBuilderFactory.getEncryptedRequestObjectBuilder().buildAskAgreementRequest
            )
        
        raw_request = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(request)

        serviceResponse = self.get_service().askAgreement(request.getRequest())
        raw_response = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(serviceResponse)

        response = self.get_response_builder().handleAskAgreementResponse(serviceResponse, request)
        self.verify_result(response)

        response_string = self.GATEWAY.jvm.java.lang.String(response.getBusinessResponse(), "UTF-8")
        response_pydantic = self.convert_response_to_pydantic(response, AskResponseBundle)
        return AskResponse(
            response=response_pydantic,
            transaction_request=template,
            transaction_response=response_string,
            soap_request=raw_request,
            soap_response=raw_response
        )

    def consult_agreement(
        self, 
        token: str,
        input_model: Patient
        ) -> str:
        practitioner = self.set_configuration_from_token(token)
        request, template = self.render_consult_agreement_bundle(
            practitioner=practitioner,
            input_model=input_model
        )

        raw_request = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(request)

        serviceResponse = self.get_service().consultAgreement(request.getRequest())
        raw_response = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(serviceResponse)

        response = self.get_response_builder().handleConsultAgreementResponse(serviceResponse, request)
        self.verify_result(response)

        response_string = self.GATEWAY.jvm.java.lang.String(response.getBusinessResponse(), "UTF-8")
        response_pydantic = self.convert_response_to_pydantic(response, ConsultResponseBundle)
        return ConsultResponse(
            response=response_pydantic,
            transaction_request=template,
            transaction_response=response_string,
            soap_request=raw_request,
            soap_response=raw_response
        )
    
    def async_messages(
            self,
            token: str,
    ):
        practitioner = self.set_configuration_from_token(token)

        request = self.GATEWAY.jvm.be.ehealth.businessconnector.genericasync.domain.GetRequest.newBuilder().withDefaults().build()
        service = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreementasync.session.AgreementSessionServiceFactory.getAgrementService()
        response = service.getEAgreementResponse(request)

        logger.info(response.getMsgResponses().size())

        # ProcessedMsgResponse<byte[]> processedMsgResponse = response.getMsgResponses().get(0);
        # assertEquals("SignatureVerificationResult should contain no error", 0, processedMsgResponse.getSignatureVerificationResult().getErrors().size());
        # MsgResponse msgResponse = processedMsgResponse.getMsgResponse();
        # assertNotNull("Missing xades", msgResponse.getXadesT());
        # XmlAsserter.assertSimilar(ConnectorXmlUtils.toObject(processedMsgResponse.getSignedData(), EncryptedKnownContent.class), processedMsgResponse.getRawDecryptedBlob());
        # byte[] businessContent = processedMsgResponse.getBusinessResponse();
        # String stringContent = new String(businessContent, "UTF-8");
        # XmlAsserter.assertSimilar(ConnectorIOUtils.getResourceAsString("/examples/mycarenet/eagreementasync/expected/eAgreementResponse.xml"), stringContent);

        # AgreementSessionServiceFactory.getAgrementService().confirmAllMessages(response);