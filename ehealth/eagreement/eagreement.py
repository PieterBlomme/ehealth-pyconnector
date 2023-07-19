from py4j.java_gateway import JavaGateway
import logging
import datetime
import tempfile
import uuid
import pytz
from typing import List, Optional, Tuple
from pydantic import BaseModel, root_validator
from io import StringIO
from ..sts.assertion import Assertion
from xsdata.models.datatype import XmlDateTime, XmlDate
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
    QuantityQuantity, AuthoredOn
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
        return nihii, givenname, surname
    
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

    @classmethod
    def _render_message_header(cls,
                               practitioner_role_urn: str,
                               ):
        message_header_uuid = str(uuid.uuid4())
        message_header = Entry(
                    full_url=FullUrl(f"urn:uuid:{message_header_uuid}"),
                    resource=Resource(
                        message_header=MessageHeader(
                            id=Id(message_header_uuid),
                            meta=MetaType(Profile("https://www.ehealth.fgov.be/standards/fhir/mycarenet/StructureDefinition/be-messageheader")),
                            event_coding=EventCoding(
                                system=System("https://www.ehealth.fgov.be/standards/fhir/mycarenet/CodeSystem/message-events"),
                                code=Code("claim-ask")
                            ),
                            destination=Destination(
                                name=Name(value="MyCareNet"),
                                endpoint=Endpoint("MyCareNet")
                                ),
                            source=Source(Endpoint(practitioner_role_urn)),
                            sender=Sender(Reference("PractitionerRole/PractitionerRole1")),
                            focus=Focus(Reference("Claim/Claim1")),            
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
        nihii: str,
        givenname: str,
        surname: str,
        practitioner: Optional[str] = "Practitioner1",
                            ):
        entry_uuid = str(uuid.uuid4())
        return Entry(
                    full_url=FullUrl(f"urn:uuid:{entry_uuid}"),
                    resource=Resource(
                        practitioner=Practitioner1(
                            id=Id(practitioner),
                            meta=MetaType(Profile("https://www.ehealth.fgov.be/standards/fhir/core/StructureDefinition/be-practitioner")),
                            identifier=Identifier(
                                system=System("https://www.ehealth.fgov.be/standards/fhir/core/NamingSystem/nihdi"),
                                value=Value(nihii)
                            ),
                            name=Name(
                                family=Family(surname),
                                given=Given(givenname)
                            )
                        ),
                    )
                )
    
    @classmethod
    def _render_patient(cls,
                        ssin: str, givenname: str, surname: str):
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
                                value=Value(ssin)
                            ),
                            name=Name(
                                family=Family(surname),
                                given=Given(givenname)
                            ),
                            gender=Gender("male")
                        ),
                    )
                )
    
    @classmethod
    def render_service_request_1(cls):
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
                                    content_type=ContentType("application/pdf"),
                                    data=Data("QW5uZXhlIGlubGluZSwgYmFzZTY0ZWQ=")
                                )
                            ),
                            status=Status("active"),
                            intent=Intent("order"),
                            category=Category(
                                coding=Coding(
                                    system=System("http://snomed.info/sct"),
                                    code=Code("91251008"),
                                )
                            ),
                            code=NestedCode(
                                coding=Coding(
                                    system=System("http://snomed.info/sct"),
                                    code=Code("91251008"),
                                )
                            ),
                            quantity_quantity=QuantityQuantity(Value(15)),
                            authored_on=AuthoredOn(XmlDate.from_date(datetime.date.today() - datetime.timedelta(days=145))),
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
                      ):
        entry_uuid = str(uuid.uuid4())
        return Entry(
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
                                    code=Code("physiotherapy-fb"),
                                )
                            ),
                            use=Use("preauthorization"),
                            patient=Patient2(Reference("Patient/Patient1")),
                            billable_period=BillablePeriod(
                                Start(
                                    value=XmlDate.from_date(datetime.date.today() - datetime.timedelta(days=145))
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
                            referral=Referral(Reference("ServiceRequest/ServiceRequest1")),
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
                                        code=Code("fb-51")
                                    ),
                                ),
                                serviced_date=ServicedDate(XmlDate.from_date(datetime.date.today() - datetime.timedelta(days=156)))
                            )

                        ),
                    )
                )
    
    def render_bundle(
        self,
        nihii: str,
        givenname: str,
        surname: str
        ):
        id_ = str(uuid.uuid4())
        now = datetime.datetime.now(pytz.timezone("Europe/Brussels"))
        practitioner_physio = self._render_practitioner(
            nihii=nihii,
            givenname=givenname,
            surname=surname,
            practitioner="Practitioner1"
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
            ssin="90060421941",
            givenname="Pieter",
            surname="Blomme"
        )
        practitioner_physician = self._render_practitioner(
            nihii="00092210605",
            givenname="Pieter",
            surname="Blomme",
            practitioner="Practitioner2"
        )
        practitioner_role_physician = self._render_practitioner_role(
            practitioner_role="PractitionerRole2",
            practitioner=f"Practitioner/Practitioner2",
            code="persphysician"
        )
        annex = self.render_service_request_1()
        prescription = self.render_service_request_2()
        claim = self._render_claim(
            now=now,
            )
        
        bundle = Bundle(
            id=Id(id_),
            meta=MetaType(Profile("https://www.ehealth.fgov.be/standards/fhir/mycarenet/StructureDefinition/be-eagreementdemand")),
            timestamp=Timestamp(now.isoformat(timespec="seconds")),
            type=TypeType(value="message"),
            entry=[
                message_header,
                # organization,
                practitioner_role_physio,
                practitioner_physio,
                patient,
                practitioner_role_physician,
                practitioner_physician,
                annex,
                prescription,
                claim
            ]
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
        # bundleLocation: str,
        patientNiss: str = "90060421941"
        ) -> str:
        nihii, givenname, surname = self.set_configuration_from_token(token)

        template, id_ = self.render_bundle(
            nihii=nihii,
            givenname=givenname,
            surname=surname
        )
        logger.info(template)

        responseBuilder = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreement.builders.ResponseObjectBuilderFactory.getResponseObjectBuilder()
        
        bundle = bytes(template, encoding="utf-8")
        # with open("/mnt/c/Users/piete/Documents/ehealth-pyconnector/tests/data/Bundle-ex01.xml", "rb") as f:
        #     bundle = f.read()

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
    

    def consult_agreement(
        self, 
        token: str,
        # bundleLocation: str,
        patientNiss: str = "90060421941"
        ) -> str:
        id_ = "ex12"
        nihii = self.set_configuration_from_token(token)

        responseBuilder = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreement.builders.ResponseObjectBuilderFactory.getResponseObjectBuilder()
        
        # bundle = bytes(template, encoding="utf-8")
        with open("/mnt/c/Users/piete/Documents/ehealth-pyconnector/tests/data/Bundle-ex12.xml", "rb") as f:
            bundle = f.read()

        self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.dump(bundle)

        patientInfo = self.GATEWAY.jvm.be.ehealth.business.common.domain.Patient()
        patientInfo.setInss(patientNiss)

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
        response = responseBuilder.handleConsultAgreementResponse(serviceResponse, consultRequest)
        signVerifResult = response.getSignatureVerificationResult()
        for entry in signVerifResult.getErrors():
            self.GATEWAY.jvm.org.junit.Assert.assertTrue("Errors found in the signature verification",
                  entry.getValue().isValid())
        logger.info(self.GATEWAY.jvm.java.lang.String(response.getBusinessResponse(), "UTF-8"))
        return ""