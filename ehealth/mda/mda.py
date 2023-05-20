from py4j.java_gateway import JavaGateway
import logging
import datetime
import tempfile
import uuid
from typing import List, Optional
from io import StringIO
from ..sts.assertion import Assertion
from .attribute_query import AttributeQuery, Issuer, Extensions, Subject, SubjectConfirmation, SubjectConfirmationData, NameId, Facet, Dimension
from . response import MemberData, Response
from xsdata.models.datatype import XmlDateTime
from xsdata_pydantic.bindings import XmlSerializer, XmlParser

logger = logging.getLogger(__name__)

class AbstractMDAService:
    pass

class FakeMDAService(AbstractMDAService):
    pass

class MDAService(AbstractMDAService):
    def __init__(
            self,
            mycarenet_license_username: str,
            mycarenet_license_password: str,
            etk_endpoint: str = "$uddi{uddi:ehealth-fgov-be:business:etkdepot:v1}",
            environment: str = "acc",
    ):
        self.GATEWAY = JavaGateway()
        self.EHEALTH_JVM = self.GATEWAY.entry_point
        self.HOK_METHOD = self.GATEWAY.jvm.be.ehealth.technicalconnector.service.sts.impl.AbstractMDAService.HOK_METHOD
    
        # set up required configuration
        self.config_validator = self.EHEALTH_JVM.getConfigValidator()
        
        self.config_validator.setProperty("mycarenet.licence.username", mycarenet_license_username)
        self.config_validator.setProperty("mycarenet.licence.password", mycarenet_license_password)
        self.config_validator.setProperty("endpoint.etk", etk_endpoint)
        self.config_validator.setProperty("environment", environment)

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
    
    def render_attribute_query(
        self, 
        nihii: str, 
        ssin: Optional[str],
        registrationNumber: Optional[str],
        mutuality: Optional[str], 
        notBefore: datetime.datetime, 
        notOnOrAfter: datetime.datetime,
        facets: List[Facet]
        ):
        now = datetime.datetime.now()
        id_ = str(uuid.uuid4())
        
        if ssin is not None:
            name_id = NameId(value=ssin)
        else:
            assert registrationNumber is not None
            assert mutuality is not None
            name_id = NameId(value=f"{registrationNumber}@{mutuality}", format="urn:be:cin:nippin:careReceiver:registrationNumber@mut")
            
        attrquery = AttributeQuery(
            issue_instant=XmlDateTime.from_datetime(now),
            id="_" + id_,
            issuer=Issuer(
                value=nihii
            ),
            extensions=Extensions(
                facets=facets
            ),
            subject=Subject(
                name_id=name_id,
                subject_confirmation=SubjectConfirmation(
                    subject_confirmation_data=SubjectConfirmationData(
                        not_before=XmlDateTime.from_datetime(notBefore),
                        not_on_or_after=XmlDateTime.from_datetime(notOnOrAfter),
                    )
                )
            ),
        )
        serializer = XmlSerializer()
        serializer.config.pretty_print = True
        serializer.config.xml_declaration = True
        ns_map = {
            "samlp": "urn:oasis:names:tc:SAML:2.0:protocol",
            "saml": "urn:oasis:names:tc:SAML:2.0:assertion",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "ext": "urn:be:cin:nippin:memberdata:saml:extension"
        }
        return serializer.render(attrquery, ns_map), id_
        
    def get_member_data(
        self, 
        token: str, 
        notBefore: datetime.datetime, 
        notOnOrAfter: datetime.datetime,
        ssin: Optional[str] = None,
        registrationNumber: Optional[str] = None,
        mutuality: Optional[str] = None, 
        facets=[
                    Facet(
                        id="urn:be:cin:nippin:insurability",
                        dimensions=[
                            Dimension(
                                id="requestType",
                                value="information",
                            ),
                            Dimension(
                                id="contactType",
                                value="other",
                            ),
                        ]
                    )
                ],
        ) -> str:
        nihii = self.set_configuration_from_token(token)
        
        template, id_ = self.render_attribute_query(nihii, ssin, registrationNumber, mutuality, notBefore, notOnOrAfter, facets=facets)

        with tempfile.NamedTemporaryFile(suffix='.xml', mode='w', delete=False) as tmp:
            # obviously this is lazy ...
            tmp.write(template)
        content = self.EHEALTH_JVM.createAttributeQueryFromTemplate(self.EHEALTH_JVM.createHashMap(), tmp.name)
                    
        inputReference = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.domain.InputReference(id_)        
        memberDataRequest = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.memberdatacommons.builders.RequestObjectBuilderFactory.getEncryptedRequestObjectBuilder().buildConsultationRequest(True, inputReference, content)
        raw_request = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(memberDataRequest)
        
        service = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.memberdatav2.session.MemberDataSessionServiceFactory.getMemberDataSyncService()
        wsResponse = service.consultMemberData(memberDataRequest)
        
        raw_response = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(wsResponse)
        responseBuilder = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.memberdatav2.builders.ResponseObjectBuilderFactory.getResponseObjectBuilder()
        response = responseBuilder.handleConsultationResponse(wsResponse)
        signVerifResult = response.getSignatureVerificationResult()
        for entry in signVerifResult.entrySet():
            self.GATEWAY.jvm.org.junit.Assert.assertTrue("Errors found in the signature verification",
                  entry.getValue().isValid())
        
        parser = XmlParser()
        response_string = self.GATEWAY.jvm.java.lang.String(response.getResponse(), "UTF-8")
        response_pydantic = parser.parse(StringIO(response_string), Response)
        
        return MemberData(
            response=response_pydantic,
            transaction_request=template,
            transaction_response=response_string,
            soap_request=raw_request,
            soap_response=raw_response
        )