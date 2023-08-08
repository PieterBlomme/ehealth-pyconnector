import logging
import datetime
import uuid
import pytz
from io import StringIO
from typing import Any, Callable
from xsdata_pydantic.bindings import XmlSerializer, XmlParser
from .bundle import (
    Bundle, MetaType, Profile, Timestamp,
    Id, TypeType
)
from pydantic import BaseModel
from .input_models import Patient, Practitioner, AskAgreementInputModel
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
    
    @classmethod
    def serialize_template(cls, bundle: BaseModel):
        serializer = XmlSerializer()
        serializer.config.pretty_print = True
        # serializer.config.xml_declaration = True
        ns_map = {
            "": "http://hl7.org/fhir"
        }
        return serializer.render(bundle, ns_map)
    
    def render_ask_or_extend_agreement_bundle(
        self,
        practitioner: Practitioner,
        input_model: AskAgreementInputModel,
        ):
        id_ = str(uuid.uuid4())
        now = datetime.datetime.now(pytz.timezone("Europe/Brussels"))
        practitioner_physio = self._render_practitioner(
            practitioner=practitioner,
            practitioner_identifier="Practitioner1"
        )
        practitioner_role_physio = self._render_practitioner_role(
            practitioner_role="PractitionerRole1",
            practitioner=f"Practitioner/Practitioner1",
            code="persphysiotherapist"
        )
        # organization = self._render_organization()
        message_header = self._render_message_header(
            practitioner_role_urn=practitioner_role_physio.full_url.value,
            claim=input_model.claim.transaction
            )

        patient = self._render_patient(
            patient=input_model.patient
        )
        practitioner_physician = self._render_practitioner(
            practitioner=input_model.physician,
            practitioner_identifier="Practitioner2"
        )
        practitioner_role_physician = self._render_practitioner_role(
            practitioner_role="PractitionerRole2",
            practitioner=f"Practitioner/Practitioner2",
            code="persphysician"
        )
        entries = [
               message_header,
                # organization,
                practitioner_role_physio,
                practitioner_physio,
                patient,
                practitioner_role_physician,
                practitioner_physician,
        ]
        if input_model.claim.prescription:
            annex = self._render_service_request_1(input_model.claim.prescription)
            entries.append(annex)
            service_request = f"ServiceRequest/{annex.resource.service_request.id.value}"
            # prescription = self.render_service_request_2()
            # entries.append(prescription)
        else:
            service_request = None
        claim = self._render_claim(
            now=now,
            claim_ask=input_model.claim,
            service_request=service_request
            )
        entries.append(claim)
        
        bundle = Bundle(
            id=Id(id_),
            meta=MetaType(Profile("https://www.ehealth.fgov.be/standards/fhir/mycarenet/StructureDefinition/be-eagreementdemand")),
            timestamp=Timestamp(now.isoformat(timespec="seconds")),
            type=TypeType(value="message"),
            entry=entries
        )
        template = self.serialize_template(bundle)
        request = self.redundant_template_render(
            template=template,
            patient_ssin=input_model.patient.ssin,
            id_=id_,
            builder_func=self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreement.builders.RequestObjectBuilderFactory.getEncryptedRequestObjectBuilder().buildAskAgreementRequest
            )
        return request, template
    
    def render_consult_agreement_bundle(
        self,
        practitioner: Practitioner,
        input_model: Patient
        ):
        id_ = str(uuid.uuid4())
        now = datetime.datetime.now(pytz.timezone("Europe/Brussels"))
        practitioner_physio = self._render_practitioner(
            practitioner=practitioner,
            practitioner_identifier="Practitioner1"
        )
        practitioner_role_physio = self._render_practitioner_role(
            practitioner_role="PractitionerRole1",
            practitioner=f"Practitioner/Practitioner1",
            code="persphysiotherapist"
        )
        message_header = self._render_message_header(
            practitioner_role_urn=practitioner_role_physio.full_url.value,
            claim=None
            )

        parameters = self._render_parameters()
        patient = self._render_patient(
            patient=input_model
        )
        entries = [
                message_header,
                parameters,
                practitioner_role_physio,
                practitioner_physio,
                patient,
        ]
        
        bundle = Bundle(
            id=Id(id_),
            meta=MetaType(Profile("https://www.ehealth.fgov.be/standards/fhir/mycarenet/StructureDefinition/be-eagreementconsult")),
            timestamp=Timestamp(now.isoformat(timespec="seconds")),
            type=TypeType(value="message"),
            entry=entries
        )
        
        template = self.serialize_template(bundle)
        request = self.redundant_template_render(
            template=template,
            patient_ssin=input_model.ssin,
            id_=id_,
            builder_func=self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreement.builders.RequestObjectBuilderFactory.getEncryptedRequestObjectBuilder().buildConsultAgreementRequest
            )
        return request, template
    
    def verify_result(self, response: Any):
        signVerifResult = response.getSignatureVerificationResult()
        for entry in signVerifResult.getErrors():
            self.GATEWAY.jvm.org.junit.Assert.assertTrue("Errors found in the signature verification",
                  entry.getValue().isValid())
    
    def redundant_template_render(self, template: Any, patient_ssin: str, id_: str, builder_func: Callable):
        bundle = bytes(template, encoding="utf-8")
        self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.dump(bundle)

        # TODO figure out how to remove this.  The bundle is already rendered at this point ...
        patientInfo = self.GATEWAY.jvm.be.ehealth.business.common.domain.Patient()
        patientInfo.setInss(patient_ssin)

        # input reference and Bundle ID must match
        inputReference = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.domain.InputReference(id_)
        return builder_func(
            self.is_test, 
            inputReference, 
            patientInfo, 
            self.GATEWAY.jvm.org.joda.time.DateTime(), 
            bundle
            )

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

        request, template = self.render_ask_or_extend_agreement_bundle(
            practitioner=practitioner,
            input_model=input_model
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