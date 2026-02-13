from py4j.java_gateway import JavaGateway
import logging
import datetime
import tempfile
import uuid
from typing import List, Optional, Tuple, Callable
from pydantic import BaseModel, model_validator
from io import StringIO
from ..sts.assertion import Assertion
from .attribute_query import AttributeQuery, Issuer, Extensions, Subject, SubjectConfirmation, SubjectConfirmationData, NameId, Facet, Dimension
from . response import MemberData, Response
from xsdata.models.datatype import XmlDateTime
from xsdata_pydantic.bindings import XmlSerializer, XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from ehealth.utils.callbacks import storage_callback, CallMetadata, CallType, ServiceType

logger = logging.getLogger(__name__)


class MDAInputModel(BaseModel):
    notBefore: datetime.datetime
    notOnOrAfter: datetime.datetime
    ssin: Optional[str] = None
    registrationNumber: Optional[str] = None
    mutuality: Optional[str] = None
    facets: List[Facet] = [
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
    ]

    @model_validator(mode='before')
    @classmethod
    def check_card_number_omitted(cls, values):
        if isinstance(values, dict):
            ssin = values.get("ssin")
            registrationNumber = values.get("registrationNumber")
            mutuality = values.get("mutuality")
            if ssin is not None:
                if registrationNumber is not None or mutuality is not None:
                    raise ValueError("If SSIN is given, mutuality and registrationNumber should be None")
            else:
                if registrationNumber is None or mutuality is None:
                    raise ValueError("If SSIN is not given, mutuality and registrationNumber should both be provided")
        return values

    def __eq__(self, other):
            if other.__class__ is self.__class__:
                return self.model_dump_json() == other.model_dump_json()
            return NotImplemented

class AbstractMDAService:
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
        parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
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
    
class FakeMDAService(AbstractMDAService):
    def __init__(
            self,
            faked: List[Tuple[MDAInputModel, str]],
            environment: str = "acc",

    ):
        super().__init__(environment=environment)
        self.faked = faked

    def get_member_data(
        self, 
        token: str, 
        mda_input: MDAInputModel,
        callback_fn: Optional[Callable] = storage_callback
        ) -> str:
        nihii = self.set_configuration_from_token(token)

        template, id_ = self.render_attribute_query(nihii, mda_input.ssin, mda_input.registrationNumber, mda_input.mutuality, mda_input.notBefore, mda_input.notOnOrAfter, facets=mda_input.facets)
        
        parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
        for model, response_string in self.faked:
            if model == mda_input:
                response_pydantic = parser.parse(StringIO(response_string), Response)
                
                return MemberData(
                    response=response_pydantic,
                    transaction_request=template,
                    transaction_response=response_string,
                    soap_request="", # too much effort
                    soap_response="" # too much effort
                )
        raise NotImplementedError(f"Could not fake {mda_input}")

    
class MDAService(AbstractMDAService):
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

    def get_member_data(
        self, 
        token: str, 
        mda_input: MDAInputModel,
        callback_fn: Optional[Callable] = storage_callback
        ) -> str:
        timestamp = datetime.datetime.now()
        meta = CallMetadata(
            type=ServiceType.MDA,
            timestamp=timestamp,
            call_type=CallType.UNENCRYPTED_REQUEST,
            ssin=mda_input.ssin,
            registrationNumber=mda_input.registrationNumber,
            mutuality=mda_input.mutuality,
        )

        nihii = self.set_configuration_from_token(token)
        
        template, id_ = self.render_attribute_query(nihii, mda_input.ssin, mda_input.registrationNumber, mda_input.mutuality, mda_input.notBefore, mda_input.notOnOrAfter, facets=mda_input.facets)
        callback_fn(template, meta)

        with tempfile.NamedTemporaryFile(suffix='.xml', mode='w', delete=False) as tmp:
            # obviously this is lazy ...
            tmp.write(template)
        content = self.EHEALTH_JVM.createAttributeQueryFromTemplate(self.EHEALTH_JVM.createHashMap(), tmp.name)
                    
        inputReference = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.domain.InputReference(id_)        
        memberDataRequest = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.memberdatacommons.builders.RequestObjectBuilderFactory.getEncryptedRequestObjectBuilder().buildConsultationRequest(self.is_test, inputReference, content)
        raw_request = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(memberDataRequest)
        callback_fn(raw_request, meta.set_call_type(CallType.ENCRYPTED_REQUEST))

        service = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.memberdatav2.session.MemberDataSessionServiceFactory.getMemberDataSyncService()
        wsResponse = service.consultMemberData(memberDataRequest)
        
        raw_response = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(wsResponse)
        callback_fn(raw_response, meta.set_call_type(CallType.ENCRYPTED_RESPONSE))
        
        responseBuilder = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.memberdatav2.builders.ResponseObjectBuilderFactory.getResponseObjectBuilder()
        response = responseBuilder.handleConsultationResponse(wsResponse)
        signVerifResult = response.getSignatureVerificationResult()
        for entry in signVerifResult.entrySet():
            self.GATEWAY.jvm.org.junit.Assert.assertTrue("Errors found in the signature verification",
                  entry.getValue().isValid())
        
        parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
        response_string = self.GATEWAY.jvm.java.lang.String(response.getResponse(), "UTF-8")
        callback_fn(response_string, meta.set_call_type(CallType.UNENCRYPTED_RESPONSE))
        response_pydantic = parser.parse(StringIO(response_string), Response)
        
        return MemberData(
            response=response_pydantic,
            transaction_request=template,
            transaction_response=response_string,
            soap_request=raw_request,
            soap_response=raw_response
        )