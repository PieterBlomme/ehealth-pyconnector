import logging
import shutil
from io import StringIO
from py4j.java_gateway import JavaGateway
from py4j.protocol import Py4JJavaError
from typing import Any
from pathlib import Path
from contextlib import contextmanager
from .base import AbstractSTSService
from .assertion import Assertion
from xsdata_pydantic.bindings import XmlParser

logger = logging.getLogger(__name__)

PHYSIOTHERAPY_DESIGNATORS = [
        ("sessionmanager.samlattributedesignator.1", "urn:be:fgov:ehealth:1.0:certificateholder:person:ssin, urn:be:fgov:identification-namespace"),
        ("sessionmanager.samlattributedesignator.2", "urn:be:fgov:person:ssin, urn:be:fgov:identification-namespace"),
        ("sessionmanager.samlattributedesignator.3", "urn:be:fgov:person:ssin:ehealth:1.0:professional:physiotherapist:boolean, urn:be:fgov:certified-namespace:ehealth"),
        ("sessionmanager.samlattributedesignator.4", "urn:be:fgov:person:ssin:ehealth:1.0:nihii:physiotherapist:nihii11, urn:be:fgov:certified-namespace:ehealth"),
        ("sessionmanager.samlattributedesignator.5", "urn:be:fgov:person:ssin:ehealth:1.0:givenname, urn:be:fgov:certified-namespace:ehealth"),
        ("sessionmanager.samlattributedesignator.6", "urn:be:fgov:person:ssin:ehealth:1.0:surname, urn:be:fgov:certified-namespace:ehealth"),
        ("sessionmanager.samlattributedesignator.7", "urn:be:fgov:person:ssin:ehealth:1.0:fpsph:physiotherapist:boolean, urn:be:fgov:certified-namespace:ehealth"),
]

GATEWAY_ROOT = Path(__file__).parent.parent.parent

class KeyStoreException(Exception):
    pass

class SoapFaultException(Exception):
    pass

class InvalidSessionException(Exception):
    pass

