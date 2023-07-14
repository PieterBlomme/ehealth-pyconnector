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
    Insurance, Item, Coverage, Focal, ProductOrService, ServicedDate
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
        now = datetime.datetime.now(pytz.timezone("Europe/Brussels"))
        logger.info(now.isoformat())

        message_header_uuid = str(uuid.uuid4())
        message_header = Entry(
                    full_url=FullUrl(f"urn:uuid:{message_header_uuid}"),
                    resource=Resource(
                        message_header=MessageHeader(
                            id=Id(message_header_uuid),
                            meta=MetaType(Profile("https://www.ehealth.fgov.be/standards/fhir/mycarenet/StructureDefinition/be-messageheader")),
                            event_coding=EventCoding(
                                system=System("http://www.mycarenet.be/fhir/CodeSystem/message-events"),
                                code=Code("claim-ask")
                            ),
                            source=Source(Endpoint("urn:uuid:e2c6f73a-74d8-40f2-af0b-a61ad20c53d4")),
                            sender=Sender(Reference("Organization/Organization1")),
                            focus=Focus(Reference("Claim/Claim1")),            
                        )
                    )
                )
        
        organization = Entry(
                    full_url=FullUrl("urn:uuid:e2c6f73a-74d8-40f2-af0b-a61ad20c53d4"),
                    resource=Resource(
                        organization=Organization(
                            id=Id("organization1"),
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
        
        practitioner_role_physio = Entry(
                    full_url=FullUrl("urn:uuid:PractitionerRole1"),
                    resource=Resource(
                        practitioner_role=PractitionerRole(
                            id=Id("PractitionerRole1"),
                            meta=MetaType(Profile("https://www.ehealth.fgov.be/standards/fhir/mycarenet/StructureDefinition/be-practitionerrole")),
                            practitioner=Practitioner2(
                                Reference("Practitioner/Practitioner1")
                            ),
                            code=NestedCode(
                                coding=Coding(
                                    system=System("https://www.ehealth.fgov.be/standards/fhir/core/CodeSystem/cd-hcparty"),
                                    code=Code("persphysiotherapist"),
                                    display=Display("physiotherapist")
                                )
                            )
                        ),
                    )
                )

        practitioner_physio = Entry(
                    full_url=FullUrl("urn:uuid:Practitioner1"),
                    resource=Resource(
                        practitioner=Practitioner1(
                            id=Id("Practitioner1"),
                            meta=MetaType(Profile("https://www.ehealth.fgov.be/standards/fhir/mycarenet/StructureDefinition/be-practitioner")),
                            practitioner=Practitioner2(
                                Reference("Practitioner/Practitioner1")
                            ),
                            identifier=Identifier(
                                system=System("https://www.ehealth.fgov.be/standards/fhir/core/NamingSystem/nihdi"),
                                value=Value("54263481527")
                            ),
                            name=Name(
                                family=Family("Smith"),
                                given=Given("Jeff")
                            )
                        ),
                    )
                )

        patient = Entry(
                    full_url=FullUrl("urn:uuid:Patient1"),
                    resource=Resource(
                        patient=Patient1(
                            id=Id("Patient1"),
                            meta=MetaType(Profile("https://www.ehealth.fgov.be/standards/fhir/mycarenet/StructureDefinition/be-patient")),
                            practitioner=Practitioner2(
                                Reference("Practitioner/Practitioner1")
                            ),
                            identifier=Identifier(
                                system=System("https://www.ehealth.fgov.be/standards/fhir/NamingSystem/ssin"),
                                value=Value("73031805784")
                            ),
                            name=Name(
                                family=Family("Dupont"),
                                given=Given("Jean")
                            ),
                            gender=Gender("male")
                        ),
                    )
                )
        
        practitioner_role_physician = Entry(
                    full_url=FullUrl("urn:uuid:PractitionerRole2"),
                    resource=Resource(
                        practitioner_role=PractitionerRole(
                            id=Id("PractitionerRole2"),
                            meta=MetaType(Profile("https://www.ehealth.fgov.be/standards/fhir/mycarenet/StructureDefinition/be-practitionerrole")),
                            practitioner=Practitioner2(
                                Reference("Practitioner/PractitionerRole2")
                            ),
                            code=NestedCode(
                                coding=Coding(
                                    system=System("https://www.ehealth.fgov.be/standards/fhir/core/CodeSystem/cd-hcparty"),
                                    code=Code("persphysician"),
                                    display=Display("physician")
                                )
                            )
                        ),
                    )
                )

        practitioner_physician = Entry(
                    full_url=FullUrl("urn:uuid:Practitioner2"),
                    resource=Resource(
                        practitioner=Practitioner1(
                            id=Id("Practitioner2"),
                            meta=MetaType(Profile("https://www.ehealth.fgov.be/standards/fhir/mycarenet/StructureDefinition/be-practitioner")),
                            practitioner=Practitioner2(
                                Reference("Practitioner/Practitioner2")
                            ),
                            identifier=Identifier(
                                system=System("https://www.ehealth.fgov.be/standards/fhir/core/NamingSystem/nihdi"),
                                value=Value("19234011004")
                            ),
                            name=Name(
                                family=Family("Name"),
                                given=Given("First name")
                            )
                        ),
                    )
                )

        annex = Entry(
                    full_url=FullUrl("urn:uuid:ServiceRequest1"),
                    resource=Resource(
                        service_request=ServiceRequest(
                            id=Id("ServiceRequest1"),
                            contained=Contained(
                                binary=Binary(
                                    id=Id("annexSR1"),
                                    content_type=ContentType("application/pdf"),
                                    data=Data("QW5uZXhlIGlubGluZSwgYmFzZTY0ZWQ=")
                                )
                            ),
                            identifier=Identifier(
                                system=System("https://www.ehealth.fgov.be/standards/fhir/NamingSystem/uhmep"),
                                value=Value("n° de la prescription")
                            ),
                            status=Status("active"),
                            intent=Intent("order"),
                            subject=Subject(
                                reference=Reference("Patient/Patient1")
                            ),
                            requester=Requester(Reference("PractitionerRole/PractitionerRole2")),
                            supporting_info=SupportingInfo(reference=Reference("#annexSR1"))
                        ),
                    )
                )

        claim = Entry(
                    full_url=FullUrl("urn:uuid:Claim1"),
                    resource=Resource(
                        claim=Claim(
                            id=Id("Claim1"),
                            meta=MetaType(Profile("https://www.ehealth.fgov.be/standards/fhir/mycarenet/StructureDefinition/be-eagreementclaim")),
                            status=Status("active"),
                            type=TypeType(
                                coding=EventCoding(
                                    system=System("http://terminology.hl7.org/CodeSystem/claim-type"),
                                    code=Code("professional"),
                                )
                            ),
                            sub_type=SubType(
                                coding=Coding(
                                    system=System("http://www.mycarenet.be/fhir/CodeSystem/agreement-types"),
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
                            created=Created(now.isoformat()),
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
                                        system=System("http://www.mycarenet.be/fhir/CodeSystem/nihdi-physiotherapy-pathologysituationcode"),
                                        code=Code("fb-51")
                                    ),
                                ),
                                serviced_date=ServicedDate(XmlDate.from_date(datetime.date.today() - datetime.timedelta(days=156)))
                            )

                        ),
                    )
                )
        
        bundle = Bundle(
            id=Id(id_),
            timestamp=Timestamp(now.isoformat()),
            type=TypeType(value="message"),
            entry=[
                message_header,
                organization,
                practitioner_role_physio,
                practitioner_physio,
                patient,
                practitioner_role_physician,
                practitioner_physician,
                annex,
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
        bundleLocation: str,
        patientNiss: str = "90060421941"
        ) -> str:
        template, id_ = self.render_bundle()
        nihii = self.set_configuration_from_token(token)

        responseBuilder = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreement.builders.ResponseObjectBuilderFactory.getResponseObjectBuilder()
        
        bundle = bytes(template, encoding="utf-8")

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