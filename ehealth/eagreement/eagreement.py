import logging
from io import StringIO
from typing import Any, Callable
from xsdata_pydantic.bindings import XmlParser
from .input_models import Patient, AskAgreementInputModel
from .ask_agreement import Bundle as AskResponseBundle, Response as AskResponse
from .consult_agreement import Bundle as ConsultResponseBundle, Response as ConsultResponse
from .async_messages import Response as AsyncResponse
from .eagreement_base import AbstractEAgreementService

logger = logging.getLogger(__name__)

class ServerSideException(Exception):
    pass


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
        logger.info(self.config_validator.getProperty("KEYSTORE_DIR"))
        logger.info(self.config_validator.getProperty("truststore_location"))
        logger.info(self.config_validator.getProperty("CAKEYSTORE_LOCATION"))
        logger.info(self.config_validator.getProperty("CAKEYSTORE_PASSWORD"))
    
    def get_service(self):
        return self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreement.session.AgreementSessionServiceFactory.getAgreementService()
    
    def get_response_builder(self):
        return self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreement.builders.ResponseObjectBuilderFactory.getResponseObjectBuilder()
    
    def verify_result(self, response: Any):
        signVerifResult = response.getSignatureVerificationResult()
        for entry in signVerifResult.getErrors():
            try:
                self.GATEWAY.jvm.org.junit.Assert.assertTrue("Errors found in the signature verification",
                    entry.getValue().isValid())
            except Exception as e:
                logger.exception(e)
                logger.error(entry)
                if "SIGNATURE_NOT_PRESENT" in str(entry):
                    raise ServerSideException("SIGNATURE_NOT_PRESENT, this can usually be solved with a retry ...")

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

        try:
            serviceResponse = self.get_service().askAgreement(request.getRequest())
        except Exception as e:
            if "SEND_TO_IO_EXCEPTION" in str(e.java_exception):
                raise ServerSideException(str(e.java_exception))
            raise e
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
        template, id_ = self.render_consult_agreement_bundle(
            practitioner=practitioner,
            input_model=input_model
        )
        request = self.redundant_template_render(
            template=template,
            patient_ssin=input_model.ssin,
            id_=id_,
            builder_func=self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreement.builders.RequestObjectBuilderFactory.getEncryptedRequestObjectBuilder().buildConsultAgreementRequest
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
        raw_request = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(request)
        logger.info(raw_request)

        service = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreementasync.session.AgreementSessionServiceFactory.getAgrementService()
        serviceResponse = service.getEAgreementResponse(request)
        logger.info(serviceResponse)
        raw_response = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(serviceResponse)
        logger.info(raw_response)

        for i in range(serviceResponse.getMsgResponses().size()):
            processedMsgResponse = serviceResponse.getMsgResponses().get(i) # TODO what if multiple
            self.verify_result(processedMsgResponse)
            msgResponse = processedMsgResponse.getMsgResponse()
            logger.info(msgResponse)
            stringContent = self.GATEWAY.jvm.java.lang.String(processedMsgResponse.getBusinessResponse(), "UTF-8")
            logger.info(stringContent)

        # TODO confirm delivery
        # for now only if decisions, we don't know what to do in other cases
        # AgreementSessionServiceFactory.getAgrementService().confirmAllMessages(response);
        return AsyncResponse(
            response=None,
            transaction_request="",
            transaction_response="",
            soap_request=raw_request,
            soap_response=raw_response
        )