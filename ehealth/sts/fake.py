from py4j.java_gateway import JavaGateway
import logging
from contextlib import contextmanager
from xsdata_pydantic.bindings import XmlSerializer
from .sts import STSService
from .assertion import Assertion

logger = logging.getLogger(__name__)

class FakeSTSService(STSService):
    """
    Mimics behaviour of STSService without actual external endpoint connection.  
    Keystore decryption is validated, but token request is faked.
    """
    
    def __init__(
            self,
    ):
        self.GATEWAY = JavaGateway()
        self.EHEALTH_JVM = self.GATEWAY.entry_point
        self.HOK_METHOD = self.GATEWAY.jvm.be.ehealth.technicalconnector.service.sts.impl.AbstractSTSService.HOK_METHOD
    
    def get_serialized_token(self, path: str, pwd: str, ssin: str, quality: str = "physiotherapy") -> str:
        designators = self.build_designators(quality)
        attributes = self.build_saml_attributes(ssin, quality)
        authentication = self.create_service(path, pwd, "authentication")
        service = self.create_service(path, pwd, "authentication")
        
        assertion = Assertion.fake()
        serializer = XmlSerializer()
        serializer.config.pretty_print = True
        serializer.config.xml_declaration = True
        ns_map = {
            "samlp": "urn:oasis:names:tc:SAML:2.0:protocol",
            "saml": "urn:oasis:names:tc:SAML:2.0:assertion",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "ext": "urn:be:cin:nippin:memberdata:saml:extension"
        }
        return serializer.render(assertion, ns_map)
    
    @contextmanager
    def session(self, token: str, path: str, pwd: str) -> str:
        # Basic validation of the token
        assertion = self.GATEWAY.jvm.be.ehealth.technicalconnector.service.sts.utils.SAMLConverter.toElement(token)
        # Basic decyrption check
        service = self.GATEWAY.jvm.be.ehealth.technicalconnector.service.sts.security.impl.KeyStoreCredential(path, "authentication", pwd)
        token = self.GATEWAY.jvm.be.ehealth.technicalconnector.service.sts.SAMLTokenFactory.getInstance().createSamlToken(assertion, service)
        yield None