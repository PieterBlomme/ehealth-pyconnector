from dataclasses import field
from pydantic import BaseModel, Field, ConfigDict
from pydantic.dataclasses import dataclass
from typing import List, Optional, Union
from xsdata.models.datatype import XmlDateTime
import uuid
import datetime

@dataclass
class CanonicalizationMethod:
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    algorithm: Optional[str] = field(
        default=None,
        metadata={
            "name": "Algorithm",
            "type": "Attribute",
        }
    )


@dataclass
class DigestMethod:
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    algorithm: Optional[str] = field(
        default=None,
        metadata={
            "name": "Algorithm",
            "type": "Attribute",
        }
    )


@dataclass
class SignatureMethod:
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    algorithm: Optional[str] = field(
        default=None,
        metadata={
            "name": "Algorithm",
            "type": "Attribute",
        }
    )


@dataclass
class Transform:
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    algorithm: Optional[str] = field(
        default=None,
        metadata={
            "name": "Algorithm",
            "type": "Attribute",
        }
    )


@dataclass
class X509Data:
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    x509_certificate: Optional[str] = field(
        default=None,
        metadata={
            "name": "X509Certificate",
            "type": "Element",
        }
    )


@dataclass
class Attribute:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:1.0:assertion"

    attribute_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "AttributeName",
            "type": "Attribute",
        }
    )
    attribute_namespace: Optional[str] = field(
        default=None,
        metadata={
            "name": "AttributeNamespace",
            "type": "Attribute",
        }
    )
    attribute_value: Optional[Union[bool, str]] = field(
        default=None,
        metadata={
            "name": "AttributeValue",
            "type": "Element",
        }
    )


@dataclass
class Conditions:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:1.0:assertion"

    not_before: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "NotBefore",
            "type": "Attribute",
        }
    )
    not_on_or_after: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "NotOnOrAfter",
            "type": "Attribute",
        }
    )


@dataclass
class NameIdentifier:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:1.0:assertion"

    format: Optional[str] = field(
        default="urn:oasis:names:tc:SAML:1.1:nameid-format:X509SubjectName",
        metadata={
            "name": "Format",
            "type": "Attribute",
        }
    )
    name_qualifier: Optional[str] = field(
        default="CN=TEST-ZetesConfidens-eHealth acceptance test-issuing CA 001, SERIALNUMBER=001, O=ZETES SA, C=BE",
        metadata={
            "name": "NameQualifier",
            "type": "Attribute",
        }
    )
    value: str = field(
        default=""
    )


@dataclass
class KeyInfo:
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    x509_data: Optional[X509Data] = field(
        default=None,
        metadata={
            "name": "X509Data",
            "type": "Element",
        }
    )


@dataclass
class Transforms:
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    transform: List[Transform] = field(
        default_factory=lambda: [
            Transform(algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"), 
            Transform(algorithm="http://www.w3.org/2001/10/xml-exc-c14n#")
            ],
        metadata={
            "name": "Transform",
            "type": "Element",
        }
    )


@dataclass
class Reference:
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    uri: Optional[str] = field(
        default=None,
        metadata={
            "name": "URI",
            "type": "Attribute",
        }
    )
    transforms: Optional[Transforms] = field(
        default=None,
        metadata={
            "name": "Transforms",
            "type": "Element",
        }
    )
    digest_method: Optional[DigestMethod] = field(
        default_factory=lambda: DigestMethod("http://www.w3.org/2001/04/xmlenc#sha256"),
        metadata={
            "name": "DigestMethod",
            "type": "Element",
        }
    )
    digest_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "DigestValue",
            "type": "Element",
        }
    )


@dataclass
class SubjectConfirmation:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:1.0:assertion"

    confirmation_method: Optional[str] = field(
        default="urn:oasis:names:tc:SAML:1.0:cm:holder-of-key",
        metadata={
            "name": "ConfirmationMethod",
            "type": "Element",
        }
    )
    key_info: Optional[KeyInfo] = field(
        default=None,
        metadata={
            "name": "KeyInfo",
            "type": "Element",
            "namespace": "http://www.w3.org/2000/09/xmldsig#",
        }
    )


