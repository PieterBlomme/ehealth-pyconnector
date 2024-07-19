import logging
import datetime
from io import StringIO
from typing import Any, Callable, Optional
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata_pydantic.bindings import XmlParser
from .input_models import Patient, AskAgreementInputModel
from .ask_agreement import Bundle as AskResponseBundle, Response as AskResponse
from .consult_agreement import Bundle as ConsultResponseBundle, Response as ConsultResponse
from .async_messages import Bundle as AsyncBundle, Response as AsyncResponse
from .eagreement_base import AbstractEAgreementService
from ehealth.utils.callbacks import storage_callback, CallMetadata, CallType, ServiceType

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
        self.config_validator.setProperty("endpoint.agreement", "$uddi{uddi:ehealth-fgov-be:business:mycareneteagreement:v1}")
        if environment == "acc":
            self.config_validator.setProperty("endpoint.genericasync.eagreement.v1", "https://pilot.mycarenet.be:9443/mcn/bed/ehealth/GenAsync/eagreement")
        else:
            self.config_validator.setProperty("endpoint.genericasync.eagreement.v1", "https://services.ehealth.fgov.be/MyCareNet/eAgreement/v1")
            
    
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
        parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
        response_string = self.GATEWAY.jvm.java.lang.String(response.getBusinessResponse(), "UTF-8")
        try:
            return parser.parse(StringIO(response_string), target_class)  
        except:
            logger.error(response_string)
            raise

    def template_render(self, template: Any, patient: Patient, id_: str, io_routing: bool):
        logger.info("Inside custom askAgreement template render")
        bundle = bytes(template, encoding="utf-8")
        self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.dump(bundle)

        # TODO figure out how to remove this.  The bundle is already rendered at this point ...
        patientInfo = self.GATEWAY.jvm.be.ehealth.business.common.domain.Patient()
        if patient.ssin:
            patientInfo.setInss(patient.ssin)
        else:
            patientInfo.setRegNrWithMut(patient.insurancymembership)
            patientInfo.setMutuality(patient.insurancenumber)

        # input reference and Bundle ID must match
        inputReference = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.domain.InputReference(id_)

        builder_func = self.GATEWAY.getEncryptedRequestObjectBuilderImplWithRouting().buildAskAgreementRequest
        return builder_func(
            self.is_test,
            io_routing,
            inputReference, 
            patientInfo, 
            self.GATEWAY.jvm.org.joda.time.DateTime(), 
            bundle
            )
    
    def ask_agreement(
        self, 
        token: str,
        input_model: AskAgreementInputModel,
        callback_fn: Optional[Callable] = storage_callback
        ) -> str:
        timestamp = datetime.datetime.now()
        meta = CallMetadata(
            type=ServiceType.ASK_EAGREEMENT,
            timestamp=timestamp,
            call_type=CallType.UNENCRYPTED_REQUEST,
            ssin=input_model.patient.ssin,
            registrationNumber=input_model.patient.insurancenumber,
            mutuality=input_model.patient.insurancymembership,
        )

        practitioner = self.set_configuration_from_token(token)

        template, id_ = self.render_ask_or_extend_agreement_bundle(
            practitioner=practitioner,
            input_model=input_model
        )
        callback_fn(template, meta)
        
        request = self.template_render(
            template=template,
            patient=input_model.patient,
            id_=id_,
            io_routing=input_model.io_routing
            )
        
        raw_request = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(request)
        callback_fn(raw_request, meta.set_call_type(CallType.ENCRYPTED_REQUEST))

        try:
            serviceResponse = self.get_service().askAgreement(request.getRequest())
        except Exception as e:
            if "SEND_TO_IO_EXCEPTION" in str(e.java_exception):
                raise ServerSideException(str(e.java_exception))
            raise Exception(str(e.java_exception))
        raw_response = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(serviceResponse)
        callback_fn(raw_response, meta.set_call_type(CallType.ENCRYPTED_RESPONSE))

        response = self.get_response_builder().handleAskAgreementResponse(serviceResponse, request)
        self.verify_result(response)

        response_string = self.GATEWAY.jvm.java.lang.String(response.getBusinessResponse(), "UTF-8")
        callback_fn(response_string, meta.set_call_type(CallType.UNENCRYPTED_RESPONSE))

        response_pydantic = self.convert_response_to_pydantic(response, AskResponseBundle)
        return AskResponse(
            response=response_pydantic,
            transaction_request=template,
            transaction_response=response_string,
            soap_request=raw_request,
            soap_response=raw_response
        )

    def argue_agreement(
        self, 
        token: str,
        input_model: AskAgreementInputModel,
        callback_fn: Optional[Callable] = storage_callback
        ) -> str:
        timestamp = datetime.datetime.now()
        meta = CallMetadata(
            type=ServiceType.ARGUE_EAGREEMENT,
            timestamp=timestamp,
            call_type=CallType.UNENCRYPTED_REQUEST,
            ssin=input_model.patient.ssin,
            registrationNumber=input_model.patient.insurancenumber,
            mutuality=input_model.patient.insurancymembership,
        )
        practitioner = self.set_configuration_from_token(token)

        template, id_ = self.render_argue_agreement_bundle(
            practitioner=practitioner,
            input_model=input_model
        )
        callback_fn(template, meta)

        request = self.redundant_template_render(
            template=template,
            patient=input_model.patient,
            id_=id_,
            builder_func=self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreement.builders.RequestObjectBuilderFactory.getEncryptedRequestObjectBuilder().buildAskAgreementRequest
            )
        
        raw_request = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(request)
        callback_fn(raw_request, meta.set_call_type(CallType.ENCRYPTED_REQUEST))

        try:
            serviceResponse = self.get_service().askAgreement(request.getRequest())
        except Exception as e:
            if "SEND_TO_IO_EXCEPTION" in str(e.java_exception):
                raise ServerSideException(str(e.java_exception))
            raise e
        raw_response = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(serviceResponse)
        callback_fn(raw_response, meta.set_call_type(CallType.ENCRYPTED_RESPONSE))

        response = self.get_response_builder().handleAskAgreementResponse(serviceResponse, request)
        self.verify_result(response)

        response_string = self.GATEWAY.jvm.java.lang.String(response.getBusinessResponse(), "UTF-8")
        callback_fn(response_string, meta.set_call_type(CallType.UNENCRYPTED_RESPONSE))

        response_pydantic = self.convert_response_to_pydantic(response, AskResponseBundle)
        return AskResponse(
            response=response_pydantic,
            transaction_request=template,
            transaction_response=response_string,
            soap_request=raw_request,
            soap_response=raw_response
        )

    def cancel_agreement(
        self, 
        token: str,
        input_model: AskAgreementInputModel,
        callback_fn: Optional[Callable] = storage_callback
        ) -> str:
        timestamp = datetime.datetime.now()
        meta = CallMetadata(
            type=ServiceType.CONSULT_EAGREEMENT,
            timestamp=timestamp,
            call_type=CallType.UNENCRYPTED_REQUEST,
            ssin=input_model.patient.ssin,
            registrationNumber=input_model.patient.insurancenumber,
            mutuality=input_model.patient.insurancymembership,
        )
    
        practitioner = self.set_configuration_from_token(token)

        template, id_ = self.render_cancel_agreement_bundle(
            practitioner=practitioner,
            input_model=input_model
        )
        callback_fn(template, meta)

        request = self.redundant_template_render(
            template=template,
            patient=input_model.patient,
            id_=id_,
            builder_func=self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreement.builders.RequestObjectBuilderFactory.getEncryptedRequestObjectBuilder().buildAskAgreementRequest
            )
        
        raw_request = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(request)
        callback_fn(raw_request, meta.set_call_type(CallType.ENCRYPTED_REQUEST))

        logger.info(template)
        try:
            serviceResponse = self.get_service().askAgreement(request.getRequest())
        except Exception as e:
            if "SEND_TO_IO_EXCEPTION" in str(e.java_exception):
                raise ServerSideException(str(e.java_exception))
            raise e
        raw_response = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(serviceResponse)
        callback_fn(raw_response, meta.set_call_type(CallType.ENCRYPTED_RESPONSE))

        response = self.get_response_builder().handleAskAgreementResponse(serviceResponse, request)
        self.verify_result(response)

        response_string = self.GATEWAY.jvm.java.lang.String(response.getBusinessResponse(), "UTF-8")
        callback_fn(response_string, meta.set_call_type(CallType.UNENCRYPTED_RESPONSE))

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
        input_model: Patient,
        callback_fn: Optional[Callable] = storage_callback
        ) -> str:
        timestamp = datetime.datetime.now()
        meta = CallMetadata(
            type=ServiceType.CONSULT_EAGREEMENT,
            timestamp=timestamp,
            call_type=CallType.UNENCRYPTED_REQUEST,
            ssin=input_model.ssin,
            registrationNumber=input_model.insurancenumber,
            mutuality=input_model.insurancymembership,
        )

        practitioner = self.set_configuration_from_token(token)
        template, id_ = self.render_consult_agreement_bundle(
            practitioner=practitioner,
            input_model=input_model
        )
        callback_fn(template, meta)

        request = self.redundant_template_render(
            template=template,
            patient=input_model,
            id_=id_,
            builder_func=self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreement.builders.RequestObjectBuilderFactory.getEncryptedRequestObjectBuilder().buildConsultAgreementRequest
            )
        
        raw_request = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(request)
        callback_fn(raw_request, meta.set_call_type(CallType.ENCRYPTED_REQUEST))

        serviceResponse = self.get_service().consultAgreement(request.getRequest())
        raw_response = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(serviceResponse)
        callback_fn(raw_response, meta.set_call_type(CallType.ENCRYPTED_RESPONSE))

        response = self.get_response_builder().handleConsultAgreementResponse(serviceResponse, request)
        # self.verify_result(response)

        response_string = self.GATEWAY.jvm.java.lang.String(response.getBusinessResponse(), "UTF-8")
        callback_fn(response_string, meta.set_call_type(CallType.UNENCRYPTED_RESPONSE))

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
        callback_fn: Optional[Callable] = storage_callback
    ):
        timestamp = datetime.datetime.now()
        meta = CallMetadata(
            type=ServiceType.ASYNC_MESSAGES_EAGREEMENT,
            timestamp=timestamp,
            call_type=CallType.UNENCRYPTED_REQUEST
        )

        self.set_configuration_from_token(token)

        request = self.GATEWAY.jvm.be.ehealth.businessconnector.genericasync.domain.GetRequest.newBuilder().withDefaults().build()
        raw_request = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(request)
        callback_fn(raw_request, meta.set_call_type(CallType.ENCRYPTED_REQUEST))

        service = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreementasync.session.AgreementSessionServiceFactory.getAgrementService()
        serviceResponse = service.getEAgreementResponse(request)
        raw_response = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(serviceResponse)
        callback_fn(raw_response, meta.set_call_type(CallType.ENCRYPTED_RESPONSE))

        async_responses = []
        for i in range(serviceResponse.getMsgResponses().size()):
            processedMsgResponse = serviceResponse.getMsgResponses().get(i) # TODO what if multiple
            logger.info(processedMsgResponse.getMsgResponse().getDetail().getReference())
            response_string = self.GATEWAY.jvm.java.lang.String(processedMsgResponse.getBusinessResponse(), "UTF-8")

            # new timestamp for each message
            timestamp = datetime.datetime.now()
            meta = CallMetadata(
                type=ServiceType.ASYNC_MESSAGES_EAGREEMENT,
                timestamp=timestamp,
                call_type=CallType.UNENCRYPTED_RESPONSE
            )
            callback_fn(response_string, meta)

            response_pydantic = self.convert_response_to_pydantic(processedMsgResponse, AsyncBundle)
            async_response = AsyncResponse(
                response=response_pydantic,
                transaction_request="",
                transaction_response=response_string,
                soap_request=raw_request,
                soap_response=raw_response,
                reference=processedMsgResponse.getMsgResponse().getDetail().getReference(),
            )
            async_responses.append(async_response)
            
        return async_responses

    def confirm_message(
            self,
            token: str,
            reference: str,
    ):
        self.set_configuration_from_token(token)
        response = self.EHEALTH_JVM.confirmEAgreementMessage(reference)
        logger.info(response)