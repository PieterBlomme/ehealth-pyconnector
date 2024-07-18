from py4j.java_gateway import JavaGateway
import logging
from typing import Optional
from io import StringIO
from xsdata_pydantic.bindings import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from .get_professional_contact_info_response import GetProfessionalContactInfoResponse
from . search_professionals_response import SearchProfessionalsResponse

logger = logging.getLogger(__name__)

class InvalidNihii(Exception):
    pass

class UnknownNihii(Exception):
    pass

class AbstractAddressBookService:
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

    def render_search_query(
        self, 
        first_name_search: Optional[str],
        last_name_search: str,
        profession_search: str,
        offset: Optional[int] = 0,
        limit: Optional[int] = 0
        ):
        request = self.GATEWAY.jvm.be.fgov.ehealth.addressbook.protocol.v1.SearchProfessionalsRequest()
        if first_name_search:
            request.setFirstName(first_name_search)
        if last_name_search:
            request.setLastName(last_name_search)
        if profession_search:
            request.setProfession(profession_search)
        request.setIssueInstant(self.GATEWAY.jvm.org.joda.time.DateTime.now())
        request.setOffset(offset)
        request.setMaxElements(limit)
        logger.info(f"offset {offset} limit {limit}")
        return request
    
    def render_get_query(
        self, 
        prof_nihii: str, 
        ):
        request = self.GATEWAY.jvm.be.fgov.ehealth.addressbook.protocol.v1.GetProfessionalContactInfoRequest()
        request.setNIHII(prof_nihii)
        request.setIssueInstant(self.GATEWAY.jvm.org.joda.time.DateTime.now())
        return request
    
class AddressBookService(AbstractAddressBookService):
    def __init__(
            self,
            etk_endpoint: str = "$uddi{uddi:ehealth-fgov-be:business:etkdepot:v1}",
            environment: str = "acc",
    ):
        super().__init__(environment=environment)
    
        # set up required configuration
        self.config_validator.setProperty("endpoint.etk", etk_endpoint)

    def get(
        self,
        prof_nihii: str
    ) -> GetProfessionalContactInfoResponse:
        request = self.render_get_query(prof_nihii)
        service = self.GATEWAY.jvm.be.ehealth.businessconnector.addressbook.session.AddressbookSessionServiceFactory.getAddressbookSessionService()
        
        try:
            response = service.getProfessionalContactInfo(request)
        except Exception as e:
            if f"The value '{prof_nihii}' of element 'NIHII' is not valid" in str(e.java_exception):
                raise InvalidNihii
            elif "Error while executing web service call" in str(e.java_exception):
                # this might catch more than just unknown
                raise UnknownNihii
            else:
                raise e

        
        response_string = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(response)
        parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
        return parser.parse(StringIO(response_string), GetProfessionalContactInfoResponse)

    def search(
        self,
        last_name_search: str,
        first_name_search: Optional[str] = None,
        profession_search: Optional[str] = "PHYSICIAN",
        ) -> SearchProfessionalsResponse:
        offset = 0
        limit = 20
        results = None
        while True:
            # handle pagination
            request = self.render_search_query(first_name_search, last_name_search, profession_search, offset=offset, limit=limit)
            service = self.GATEWAY.jvm.be.ehealth.businessconnector.addressbook.session.AddressbookSessionServiceFactory.getAddressbookSessionService()
            response = service.searchProfessionals(request)
            response_string = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(response)
            parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
            result = parser.parse(StringIO(response_string), SearchProfessionalsResponse)
            if not results:
                results = result
            else:
                results.health_care_professional.extend(result.health_care_professional)
            offset += limit
            if len(result.health_care_professional) < limit:
                break
        return results