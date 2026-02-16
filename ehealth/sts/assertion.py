from pydantic import BaseModel, Field
from typing import List, Optional, Union
from xsdata.models.datatype import XmlDateTime
import uuid
import datetime
class CanonicalizationMethod(BaseModel):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    algorithm: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Algorithm",
            "type": "Attribute",
        }
    )


class DigestMethod(BaseModel):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    algorithm: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Algorithm",
            "type": "Attribute",
        }
    )


class SignatureMethod(BaseModel):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    algorithm: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Algorithm",
            "type": "Attribute",
        }
    )


class Transform(BaseModel):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    algorithm: Optional[str] = Field(
        default=None,
        metadata={
            "name": "Algorithm",
            "type": "Attribute",
        }
    )


class X509Data(BaseModel):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    x509_certificate: Optional[str] = Field(
        default=None,
        metadata={
            "name": "X509Certificate",
            "type": "Element",
        }
    )


class Attribute(BaseModel):
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:1.0:assertion"

    attribute_name: Optional[str] = Field(
        default=None,
        metadata={
            "name": "AttributeName",
            "type": "Attribute",
        }
    )
    attribute_namespace: Optional[str] = Field(
        default=None,
        metadata={
            "name": "AttributeNamespace",
            "type": "Attribute",
        }
    )
    attribute_value: Optional[Union[bool, str]] = Field(
        default=None,
        metadata={
            "name": "AttributeValue",
            "type": "Element",
        }
    )


class Conditions(BaseModel):
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:1.0:assertion"

    not_before: Optional[XmlDateTime] = Field(
        default=None,
        metadata={
            "name": "NotBefore",
            "type": "Attribute",
        }
    )
    not_on_or_after: Optional[XmlDateTime] = Field(
        default=None,
        metadata={
            "name": "NotOnOrAfter",
            "type": "Attribute",
        }
    )


class NameIdentifier(BaseModel):
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:1.0:assertion"

    format: Optional[str] = Field(
        default="urn:oasis:names:tc:SAML:1.1:nameid-format:X509SubjectName",
        metadata={
            "name": "Format",
            "type": "Attribute",
        }
    )
    name_qualifier: Optional[str] = Field(
        default="CN=TEST-ZetesConfidens-eHealth acceptance test-issuing CA 001, SERIALNUMBER=001, O=ZETES SA, C=BE",
        metadata={
            "name": "NameQualifier",
            "type": "Attribute",
        }
    )
    value: str = Field(
        default=""
    )


class KeyInfo(BaseModel):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    x509_data: Optional[X509Data] = Field(
        default=None,
        metadata={
            "name": "X509Data",
            "type": "Element",
        }
    )


