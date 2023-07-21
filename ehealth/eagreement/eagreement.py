from py4j.java_gateway import JavaGateway
import logging
import datetime
import tempfile
import uuid
import pytz
from typing import List, Optional
from io import StringIO
from ..sts.assertion import Assertion
from xsdata.models.datatype import XmlDate
from xsdata_pydantic.bindings import XmlSerializer, XmlParser
from .bundle import (
    Bundle, Entry, FullUrl, Resource, MessageHeader, MetaType, Profile, Timestamp,
    EventCoding, Destination, Sender, Source, Focus, System, Code, Endpoint,
    Reference, Organization, Id, Identifier, TypeType, Value, Coding,
    Practitioner2, PractitionerRole, Display, Practitioner1, Name,
    Family, Given, NestedCode, Patient1, Gender, ServiceRequest,
    Contained, Binary, ContentType, Data, Status, Intent,
    Subject, Requester, SupportingInfo, Claim, SubType, Use,
    BillablePeriod, Patient2, Start, Created, Enterer,
    Provider,Priority, Referral, Sequence, Category,
    Insurance, Item, Coverage, Focal, ProductOrService, ServicedDate,
    QuantityQuantity, AuthoredOn, Parameter, Parameters, ValueCode,
    ValueCoding, ValueString, ValueReference
)
from .input_models import Patient, Practitioner, AskAgreementInputModel, ClaimAsk, Prescription
from .ask_agreement import Bundle as AskResponseBundle, Response as AskResponse
from .consult_agreement import Bundle as ConsultresposneBundle, Response as ConsultResponse

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
        return nihii, givenname, surname

    @classmethod
    def _render_message_header(cls,
                               practitioner_role_urn: str,
                               claim: Optional[str] = "claim-ask"
                               ):
        message_header_uuid = str(uuid.uuid4())

        if claim:
            event_coding = event_coding=EventCoding(
                                system=System("https://www.ehealth.fgov.be/standards/fhir/mycarenet/CodeSystem/message-events"),
                                code=Code(claim)
                            )
            focus=Focus(Reference("Claim/Claim1"))
        else:
            event_coding = event_coding=EventCoding(
                                system=System("http://hl7.org/fhir/restful-interaction"),
                                code=Code("search-type")
                            )
            focus=Focus(Reference("Parameters/Parameters1"))

        message_header = Entry(
                    full_url=FullUrl(f"urn:uuid:{message_header_uuid}"),
                    resource=Resource(
                        message_header=MessageHeader(
                            id=Id(message_header_uuid),
                            meta=MetaType(Profile("https://www.ehealth.fgov.be/standards/fhir/mycarenet/StructureDefinition/be-messageheader")),
                            event_coding=event_coding,
                            destination=Destination(
                                name=Name(value="MyCareNet"),
                                endpoint=Endpoint("MyCareNet")
                                ),
                            source=Source(Endpoint(practitioner_role_urn)),
                            sender=Sender(Reference("PractitionerRole/PractitionerRole1")),
                            focus=focus,            
                        )
                    )
                )
        return message_header
    
    @classmethod
    def _render_organization(cls,
                             entry_uuid: Optional[str] = None):
        if not entry_uuid:
            entry_uuid = str(uuid.uuid4())
        return Entry(
                    full_url=FullUrl(f"urn:uuid:{entry_uuid}"),
                    resource=Resource(
                        organization=Organization(
                            id=Id("Organization1"),
                            meta=MetaType(Profile("https://www.ehealth.fgov.be/standards/fhir/core/StructureDefinition/be-organization")),
                            identifier=Identifier(
                                system=System("https://www.ehealth.fgov.be/standards/fhir/core/NamingSystem/nihdi"),
                                value=Value("71000436000")
                            ),
                            type=TypeType(
                                EventCoding(
                                    system=System("https://www.ehealth.fgov.be/standards/fhir/core/CodeSystem/cd-hcparty"),
                                    code=Code(value="orghospital")
                                )
                            )
                        )
                    )
                )

    @classmethod
    def _render_practitioner_role(cls,
                                practitioner_role: Optional[str] = "PractitionerRole1",
                                practitioner: Optional[str] = "Practitioner/Practitioner1",
                                code: Optional[str] = "persphysiotherapist"
                                ):
        entry_uuid = str(uuid.uuid4())
        return Entry(
                    full_url=FullUrl(f"urn:uuid:{entry_uuid}"),
                    resource=Resource(
                        practitioner_role=PractitionerRole(
                            id=Id(practitioner_role),
                            meta=MetaType(Profile("https://www.ehealth.fgov.be/standards/fhir/core/StructureDefinition/be-practitionerrole")),
                            practitioner=Practitioner2(
                                Reference(practitioner)
                            ),
                            code=NestedCode(
                                coding=Coding(
                                    system=System("https://www.ehealth.fgov.be/standards/fhir/core/CodeSystem/cd-hcparty"),
                                    code=Code(code),
                                )
                            )
                        ),
                    )
                )
    
    @classmethod
    def _render_practitioner(cls,
        practitioner: Practitioner,
        practitioner_identifier: Optional[str] = "Practitioner1",
                            ):
        entry_uuid = str(uuid.uuid4())
        return Entry(
                    full_url=FullUrl(f"urn:uuid:{entry_uuid}"),
                    resource=Resource(
                        practitioner=Practitioner1(
                            id=Id(practitioner_identifier),
                            meta=MetaType(Profile("https://www.ehealth.fgov.be/standards/fhir/core/StructureDefinition/be-practitioner")),
                            identifier=Identifier(
                                system=System("https://www.ehealth.fgov.be/standards/fhir/core/NamingSystem/nihdi"),
                                value=Value(practitioner.nihii)
                            ),
                            name=Name(
                                family=Family(practitioner.surname),
                                given=Given(practitioner.givenname)
                            )
                        ),
                    )
                )
    
    @classmethod
    def _render_patient(cls,
                        patient: Patient):
        entry_uuid = str(uuid.uuid4())
        return Entry(
                    full_url=FullUrl(f"urn:uuid:{entry_uuid}"),
                    resource=Resource(
                        patient=Patient1(
                            id=Id("Patient1"),
                            meta=MetaType(Profile("https://www.ehealth.fgov.be/standards/fhir/core/StructureDefinition/be-patient")),
                            practitioner=Practitioner2(
                                Reference("Practitioner/Practitioner1")
                            ),
                            identifier=Identifier(
                                system=System("https://www.ehealth.fgov.be/standards/fhir/core/NamingSystem/ssin"),
                                value=Value(patient.ssin)
                            ),
                            name=Name(
                                family=Family(patient.surname),
                                given=Given(patient.givenname)
                            ),
                            gender=Gender(patient.gender)
                        ),
                    )
                )
    
    @classmethod
    def _render_service_request_1(cls, prescription: Prescription):
        entry_uuid = str(uuid.uuid4())        
        return Entry(
                    full_url=FullUrl(f"urn:uuid:{entry_uuid}"),
                    resource=Resource(
                        service_request=ServiceRequest(
                            id=Id("ServiceRequest1"),
                            meta=MetaType(Profile("https://www.ehealth.fgov.be/standards/fhir/mycarenet/StructureDefinition/be-eagreementservicerequest")),
                            contained=Contained(
                                binary=Binary(
                                    id=Id("annexSR1"),
                                    content_type=ContentType(prescription.data_mimetype),
                                    data=Data(prescription.data_base64) # "QW5uZXhlIGlubGluZSwgYmFzZTY0ZWQ="
                                )
                            ),
                            status=Status("active"),
                            intent=Intent("order"),
                            category=Category(
                                coding=Coding(
                                    system=System("http://snomed.info/sct"),
                                    code=Code(prescription.snomed_category), # "91251008"
                                )
                            ),
                            code=NestedCode(
                                coding=Coding(
                                    system=System("http://snomed.info/sct"),
                                    code=Code(prescription.snomed_code), # "91251008"
                                )
                            ),
                            quantity_quantity=QuantityQuantity(Value(prescription.quantity)), # 15
                            authored_on=AuthoredOn(XmlDate.from_date(prescription.date)), # datetime.date.today() - datetime.timedelta(days=145)
                            subject=Subject(
                                reference=Reference("Patient/Patient1")
                            ),
                            requester=Requester(Reference("PractitionerRole/PractitionerRole2")),
                            supporting_info=SupportingInfo(reference=Reference("#annexSR1"))
                        ),
                    )
                )

    @classmethod
    def render_service_request_2(cls):
        entry_uuid = str(uuid.uuid4())
        return Entry(
                    full_url=FullUrl(f"urn:uuid:{entry_uuid}"),
                    resource=Resource(
                        service_request=ServiceRequest(
                            id=Id("ServiceRequest2"),
                            meta=MetaType(Profile("https://www.ehealth.fgov.be/standards/fhir/mycarenet/StructureDefinition/be-eagreementservicerequest")),
                            identifier=Identifier(
                                system=System("https://www.ehealth.fgov.be/standards/fhir/core/NamingSystem/uhmep"),
                                value=Value("71000436000")
                            ),
                            status=Status("active"),
                            intent=Intent("order"),
                            subject=Subject(
                                reference=Reference("Patient/Patient1")
                            ),
                            requester=Requester(Reference("PractitionerRole/PractitionerRole2")),
                        ),
                    )
                )
    
    @classmethod
    def _render_claim(cls,
                      now: datetime.datetime,
                      claim_ask: ClaimAsk,
                      service_request: Optional[str] = None
                      ):
        entry_uuid = str(uuid.uuid4())
        entry = Entry(
                    full_url=FullUrl(f"urn:uuid:{entry_uuid}"),
                    resource=Resource(
                        claim=Claim(
                            id=Id("Claim1"),
                            meta=MetaType(Profile("https://www.ehealth.fgov.be/standards/fhir/mycarenet/StructureDefinition/be-eagreementclaim-kine")),
                            status=Status("active"),
                            type=TypeType(
                                coding=EventCoding(
                                    system=System("http://terminology.hl7.org/CodeSystem/claim-type"),
                                    code=Code("professional"),
                                )
                            ),
                            sub_type=SubType(
                                coding=Coding(
                                    system=System("https://www.ehealth.fgov.be/standards/fhir/mycarenet/CodeSystem/agreement-types"),
                                    code=Code(claim_ask.sub_type),
                                )
                            ),
                            use=Use("preauthorization"),
                            patient=Patient2(Reference("Patient/Patient1")),
                            billable_period=BillablePeriod(
                                Start(
                                    value=XmlDate.from_date(claim_ask.billable_period)
                                    )
                            ),
                            created=Created(now.isoformat(timespec="seconds")),
                            enterer=Enterer(Reference("PractitionerRole/PractitionerRole1")),
                            provider=Provider(Reference("PractitionerRole/PractitionerRole1")),
                            priority=Priority(
                                    coding=Coding(
                                        system=System("http://terminology.hl7.org/CodeSystem/processpriority"),
                                        code=Code("stat")
                                    ),
                            ),
                            supporting_info=[
                            ],
                            insurance=Insurance(
                                sequence=Sequence(1),
                                focal=Focal(True),
                                coverage=Coverage(Display("use of mandatory insurance coverage, no further details provided here."))
                            ),
                            item=Item(
                                sequence=Sequence(1),
                                product_or_service=ProductOrService(
                                    coding=Coding(
                                        system=System("https://www.ehealth.fgov.be/standards/fhir/mycarenet/CodeSystem/nihdi-physiotherapy-pathologysituationcode"),
                                        code=Code(claim_ask.product_or_service)
                                    ),
                                ),
                                serviced_date=ServicedDate(XmlDate.from_date(claim_ask.serviced_date))
                            )

                        ),
                    )
                )
        if service_request:
            entry.resource.claim.referral = Referral(Reference(service_request))
        return entry

    @classmethod
    def _render_parameters(cls):
        entry_uuid = str(uuid.uuid4())
        return Entry(
                    full_url=FullUrl(f"urn:uuid:{entry_uuid}"),
                    resource=Resource(
                        parameters=Parameters(
                            id=Id("Parameters1"),
                            parameter=[
                                Parameter(
                                    name=Name(value="resourceType"),
                                    value_string=ValueString(value="ClaimResponse")
                                ),
                                Parameter(
                                    name=Name(value="patient"),
                                    value_reference=ValueReference(Reference(value="Patient/Patient1"))
                                ),
                                Parameter(
                                    name=Name(value="use"),
                                    value_code=ValueCode(value="preauthorization")
                                ),
                                Parameter(
                                    name=Name(value="subType"),
                                    value_coding=ValueCoding(
                                        system=System(value="https://www.ehealth.fgov.be/standards/fhir/mycarenet/CodeSystem/agreement-types"),
                                        code=Code(value="physiotherapy")
                                    )
                                ),
                            ]
                        ),
                    )
                )
    
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

    def render_ask_agreement_bundle(
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
            practitioner_role_urn=practitioner_role_physio.full_url.value
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
        
        serializer = XmlSerializer()
        serializer.config.pretty_print = True
        # serializer.config.xml_declaration = True
        ns_map = {
            "": "http://hl7.org/fhir"
        }
        return serializer.render(bundle, ns_map), id_

    def render_consult_agreement_bundle(
        self,
        practitioner: Practitioner,
        patient: Patient
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
            patient=patient
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
        
        serializer = XmlSerializer()
        serializer.config.pretty_print = True
        # serializer.config.xml_declaration = True
        ns_map = {
            "": "http://hl7.org/fhir"
        }
        return serializer.render(bundle, ns_map), id_
    
    def ask_agreement(
        self, 
        token: str,
        input_model: AskAgreementInputModel
        ) -> str:
        nihii, givenname, surname = self.set_configuration_from_token(token)

        template, id_ = self.render_ask_agreement_bundle(
            Practitioner(
                nihii=nihii,
                givenname=givenname,
                surname=surname,
            ),
            input_model=input_model
        )

        responseBuilder = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreement.builders.ResponseObjectBuilderFactory.getResponseObjectBuilder()
        
        bundle = bytes(template, encoding="utf-8")

        self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.dump(bundle)
        # TODO figure out how to remove this.  The bundle is already rendered at this point ...
        patientInfo = self.GATEWAY.jvm.be.ehealth.business.common.domain.Patient()
        patientInfo.setInss(input_model.patient.ssin)

        # input reference and Bundle ID must match
        inputReference = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.domain.InputReference(id_)
        askRequest = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreement.builders.RequestObjectBuilderFactory.getEncryptedRequestObjectBuilder().buildAskAgreementRequest(
            self.is_test, 
            inputReference, 
            patientInfo, 
            self.GATEWAY.jvm.org.joda.time.DateTime(), 
            bundle
            )
        raw_request = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(askRequest)

        service = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreement.session.AgreementSessionServiceFactory.getAgreementService()
        serviceResponse = service.askAgreement(askRequest.getRequest())
        raw_response = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(serviceResponse)

        response = responseBuilder.handleAskAgreementResponse(serviceResponse, askRequest)
        signVerifResult = response.getSignatureVerificationResult()
        for entry in signVerifResult.getErrors():
            self.GATEWAY.jvm.org.junit.Assert.assertTrue("Errors found in the signature verification",
                  entry.getValue().isValid())

        parser = XmlParser()
        response_string = self.GATEWAY.jvm.java.lang.String(response.getBusinessResponse(), "UTF-8")
        try:
            response_pydantic = parser.parse(StringIO(response_string), AskResponseBundle)
            return AskResponse(
                response=response_pydantic,
                transaction_request=template,
                transaction_response=response_string,
                soap_request=raw_request,
                soap_response=raw_response
            )
        except:
            logger.error(response_string)
            raise
    

    def consult_agreement(
        self, 
        token: str,
        input_model: Patient
        ) -> str:
        nihii, givenname, surname = self.set_configuration_from_token(token)
        template, id_ = self.render_consult_agreement_bundle(
            Practitioner(
                nihii=nihii,
                givenname=givenname,
                surname=surname,
            ),
            patient=input_model
        )

        responseBuilder = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreement.builders.ResponseObjectBuilderFactory.getResponseObjectBuilder()
        
        bundle = bytes(template, encoding="utf-8")

        self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.dump(bundle)

        patientInfo = self.GATEWAY.jvm.be.ehealth.business.common.domain.Patient()
        patientInfo.setInss(input_model.ssin)

        # input reference and AttributeQuery ID must match
        inputReference = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.domain.InputReference(id_)
        consultRequest = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreement.builders.RequestObjectBuilderFactory.getEncryptedRequestObjectBuilder().buildConsultAgreementRequest(
            self.is_test, 
            inputReference, 
            patientInfo, 
            self.GATEWAY.jvm.org.joda.time.DateTime(), 
            bundle
            )
        raw_request = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(consultRequest)
        # logger.info(raw_request)

        service = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreement.session.AgreementSessionServiceFactory.getAgreementService()
        serviceResponse = service.consultAgreement(consultRequest.getRequest())
        raw_response = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(serviceResponse)

        response = responseBuilder.handleConsultAgreementResponse(serviceResponse, consultRequest)
        signVerifResult = response.getSignatureVerificationResult()
        for entry in signVerifResult.getErrors():
            self.GATEWAY.jvm.org.junit.Assert.assertTrue("Errors found in the signature verification",
                  entry.getValue().isValid())


        parser = XmlParser()
        response_string = self.GATEWAY.jvm.java.lang.String(response.getBusinessResponse(), "UTF-8")
        try:
            response_pydantic = parser.parse(StringIO(response_string), ConsultresposneBundle)
            return ConsultResponse(
                response=response_pydantic,
                transaction_request=template,
                transaction_response=response_string,
                soap_request=raw_request,
                soap_response=raw_response
            )
        except:
            logger.error(response_string)
            raise