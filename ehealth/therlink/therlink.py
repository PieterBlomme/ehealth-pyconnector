from py4j.java_gateway import JavaGateway
from pydantic import BaseModel
import base64
import logging
from typing import Optional
from io import StringIO
from ..sts.assertion import Assertion
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata_pydantic.bindings import XmlParser
from ehealth.efact.efact import Practitioner

logger = logging.getLogger(__name__)

class TherLinkPatient(BaseModel):
    ssin: str
    firstname: str
    lastname: str
    eidnumber: Optional[str]
    isinumber: Optional[str]
    signed_encoded: Optional[bytes]


class TherLinkService:
    def __init__(
            self,
            mycarenet_license_username: str,
            mycarenet_license_password: str,
            etk_endpoint: str = "$uddi{uddi:ehealth-fgov-be:business:etkdepot:v1}",
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

        self.config_validator.setProperty("mycarenet.licence.username", mycarenet_license_username)
        self.config_validator.setProperty("mycarenet.licence.password", mycarenet_license_password)


    def set_configuration_from_token(self, token: str) -> Practitioner:
        # TODO copy paste from MDA
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

        print(f"Name: {givenname} {surname}, SSIN {ssin}, NIHII {nihii}, quality {quality}")
        
        self.config_validator.setProperty("main.kmehr.quality", "persphysiotherapist")
        self.config_validator.setProperty("kmehr.default.identifier.id.idhcparty.value", nihii)
        self.config_validator.setProperty("kmehr.default.identifier.id.inss.value", ssin)
        self.config_validator.setProperty("kmehr.single.hcparty.template.careprovider.in.therapeuticlink.id.inss.value", ssin)
        self.config_validator.setProperty("kmehr.single.hcparty.template.careprovider.in.therapeuticlink.id.idhcparty.value", nihii)
        self.config_validator.setProperty("kmehr.default.identifier.cd.cdhcparty.value", "pers" + quality)
        self.config_validator.setProperty("kmehr.default.identifier.firstname", givenname)
        self.config_validator.setProperty("kmehr.default.identifier.lastname", surname)

        hcparty = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.util.ConfigReader.getCareProvider()
        hcparty.setFamilyName(surname)
        hcparty.setFirstName(givenname)
        hcparty.setNihii(nihii)
        hcparty.setType("persphysiotherapist")
        hcparty.setInss(ssin)
        return hcparty
    
    # def verify_result(self, response: Any):
    #     signVerifResult = response.getSignatureVerificationResult()
    #     for entry in signVerifResult.getErrors():
    #         self.GATEWAY.jvm.org.junit.Assert.assertTrue("Errors found in the signature verification",
    #             entry.getValue().isValid())

    def createMandateTherapeuticLinkForProof(self, patient, hcparty):
        # TODO read patient from eid??
        commonBuilder = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.builders.RequestObjectBuilderFactory.getCommonBuilder()
        start = self.GATEWAY.jvm.org.joda.time.DateTime()
        end = start.plusMinutes(5)

        return commonBuilder.createTherapeuticLink(start, end, patient, self.GATEWAY.jvm.be.ehealth.business.kmehrcommons.HcPartyUtil.getAuthorKmehrQuality(), "ignored", None, hcparty)

    def create_signature_content(self, therapeuticLink) -> str:
        requestObjectMapper = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.mappers.MapperFactory.getRequestObjectMapper()
        contentToSign = requestObjectMapper.createTherapeuticLinkAsXmlString(therapeuticLink)
        print(f"contentToSign: {contentToSign} of type {type(contentToSign)}")
        content_bytes = bytes(contentToSign, "utf-8") 
        return base64.b64encode(content_bytes).decode("utf-8")

    # def addSignature(self, therapeuticLink, proof):
    #     content_encoded = self.create_signature_content(therapeuticLink) 

    #     response = requests.post("http://localhost:8099/certificate", json={"data": content_encoded})
    #     print(f"response {response.content} of type {type(response.content)}")
    #     if response.status_code != 200:
    #         raise Exception(response.content)
    #     signatureBytes = base64.b64decode(response.content)
    #     binaryProof = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.domain.requests.BinaryProof("CMS", signatureBytes)
    #     proof.setBinaryProof(binaryProof)
    #     return proof

    # def createProofForEidReading(self, patient, hcparty):
    #     proof = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.domain.Proof(self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.domain.ProofTypeValues.EIDSIGNING.getValue())
    #     print(f"proof: {proof}")
    #     therapeuticlink = self.createMandateTherapeuticLinkForProof(patient, hcparty)
    #     print(f"therapeuticlink: {therapeuticlink}")
    #     proof = self.addSignature(therapeuticlink, proof)
    #     return proof

    def has_therlink(self, token, patient_in: TherLinkPatient) -> bool:
        hcparty = self.set_configuration_from_token(token)
        print(f"hcparty: {hcparty}")
        commonBuilder = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.builders.RequestObjectBuilderFactory.getCommonBuilder()
        requestObjectBuilder = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.builders.RequestObjectBuilderFactory.getRequestObjectBuilder()
        requestObjectMapper = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.mappers.MapperFactory.getRequestObjectMapper()
        samlToken = self.GATEWAY.jvm.be.ehealth.technicalconnector.session.Session.getInstance().getSession().getSAMLToken()
        responseObjectMapper = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.mappers.MapperFactory.getResponseObjectMapper()
        therLinkService = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.service.ServiceFactory.getTherLinkService()

        kmehrId = commonBuilder.createKmehrID()
        print(f"kmehrId: {kmehrId}")
        author = commonBuilder.createAuthor(requestObjectBuilder.getAuthorHcParties())
        print(f"author: {author}")
        start = self.GATEWAY.jvm.org.joda.time.DateTime()
        end = (self.GATEWAY.jvm.org.joda.time.DateTime()).plusMonths(6)
        patient = self.GATEWAY.jvm.be.ehealth.business.common.domain.Patient.Builder().withFamilyName(patient_in.lastname).withFirstName(patient_in.firstname).withInss(patient_in.ssin).build()
        print(f"patient: {patient}")
        therapeuticLink = commonBuilder.createTherapeuticLink(start, end, patient, "persphysiotherapist", None, None, hcparty)

        request = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.domain.requests.HasTherapeuticLinkRequest(self.GATEWAY.jvm.org.joda.time.DateTime(), kmehrId, author, therapeuticLink)
        print(f"request: {request}")

        mappedRequest = requestObjectMapper.mapHasTherapeuticLinkRequest(request)

        hasTherapeuticLink = therLinkService.hasTherapeuticLink(samlToken, mappedRequest)
        print(f"hasTherapeuticLink: {hasTherapeuticLink.isValue()}")
        print(self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(hasTherapeuticLink))

        response = responseObjectMapper.mapJaxbToHasTherapeuticLinkResponse(hasTherapeuticLink)
        print(f"response: {response}")
        print(f"acknowledge: {response.getAcknowledge()}")
        ack = response.getAcknowledge()
        print(f"errors: {ack.getListOfErrors()} of len {len(ack.getListOfErrors())}")
        if len(ack.getListOfErrors()) > 1:
            raise Exception([err.getErrorDescription() for err in ack.getListOfErrors()])
        elif len(ack.getListOfErrors()) == 1:
            raise Exception(ack.getListOfErrors()[0].getErrorDescription())

        return hasTherapeuticLink.isValue()
    
    def create_therlink_content(self, token: str, patient_in: TherLinkPatient) -> str:
        hcparty = self.set_configuration_from_token(token)
        print(f"hcparty: {hcparty}")
        patient = self.GATEWAY.jvm.be.ehealth.business.common.domain.Patient.Builder().withFamilyName(patient_in.lastname).withFirstName(patient_in.firstname).withInss(patient_in.ssin).build()
        therapeuticlink = self.createMandateTherapeuticLinkForProof(patient, hcparty)
        return self.create_signature_content(therapeuticlink)

    def post_therlink(self, token: str, patient_in: TherLinkPatient) -> None:
        hcparty = self.set_configuration_from_token(token)
        print(f"hcparty: {hcparty}")

        therLinkService = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.service.ServiceFactory.getTherLinkService()

        if patient_in.eidnumber:
            patient = (
                self.GATEWAY.jvm.be.ehealth.business.common.domain.Patient.Builder()
                .withFamilyName(patient_in.lastname)
                .withFirstName(patient_in.firstname)
                .withEid(patient_in.eidnumber)
                .withInss(patient_in.ssin).build()
            )
            print(f"patient: {patient}")
            proof = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.domain.Proof(self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.domain.ProofTypeValues.EIDREADING.getValue())
            print(f"proof: {proof}")
        elif patient_in.isinumber:
            patient = (
                self.GATEWAY.jvm.be.ehealth.business.common.domain.Patient.Builder()
                .withFamilyName(patient_in.lastname)
                .withFirstName(patient_in.firstname)
                .withIsiPlus(patient_in.isinumber)
                .withInss(patient_in.ssin).build()
            )
            print(f"patient: {patient}")
            proof = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.domain.Proof(self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.domain.ProofTypeValues.ISIREADING.getValue())
            print(f"proof: {proof}")
        else:
            patient = self.GATEWAY.jvm.be.ehealth.business.common.domain.Patient.Builder().withFamilyName(patient_in.lastname).withFirstName(patient_in.firstname).withInss(patient_in.ssin).build()
            print(f"patient: {patient}")
            proof = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.domain.Proof(self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.domain.ProofTypeValues.EIDSIGNING.getValue())
            print(f"proof: {proof}")
            signatureBytes = base64.b64decode(patient_in.signed_encoded)
            binaryProof = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.domain.requests.BinaryProof("CMS", signatureBytes)
            proof.setBinaryProof(binaryProof)

    # def post_therlink(self, token: str,
    #                ):
    #     hcparty = self.set_configuration_from_token(token)
    #     print(f"hcparty: {hcparty}")
    #     therLinkService = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.service.ServiceFactory.getTherLinkService()
    #     patient = self.GATEWAY.jvm.be.ehealth.business.common.domain.Patient.Builder().withFamilyName(patient.lastname).withFirstName(patient.firstname).withInss(patient.ssin).build()

    #     proof = self.createProofForEidReading(patient, hcparty)
        
        linkType = "consultation"
        
        requestObjectBuilder = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.builders.RequestObjectBuilderFactory.getRequestObjectBuilder()
        
        request = requestObjectBuilder.createPutTherapeuticLinkRequest(patient, hcparty, linkType, proof)
        print(f"request: {request}")

        mapPutTherapeuticLinkRequest = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.mappers.MapperFactory.getRequestObjectMapper().mapPutTherapeuticLinkRequest(request)
        print(mapPutTherapeuticLinkRequest)

        samlToken = self.GATEWAY.jvm.be.ehealth.technicalconnector.session.Session.getInstance().getSession().getSAMLToken()
        putTherapeuticLink = therLinkService.putTherapeuticLink(samlToken, mapPutTherapeuticLinkRequest)
        print(f"putTherapeuticLink: {putTherapeuticLink}")
        response = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.mappers.MapperFactory.getResponseObjectMapper().mapJaxbToPutTherapeuticLinkResponse(putTherapeuticLink)
        print(f"response: {response}")
        ack = response.getAcknowledge()
        print(f"errors: {ack.getListOfErrors()} of len {len(ack.getListOfErrors())}")
        if len(ack.getListOfErrors()) > 1:
            raise Exception([err.getErrorDescription() for err in ack.getListOfErrors()])
        elif len(ack.getListOfErrors()) == 1:
            raise Exception(ack.getListOfErrors()[0].getErrorDescription())

    def revoke_therlink(self, token, patient_in: TherLinkPatient) -> bool:
        hcparty = self.set_configuration_from_token(token)
        print(f"hcparty: {hcparty}")
        commonBuilder = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.builders.RequestObjectBuilderFactory.getCommonBuilder()
        requestObjectBuilder = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.builders.RequestObjectBuilderFactory.getRequestObjectBuilder()
        requestObjectMapper = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.mappers.MapperFactory.getRequestObjectMapper()
        samlToken = self.GATEWAY.jvm.be.ehealth.technicalconnector.session.Session.getInstance().getSession().getSAMLToken()
        responseObjectMapper = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.mappers.MapperFactory.getResponseObjectMapper()
        therLinkService = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.service.ServiceFactory.getTherLinkService()

        kmehrId = commonBuilder.createKmehrID()
        print(f"kmehrId: {kmehrId}")
        author = commonBuilder.createAuthor(requestObjectBuilder.getAuthorHcParties())
        print(f"author: {author}")
        start = self.GATEWAY.jvm.org.joda.time.DateTime()
        end = (self.GATEWAY.jvm.org.joda.time.DateTime()).plusMonths(6)
        patient = self.GATEWAY.jvm.be.ehealth.business.common.domain.Patient.Builder().withFamilyName(patient_in.lastname).withFirstName(patient_in.firstname).withInss(patient_in.ssin).build()
        print(f"patient: {patient}")
        therapeuticLink = commonBuilder.createTherapeuticLink(start, end, patient, "persphysiotherapist", None, None, hcparty)
        
        patient = (
            self.GATEWAY.jvm.be.ehealth.business.common.domain.Patient.Builder()
            .withFamilyName(patient_in.lastname)
            .withFirstName(patient_in.firstname)
            .withEid(patient_in.eidnumber)
            .withInss(patient_in.ssin).build()
        )
        print(f"patient: {patient}")
        proof = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.domain.Proof(self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.domain.ProofTypeValues.EIDREADING.getValue())
        print(f"proof: {proof}")
        request = self.GATEWAY.jvm.be.ehealth.businessconnector.therlink.domain.requests.RevokeTherapeuticLinkRequest(self.GATEWAY.jvm.org.joda.time.DateTime(), kmehrId, author, therapeuticLink)
        print(f"request: {request}")

        mappedRequest = requestObjectMapper.mapRevokeTherapeuticLinkRequest(request)

        revokeTherapeuticLink = therLinkService.revokeTherapeuticLink(samlToken, mappedRequest)
        print(f"revokeTherapeuticLink: {revokeTherapeuticLink.isValue()}")
        print(self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(revokeTherapeuticLink))

        response = responseObjectMapper.mapJaxbToRevokeTherapeuticLinkResponse(revokeTherapeuticLink)
        print(f"response: {response}")
        print(f"acknowledge: {response.getAcknowledge()}")
        ack = response.getAcknowledge()
        print(f"errors: {ack.getListOfErrors()} of len {len(ack.getListOfErrors())}")
        if len(ack.getListOfErrors()) > 1:
            raise Exception([err.getErrorDescription() for err in ack.getListOfErrors()])
        elif len(ack.getListOfErrors()) == 1:
            raise Exception(ack.getListOfErrors()[0].getErrorDescription())

        return revokeTherapeuticLink.isValue()