class Transforms(BaseModel):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    transform: List[Transform] = Field(
        default_factory=lambda: [
            Transform(algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"), 
            Transform(algorithm="http://www.w3.org/2001/10/xml-exc-c14n#")
            ],
        metadata={
            "name": "Transform",
            "type": "Element",
        }
    )


class Reference(BaseModel):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    uri: Optional[str] = Field(
        default=None,
        metadata={
            "name": "URI",
            "type": "Attribute",
        }
    )
    transforms: Optional[Transforms] = Field(
        default=None,
        metadata={
            "name": "Transforms",
            "type": "Element",
        }
    )
    digest_method: Optional[DigestMethod] = Field(
        default_factory=lambda: DigestMethod(algorithm="http://www.w3.org/2001/04/xmlenc#sha256"),
        metadata={
            "name": "DigestMethod",
            "type": "Element",
        }
    )
    digest_value: Optional[str] = Field(
        default=None,
        metadata={
            "name": "DigestValue",
            "type": "Element",
        }
    )


class SubjectConfirmation(BaseModel):
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:1.0:assertion"

    confirmation_method: Optional[str] = Field(
        default="urn:oasis:names:tc:SAML:1.0:cm:holder-of-key",
        metadata={
            "name": "ConfirmationMethod",
            "type": "Element",
        }
    )
    key_info: Optional[KeyInfo] = Field(
        default=None,
        metadata={
            "name": "KeyInfo",
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        }
    )


class SignedInfo(BaseModel):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    canonicalization_method: Optional[CanonicalizationMethod] = Field(
        default_factory=lambda: CanonicalizationMethod(algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"),
        metadata={
            "name": "CanonicalizationMethod",
            "type": "Element",
        }
    )
    signature_method: Optional[SignatureMethod] = Field(
        default_factory=lambda: SignatureMethod(algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"),
        metadata={
            "name": "SignatureMethod",
            "type": "Element",
        }
    )
    reference: Optional[Reference] = Field(
        default=None,
        metadata={
            "name": "Reference",
            "type": "Element",
        }
    )


class Subject(BaseModel):
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:1.0:assertion"

    name_identifier: Optional[NameIdentifier] = Field(
        default=None,
        metadata={
            "name": "NameIdentifier",
            "type": "Element",
        }
    )
    subject_confirmation: Optional[SubjectConfirmation] = Field(
        default=None,
        metadata={
            "name": "SubjectConfirmation",
            "type": "Element",
        }
    )


class Signature(BaseModel):
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    signed_info: Optional[SignedInfo] = Field(
        default=None,
        metadata={
            "name": "SignedInfo",
            "type": "Element",
        }
    )
    signature_value: Optional[str] = Field(
        default=None,
        metadata={
            "name": "SignatureValue",
            "type": "Element",
        }
    )
    key_info: Optional[KeyInfo] = Field(
        default=None,
        metadata={
            "name": "KeyInfo",
            "type": "Element",
        }
    )


class AttributeStatement(BaseModel):
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:1.0:assertion"

    subject: Optional[Subject] = Field(
        default=None,
        metadata={
            "name": "Subject",
            "type": "Element",
        }
    )
    attribute: List[Attribute] = Field(
        default_factory=list,
        metadata={
            "name": "Attribute",
            "type": "Element",
        }
    )


class AuthenticationStatement(BaseModel):
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:1.0:assertion"

    authentication_instant: Optional[XmlDateTime] = Field(
        default=None,
        metadata={
            "name": "AuthenticationInstant",
            "type": "Attribute",
        }
    )
    authentication_method: Optional[str] = Field(
        default="urn:oasis:names:tc:SAML:1.0:am:X509-PKI",
        metadata={
            "name": "AuthenticationMethod",
            "type": "Attribute",
        }
    )
    subject: Optional[Subject] = Field(
        default=None,
        metadata={
            "name": "Subject",
            "type": "Element",
        }
    )


class Assertion(BaseModel):
    """
    Assertion class for SAML 1.0 assertions.
    Uses Pydantic BaseModel for xsdata-pydantic compatibility with Pydantic v2.
    """
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:1.0:assertion"

    assertion_id: Optional[str] = Field(
        default=None,
        metadata={
            "name": "AssertionID",
            "type": "Attribute",
        }
    )
    issue_instant: Optional[XmlDateTime] = Field(
        default=None,
        metadata={
            "name": "IssueInstant",
            "type": "Attribute",
        }
    )
    issuer: Optional[str] = Field(
        default="urn:be:fgov:ehealth:sts:1_0",
        metadata={
            "name": "Issuer",
            "type": "Attribute",
        }
    )
    major_version: Optional[int] = Field(
        default=1,
        metadata={
            "name": "MajorVersion",
            "type": "Attribute",
        }
    )
    minor_version: Optional[int] = Field(
        default=1,
        metadata={
            "name": "MinorVersion",
            "type": "Attribute",
        }
    )
    conditions: Optional[Conditions] = Field(
        default=None,
        metadata={
            "name": "Conditions",
            "type": "Element",
        }
    )
    authentication_statement: Optional[AuthenticationStatement] = Field(
        default=None,
        metadata={
            "name": "AuthenticationStatement",
            "type": "Element",
        }
    )
    attribute_statement: Optional[AttributeStatement] = Field(
        default=None,
        metadata={
            "name": "AttributeStatement",
            "type": "Element",
        }
    )
    signature: Optional[Signature] = Field(
        default=None,
        metadata={
            "name": "Signature",
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        }
    )

    @classmethod
    def fake(cls):
        now = datetime.datetime.now()
        id_=str(uuid.uuid4())
        dummy_ssin="12345678901"
        dummy_surname="Doe"
        dummy_givenname="John"
        dummy_name = f"{dummy_givenname} {dummy_surname}"
        dummy_nihii="12345678901"
        signature_value="signature placeholder"
        certificate="certificate placeholder"
        
        return Assertion(
            assertion_id="_" + id_,
            issue_instant=XmlDateTime.from_datetime(now),
            conditions=Conditions(
                not_before=XmlDateTime.from_datetime(now - datetime.timedelta(minutes=5)),
                not_on_or_after=XmlDateTime.from_datetime(now + datetime.timedelta(days=1)),
                ),
            authentication_statement=AuthenticationStatement(
                authentication_instant=XmlDateTime.from_datetime(now),
                subject=Subject(
                    name_identifier=NameIdentifier(
                        value=f'CN="SSIN={dummy_ssin}", OU=eHealth-platform Belgium, OU={dummy_name}, OU="SSIN={dummy_ssin}", O=Federal Government, C=BE'
                    ),
                    subject_confirmation=SubjectConfirmation(
                        key_info=KeyInfo(
                            x509_data=X509Data( x509_certificate=certificate)
                        )
                    )
                )
                ),
            attribute_statement=AttributeStatement(
                subject=Subject(
                        name_identifier=NameIdentifier(
                            value=f'CN="SSIN={dummy_ssin}", OU=eHealth-platform Belgium, OU={dummy_name}, OU="SSIN={dummy_ssin}", O=Federal Government, C=BE'
                        ),
                    ),
                attribute=[
                    Attribute(
                        attribute_name="urn:be:fgov:ehealth:1.0:certificateholder:person:ssin",
                        attribute_value=dummy_ssin,
                        attribute_namespace="urn:be:fgov:identification-namespace",
                    ),
                    Attribute(
                        attribute_name="urn:be:fgov:person:ssin",
                        attribute_value=dummy_ssin,
                        attribute_namespace="urn:be:fgov:identification-namespace",
                    ),
                    Attribute(
                        attribute_name="urn:be:fgov:person:ssin:ehealth:1.0:professional:physiotherapist:boolean",
                        attribute_value=True,
                        attribute_namespace="urn:be:fgov:certified-namespace:ehealth",
                    ),
                    Attribute(
                        attribute_name="urn:be:fgov:person:ssin:ehealth:1.0:nihii:physiotherapist:nihii11",
                        attribute_value=dummy_nihii,
                        attribute_namespace="urn:be:fgov:certified-namespace:ehealth",
                    ),
                    Attribute(
                        attribute_name="urn:be:fgov:person:ssin:ehealth:1.0:givenname",
                        attribute_value=dummy_givenname,
                        attribute_namespace="urn:be:fgov:certified-namespace:ehealth",
                    ),
                    Attribute(
                        attribute_name="urn:be:fgov:person:ssin:ehealth:1.0:surname",
                        attribute_value=dummy_surname,
                        attribute_namespace="urn:be:fgov:certified-namespace:ehealth",
                    ),
                    Attribute(
                        attribute_name="urn:be:fgov:person:ssin:ehealth:1.0:fpsph:physiotherapist:boolean",
                        attribute_value=True,
                        attribute_namespace="urn:be:fgov:certified-namespace:ehealth",
                    ),
                ]
                ),
            signature=Signature(
                signed_info=SignedInfo(
                    reference=Reference(
                        uri="#_" + id_,
                        digest_value=str(uuid.uuid4()),
                    )
                    ),
                signature_value=signature_value,
                key_info=KeyInfo(
                            x509_data=X509Data( x509_certificate=certificate)
                        )
            )
        )