class STSService(AbstractSTSService):
    def __init__(
            self,
            sts_endpoint: str = "$uddi{uddi:ehealth-fgov-be:business:iamsecuritytokenservice:v1}",
            environment: str = "acc",
            keystore_dir: str = "tests/data/",
    ):
        self.GATEWAY = JavaGateway()
        self.EHEALTH_JVM = self.GATEWAY.entry_point
        self.HOK_METHOD = self.GATEWAY.jvm.be.ehealth.technicalconnector.service.sts.impl.AbstractSTSService.HOK_METHOD
        self.config_validator = self.EHEALTH_JVM.getConfigValidator()

        # set up required configuration
        self.config_validator.setProperty("KEYSTORE_DIR", keystore_dir)
        self.config_validator.setProperty("environment", environment)
        self.config_validator.setProperty("endpoint.sts", sts_endpoint)
        
    def _build_designators_physiotherapy(self) -> Any:

        designators = self.EHEALTH_JVM.createAttributeDesignatorList()
        for v1, v2 in (
            ("urn:be:fgov:ehealth:1.0:certificateholder:person:ssin", "urn:be:fgov:identification-namespace"),
            ("urn:be:fgov:person:ssin", "urn:be:fgov:identification-namespace"),
            (
                "urn:be:fgov:person:ssin:ehealth:1.0:professional:physiotherapist:boolean",
                "urn:be:fgov:certified-namespace:ehealth"
            ),
            (
                "urn:be:fgov:person:ssin:ehealth:1.0:nihii:physiotherapist:nihii11",
                "urn:be:fgov:certified-namespace:ehealth"
            ),
            (
                "urn:be:fgov:person:ssin:ehealth:1.0:givenname",
                "urn:be:fgov:certified-namespace:ehealth"
            ),
            (
                "urn:be:fgov:person:ssin:ehealth:1.0:surname",
                "urn:be:fgov:certified-namespace:ehealth"
            ),
            (
                "urn:be:fgov:person:ssin:ehealth:1.0:fpsph:physiotherapist:boolean",
                "urn:be:fgov:certified-namespace:ehealth"
            )
        ):
            designator = self.GATEWAY.jvm.be.ehealth.technicalconnector.service.sts.domain.SAMLAttributeDesignator(v1, v2)
            designators.add(designator)
        return designators


    def _build_saml_attributes_physiotherapy(self, ssin: str) -> Any:
        attributes = self.EHEALTH_JVM.createSAMLAttributeList()
        for v1, v2, v3 in (
            (
            "urn:be:fgov:ehealth:1.0:certificateholder:person:ssin",
            "urn:be:fgov:identification-namespace",
            ssin
            ),
            ("urn:be:fgov:person:ssin", "urn:be:fgov:identification-namespace", ssin)
        ):
            attribute = self.EHEALTH_JVM.createSAMLAttribute(v1, v2, v3)
            attributes.add(attribute)
        return attributes
    
    def build_designators(self, quality: str = "physiotherapy") -> Any:
        if quality == "physiotherapy":
            return self._build_designators_physiotherapy()
        else:
            raise NotImplementedError("Not yet implemented, other designators needed")
    
    def build_saml_attributes(self, ssin: str, quality: str = "physiotherapy") -> Any:
        if quality == "physiotherapy":
            return self._build_saml_attributes_physiotherapy(ssin)
        else:
            raise NotImplementedError("Not yet implemented, other attributes needed")
    
    def create_service(self, path: str, pwd: str, alias: str) -> Any:
        try:
            return self.GATEWAY.jvm.be.ehealth.technicalconnector.service.sts.security.impl.KeyStoreCredential(path, alias, pwd)
        except Py4JJavaError as e:
            if e.java_exception.getMessage() == "Error while loading the KeyStore":
                raise KeyStoreException
            else:
                raise e

    def get_token(self, path: str, pwd: str, ssin: str, quality: str = "physiotherapy") -> str:
        designators = self.build_designators(quality)
        attributes = self.build_saml_attributes(ssin, quality)
        authentication = self.create_service(path, pwd, "authentication")
        service = self.create_service(path, pwd, "authentication")
        
        try:
            return self.GATEWAY.jvm.be.ehealth.technicalconnector.service.sts.STSServiceFactory.getInstance().getToken(authentication, service, attributes, designators, self.HOK_METHOD, 24)
        except Py4JJavaError as e:
            if str(e.java_exception.getClass()) == "class javax.xml.ws.soap.SOAPFaultException":
                raise SoapFaultException(e.java_exception.getMessage())
            else:
                raise e
    
    def get_serialized_token(self, path: str, pwd: str, ssin: str, quality: str = "physiotherapy") -> str:
        assertion = self.get_token(path, pwd, ssin, quality)
        return self.GATEWAY.jvm.be.ehealth.technicalconnector.service.sts.utils.SAMLConverter.toXMLString(assertion)

    def set_configuration_from_token(self, token: str):
        parser = XmlParser()
        token_pydantic = parser.parse(StringIO(token), Assertion)
        
        ssin = None
        quality = None
        
        for attribute in token_pydantic.attribute_statement.attribute:
            if attribute.attribute_name == 'urn:be:fgov:ehealth:1.0:certificateholder:person:ssin':
                ssin = attribute.attribute_value
            elif attribute.attribute_name.startswith('urn:be:fgov:person:ssin:ehealth:1.0:fpsph'):
                if attribute.attribute_value:
                    quality = attribute.attribute_name.split(':')[-2]

        logger.info(f"SSIN {ssin}, quality {quality}")
        
        # setting attributes
        if quality == "physiotherapist":
            for v1, v2 in PHYSIOTHERAPY_DESIGNATORS:
                self.config_validator.setProperty(v1, v2)
            self.config_validator.setProperty("sessionmanager.samlattribute.1", f"urn:be:fgov:ehealth:1.0:certificateholder:person:ssin, urn:be:fgov:identification-namespace, {ssin}")
            self.config_validator.setProperty("sessionmanager.samlattribute.2", f"urn:be:fgov:person:ssin, urn:be:fgov:identification-namespace, {ssin}")
        else:
            raise NotImplementedError("Not yet implemented, other attributes needed")
        
        
    @contextmanager
    def session(self, token: str, path: str, pwd: str) -> str:
        self.set_configuration_from_token(token)
        assertion = self.GATEWAY.jvm.be.ehealth.technicalconnector.service.sts.utils.SAMLConverter.toElement(token)
        service = self.GATEWAY.jvm.be.ehealth.technicalconnector.service.sts.security.impl.KeyStoreCredential(path, "authentication", pwd)
        token = self.GATEWAY.jvm.be.ehealth.technicalconnector.service.sts.SAMLTokenFactory.getInstance().createSamlToken(assertion, service)
        sessionmgmt = self.GATEWAY.jvm.be.ehealth.technicalconnector.session.Session.getInstance()

        self.config_validator.setProperty("sessionmanager.holderofkey.keystore", path)
        self.config_validator.setProperty("sessionmanager.encryption.keystore", path)
        self.config_validator.setProperty("sessionmanager.identification.keystore", path)

        sessionmgmt.loadSession(token, pwd, pwd)

        try:
            self.GATEWAY.jvm.org.junit.Assert.assertNotNull(token)
            try:
                self.GATEWAY.jvm.org.junit.Assert.assertEquals(True, sessionmgmt.hasValidSession())
            except Exception as e:
                raise InvalidSessionException("Session is invalid or has expired")
            yield sessionmgmt
        finally:
            sessionmgmt.unloadSession()