@dataclass
class SignedInfo:
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    canonicalization_method: Optional[CanonicalizationMethod] = field(
        default_factory=lambda: CanonicalizationMethod("http://www.w3.org/2001/10/xml-exc-c14n#"),
        metadata={
            "name": "CanonicalizationMethod",
            "type": "Element",
        }
    )
    signature_method: Optional[SignatureMethod] = field(
        default_factory=lambda: SignatureMethod("http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"),
        metadata={
            "name": "SignatureMethod",
            "type": "Element",
        }
    )
    reference: Optional[Reference] = field(
        default=None,
        metadata={
            "name": "Reference",
            "type": "Element",
        }
    )


@dataclass
class Subject:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:1.0:assertion"

    name_identifier: Optional[NameIdentifier] = field(
        default=None,
        metadata={
            "name": "NameIdentifier",
            "type": "Element",
        }
    )
    subject_confirmation: Optional[SubjectConfirmation] = field(
        default=None,
        metadata={
            "name": "SubjectConfirmation",
            "type": "Element",
        }
    )


@dataclass
class Signature:
    class Meta:
        namespace = "http://www.w3.org/2000/09/xmldsig#"

    signed_info: Optional[SignedInfo] = field(
        default=None,
        metadata={
            "name": "SignedInfo",
            "type": "Element",
        }
    )
    signature_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "SignatureValue",
            "type": "Element",
        }
    )
    key_info: Optional[KeyInfo] = field(
        default=None,
        metadata={
            "name": "KeyInfo",
            "type": "Element",
        }
    )


@dataclass
class AttributeStatement:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:1.0:assertion"

    subject: Optional[Subject] = field(
        default=None,
        metadata={
            "name": "Subject",
            "type": "Element",
        }
    )
    attribute: List[Attribute] = field(
        default_factory=list,
        metadata={
            "name": "Attribute",
            "type": "Element",
        }
    )


@dataclass
class AuthenticationStatement:
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:1.0:assertion"

    authentication_instant: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "AuthenticationInstant",
            "type": "Attribute",
        }
    )
    authentication_method: Optional[str] = field(
        default="urn:oasis:names:tc:SAML:1.0:am:X509-PKI",
        metadata={
            "name": "AuthenticationMethod",
            "type": "Attribute",
        }
    )
    subject: Optional[Subject] = field(
        default=None,
        metadata={
            "name": "Subject",
            "type": "Element",
        }
    )


class Assertion(BaseModel):
    class Meta:
        namespace = "urn:oasis:names:tc:SAML:1.0:assertion"

    model_config = ConfigDict(defer_build=True)

    assertion_id: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "name": "AssertionID",
            "type": "Attribute",
        }
    )
    issue_instant: Optional[XmlDateTime] = Field(
        default=None,
        json_schema_extra={
            "name": "IssueInstant",
            "type": "Attribute",
        }
    )
    issuer: Optional[str] = Field(
        default="urn:be:fgov:ehealth:sts:1_0",
        json_schema_extra={
            "name": "Issuer",
            "type": "Attribute",
        }
    )
    major_version: Optional[int] = Field(
        default=1,
        json_schema_extra={
            "name": "MajorVersion",
            "type": "Attribute",
        }
    )
    minor_version: Optional[int] = Field(
        default=1,
        json_schema_extra={
            "name": "MinorVersion",
            "type": "Attribute",
        }
    )
    conditions: Optional[Conditions] = Field(
        default=None,
        json_schema_extra={
            "name": "Conditions",
            "type": "Element",
        }
    )
    authentication_statement: Optional[AuthenticationStatement] = Field(
        default=None,
        json_schema_extra={
            "name": "AuthenticationStatement",
            "type": "Element",
        }
    )
    attribute_statement: Optional[AttributeStatement] = Field(
        default=None,
        json_schema_extra={
            "name": "AttributeStatement",
            "type": "Element",
        }
    )
    signature: Optional[Signature] = Field(
        default=None,
        json_schema_extra={
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
