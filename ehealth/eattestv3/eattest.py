from py4j.java_gateway import JavaGateway
from typing import Any, Optional, Callable
import datetime
import pytz
import logging
from .input_models import Practitioner, Patient as PatientIn, EAttestInputModel, CancelEAttestInputModel, Transaction as TransactionIn
from io import StringIO
from ..sts.assertion import Assertion
from xsdata.models.datatype import XmlDate, XmlTime
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata_pydantic.bindings import XmlSerializer, XmlParser
from pydantic import BaseModel
from ehealth.utils.callbacks import storage_callback, CallMetadata, CallType, ServiceType
import tempfile
from .exceptions import EAttestRetryableAttempt, TechnicalEAttestException
from .send_transaction_request import (
    SendTransactionRequest,
    Request,
    Id2,
    Author2,
    Hcparty,
    Id1, Cd,
    Kmehrmessage,
    Header,
    Sender,
    Recipient,
    Patient,
    Folder,
    Insurancymembership,
    Sex,
    Transaction,
    Author1,
    Item,
    Cost,
    Content,
    Quantity,
    Text
)
from .send_transaction_response import EAttestV3, SendTransactionResponse

logger = logging.getLogger(__name__)

class EAttestV3Service:
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
        self.config_validator.setProperty("endpoint.etk", etk_endpoint)
        self.config_validator.setProperty("endpoint.eattestv3", "$uddi{uddi:ehealth-fgov-be:business:mycareneteattest:v3}")

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

        logger.info(f"Name: {givenname} {surname}, SSIN {ssin}, NIHII {nihii}, quality {quality}")
        self.config_validator.setProperty("mycarenet.default.careprovider.nihii.value", nihii)
        self.config_validator.setProperty("mycarenet.default.careprovider.nihii.quality", quality)
        self.config_validator.setProperty("mycarenet.default.careprovider.physicalperson.ssin", ssin)
        self.config_validator.setProperty("mycarenet.default.careprovider.physicalperson.name", f"{givenname} {surname}")
        return Practitioner(
                nihii=nihii,
                givenname=givenname,
                surname=surname,
                ssin=ssin
            )
    
    def verify_result(self, response: Any):
        signVerifResult = response.getSignatureVerificationResult()
        for entry in signVerifResult.getErrors():
            # Ignoring timestamp issues :( :(
            logger.error(f"Errors in {entry}")
            # self.GATEWAY.jvm.org.junit.Assert.assertTrue("Errors found in the signature verification",
            #     entry.getValue().isValid())
    
    def render_sender(self, practitioner: Practitioner):
        return Hcparty(
                    id=[
                        Id1(s="ID-HCPARTY", value=practitioner.nihii),
                        Id1(s="INSS", value=practitioner.ssin),                        
                    ],
                    cd=Cd(s="CD-HCPARTY", sv="1.16", value="persphysiotherapist"),
                    firstname=practitioner.givenname,
                    familyname=practitioner.surname
                )
    
    def render_request(self, practitioner: Practitioner, now: datetime.datetime):
        n14 = datetime.datetime.now().isoformat().replace('-', '').replace(':', '').replace('T', '').replace('.', '')[2:16]
        return Request(
            id=Id2(value=f"{practitioner.nihii}.{n14}", sv="1.0"),
            author=Author2(hcparty=self.render_sender(practitioner)),
            date=XmlDate.from_date(now),
            time=XmlTime.from_time(now),
        )
    
    def render_transaction(self, transaction: TransactionIn, practitioner: Practitioner, now: datetime.datetime):
        transaction_seq = 1

        amount = round(sum([cgd.amount for cgd in transaction.cgds]), 2)

        items = [
                Item(
                    id=Id1(s="ID-KMEHR", sv="1.0", value=1),
                    cd=Cd(s="CD-ITEM-MYCARENET", sv="1.4", value="patientpaid"),
                    cost=Cost(decimal="{:.2f}".format(amount))
                ),
                Item(
                    id=Id1(s="ID-KMEHR", sv="1.0", value=2),
                    cd=Cd(s="CD-ITEM-MYCARENET", sv="1.4", value="paymentreceivingparty"),
                    content=[Content(
                        id=Id1(s="ID-CBE", sv="1.0", value=transaction.kbo_number)
                    )]
                )
            ]
        
        # handle cga supplement
        supplements = [cgd.supplement for cgd in transaction.cgds if cgd.supplement]
        if len(supplements) > 0:
                items.append(
                    Item(
                        id=Id1(s="ID-KMEHR", sv="1.0", value=2),
                        cd=Cd(s="CD-ITEM-MYCARENET", sv="1.11", value="supplement"),
                        cost=Cost(decimal="{:.2f}".format(sum(supplements)))
                    ),
                )        

        cga = Transaction(
            id=Id1(s="ID-KMEHR", sv="1.0", value=transaction_seq),
            cd=Cd(sv="1.4", s="CD-TRANSACTION-MYCARENET", value="cga"),
            author=Author1(hcparty=self.render_sender(practitioner)),
            date=XmlDate.from_date(now),
            time=XmlTime.from_time(now),
            iscomplete=True,
            isvalidated=True,
            item=items
            )

        transactions = [cga]

        for cgd in transaction.cgds:
            items = [
                    Item(
                        id=Id1(s="ID-KMEHR", sv="1.0", value=1),
                        cd=Cd(s="CD-ITEM", sv="1.11", value="claim"),
                        content=[
                            Content(
                                cd=Cd(s="CD-NIHDI", sv="1.0", value=cgd.claim)
                            ),
                            Content(
                                cd=Cd(s="LOCAL", sl="NIHDI-CLAIM-NORM", sv="1.0", value=cgd.claim_norm)
                            ),
                            # Content(
                            #     cd=Cd(s="CD-NIHDI-RELATEDSERVICE", sv="1.0", value=transaction.relatedservice)
                            # ),
                        ],
                        quantity=Quantity(decimal=1)
                    ),
                    Item(
                        id=Id1(s="ID-KMEHR", sv="1.0", value=2),
                        cd=Cd(s="CD-ITEM", sv="1.11", value="encounterdatetime"),
                        content=[
                            Content(
                                date=XmlDate.from_date(cgd.encounterdatetime)
                            ),
                        ],
                    ),
                    Item(
                        id=Id1(s="ID-KMEHR", sv="1.0", value=3),
                        cd=Cd(s="CD-ITEM-MYCARENET", sv="1.6", value="patientpaid"),
                        cost=Cost(decimal="{:.2f}".format(cgd.amount))
                    ),
                    Item(
                        id=Id1(s="ID-KMEHR", sv="1.0", value=4),
                        cd=Cd(s="CD-ITEM-MYCARENET", sv="1.6", value="decisionreference"),
                        content=[Content(
                            id=Id1(s="LOCAL", sl="OAreferencesystemname", sv="1.0", value=cgd.decisionreference)
                        )]
                    ),
                ]
            if cgd.location:
                location_content = [
                            Content(
                                hcparty=Hcparty(
                                    id=[
                                        Id1(s="ID-HCPARTY", value=cgd.location.nihii),
                                        
                                    ],
                                    cd=Cd(s="CD-HCPARTY", sv="1.16", value=cgd.location.code_hc), # TODO
                                ),
                            )
                        ]
                if cgd.location.dienstcode:
                    location_content.append(
                        Content(
                            cd=Cd(s="LOCAL", sl="NIHDI-SERVICE-CD", sv="1.0", value=cgd.location.dienstcode),
                        )
                    )

                items.append(
                    Item(
                        id=Id1(s="ID-KMEHR", sv="1.0", value=3),
                        cd=Cd(s="CD-ITEM", sv="1.11", value="encounterlocation"),
                        content=location_content,
                    )
                )

            if cgd.supplement:
                items.append(
                    Item(
                        id=Id1(s="ID-KMEHR", sv="1.0", value=2),
                        cd=Cd(s="CD-ITEM-MYCARENET", sv="1.11", value="supplement"),
                        cost=Cost(decimal="{:.2f}".format(cgd.supplement))
                    ),
                )

            if cgd.requestor:
                items.append(
                    Item(
                        id=Id1(s="ID-KMEHR", sv="1.0", value=2),
                        cd=Cd(s="CD-ITEM", sv="1.11", value="requestor"),
                        content=[
                            Content(
                                cd=Cd(s="LOCAL", sl="NIHDI-REQUESTOR-NORM", sv="1.0", value=cgd.requestor.norm)
                            ),
                            Content(
                                hcparty=Hcparty(
                                    id=[
                                        Id1(s="ID-HCPARTY", value=cgd.requestor.nihii),
                                    ],
                                    cd=Cd(s="CD-HCPARTY", sv="1.16", value="persphysician"), # TODO
                                    firstname=cgd.requestor.givenname,
                                    familyname=cgd.requestor.surname,
                                ),
                            ),
                            Content(
                                date=XmlDate.from_date(cgd.requestor.date_prescription)
                            )
                        ],
                    )
                )
            transaction_seq += 1
            cgd = Transaction(
                id=Id1(s="ID-KMEHR", sv="1.0", value=transaction_seq),
                cd=Cd(sv="1.4", s="CD-TRANSACTION-MYCARENET", value="cgd"),
                author=Author1(hcparty=self.render_sender(practitioner)),
                date=XmlDate.from_date(now),
                time=XmlTime.from_time(now),
                iscomplete=True,
                isvalidated=True,
                item=items
            )

            transactions.append(cgd)
        return transactions
    
    def render_patient(self, patient: PatientIn):
        if patient.ssin:
            insurance_membership = None
        else:
            insurance_membership = Insurancymembership(
                id=Id1(s="ID-INSURANCE", sv="1.0", value=patient.insurance_io),
                membership=patient.insurance_number
            )
        return Patient(
            id=Id1(s="ID-PATIENT", sv="1.0", value=patient.ssin or ""),
            firstname=patient.givenname,
            familyname=patient.surname,
            # NOT IMPLEMENTED, OPTIONAL
            # birthdate=patient.birth_date.isoformat(),
            sex=Sex(cd=Cd(s="CD-SEX", sv="1.1", value=patient.gender)),
            insurancymembership=insurance_membership
        )

    def render_message(self, practitioner: Practitioner, now: datetime.datetime, input_model: EAttestInputModel):
        return Kmehrmessage(
            header=Header(
                id=Id1(s="ID-KMEHR", sv="1.0", value=1),
                date=XmlDate.from_date(now),
                time=XmlTime.from_time(now),
                sender=Sender(hcparty=self.render_sender(practitioner)),
                recipient=Recipient(hcparty=Hcparty(
                    cd=Cd(s="CD-HCPARTY", sv="1.14", value="application"),
                    name="mycarenet"
                ))
            ),
            # NOTE: folder should actually be a list
            folder=Folder(
                id=Id1(s="ID-KMEHR", sv="1.0", value="1"),
                patient=self.render_patient(input_model.patient),
                # NOTE: there could be multiple attestations in a single request?
                transaction=self.render_transaction(input_model.transaction, practitioner, now)
            )
        )

    def render_cancel_transaction(self, invoice_number: str, reason: str, practitioner: Practitioner, now: datetime.datetime):
        transaction_seq = 1

        items = [
                Item(
                    id=Id1(s="ID-KMEHR", sv="1.0", value=1),
                    cd=Cd(s="CD-ITEM-MYCARENET", sv="1.64", value="invoicingnumber"),
                    content=[
                        Content(text=Text(value=invoice_number)),
                        Content(
                            cd=Cd(s="LOCAL", sl="NIHDI-CANCELLATION-REASON", sv="1.0", value=reason)
                        )
                    ]
                ),
            ]     

        cga = Transaction(
            id=Id1(s="ID-KMEHR", sv="1.0", value=transaction_seq),
            cd=Cd(sv="1.54", s="CD-TRANSACTION-MYCARENET", value="cgacancellation"),
            author=Author1(hcparty=self.render_sender(practitioner)),
            date=XmlDate.from_date(now),
            time=XmlTime.from_time(now),
            iscomplete=True,
            isvalidated=True,
            item=items
            )

        transactions = [cga]
        return transactions
    
    def render_cancel_message(self, practitioner: Practitioner, now: datetime.datetime, input_model: CancelEAttestInputModel):
        return Kmehrmessage(
            header=Header(
                id=Id1(s="ID-KMEHR", sv="1.0", value=1),
                date=XmlDate.from_date(now),
                time=XmlTime.from_time(now),
                sender=Sender(hcparty=self.render_sender(practitioner)),
                recipient=Recipient(hcparty=Hcparty(
                    cd=Cd(s="CD-HCPARTY", sv="1.14", value="application"),
                    name="mycarenet"
                ))
            ),
            folder=Folder(
                id=Id1(s="ID-KMEHR", sv="1.0", value="1"),
                patient=self.render_patient(input_model.patient),
                # NOTE: there could be multiple attestations in a single request?
                transaction=self.render_cancel_transaction(input_model.invoice_number, input_model.reason, practitioner, now)
            )
        )
    
    @classmethod
    def serialize_template(cls, bundle: BaseModel):
        serializer = XmlSerializer()
        serializer.config.pretty_print = True
        # serializer.config.xml_declaration = True
        ns_map = {
            # "" : "",
            "xmlns": "http://www.ehealth.fgov.be/messageservices/protocol/v1",
            "msgws": "http://www.ehealth.fgov.be/messageservices/core/v1",
            "kmehr": "http://www.ehealth.fgov.be/standards/kmehr/schema/v1"
        }
        return serializer.render(bundle, ns_map)
    
    def handle_send_attestation_response(self, attestBuilder: Any, template: str, raw_request: str, sendAttestationResponse: Any, meta: CallMetadata, callback_fn: Optional[Callable] = storage_callback) -> EAttestV3:
        raw_response = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(sendAttestationResponse)
        callback_fn(raw_response, meta.set_call_type(CallType.ENCRYPTED_RESPONSE))

        attestResponse = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.attestv3.builders.ResponseObjectBuilderFactory.getResponseObjectBuilder().handleSendAttestionResponse(sendAttestationResponse, attestBuilder)
        self.verify_result(attestResponse)
        response_string = self.GATEWAY.jvm.java.lang.String(attestResponse.getBusinessResponse(), "UTF-8")
        callback_fn(response_string, meta.set_call_type(CallType.UNENCRYPTED_RESPONSE))
        xades_response_string = self.GATEWAY.jvm.java.lang.String(attestResponse.getXadesT(), "UTF-8")
        callback_fn(xades_response_string, meta.set_call_type(CallType.XADES_RESPONSE))

        parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
        response_pydantic = parser.parse(StringIO(response_string), SendTransactionResponse)
        
        return EAttestV3(
            response=response_pydantic,
            transaction_request=template,
            transaction_response=response_string.replace('ns:', ''),
            soap_request=raw_request,
            soap_response=raw_response
        )
    
    def send_attestation(self, token: str, input_model: EAttestInputModel,
                         callback_fn: Optional[Callable] = storage_callback):
        timestamp = datetime.datetime.now()
        meta = CallMetadata(
            type=ServiceType.EATTEST,
            timestamp=timestamp,
            call_type=CallType.UNENCRYPTED_REQUEST,
            ssin=input_model.patient.ssin,
            registrationNumber=input_model.patient.insurance_number,
            mutuality=input_model.patient.insurance_io,
        )

        now = datetime.datetime.now(pytz.timezone("Europe/Brussels"))
        practitioner = self.set_configuration_from_token(token)
        kmehrmessage_pydantic = SendTransactionRequest(
            request=self.render_request(practitioner, now),
            kmehrmessage=self.render_message(practitioner, now, input_model)
        )
        template = self.serialize_template(kmehrmessage_pydantic).replace('xmlns:xmlns="http://www.ehealth.fgov.be/messageservices/protocol/v1"', 'xmlns="http://www.ehealth.fgov.be/messageservices/protocol/v1"')
        callback_fn(template, meta)

        # obviously this is lazy ...
        with tempfile.NamedTemporaryFile(suffix='.xml', mode='w', delete=False) as tmp:
            tmp.write(template)

        input_reference_str = kmehrmessage_pydantic.request.id.value.split('.')[1]
        inputReference = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.domain.InputReference(input_reference_str)

        if input_model.patient.ssin:
            ssin = input_model.patient.ssin
        else:
            raise Exception("eAttest ondersteunt registratienummer niet")
        
        send_attest_request = (self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.attestv3.builders.SendAttestationRequestInput
                               .builder()
                               .isTest(self.is_test)
                               .inputReference(inputReference)
                               .kmehrmessage(self.EHEALTH_JVM.getBytesFromFile(tmp.name))
                                .patientSsin(self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.domain.Ssin(ssin))
                                .referenceDate(self.GATEWAY.jvm.java.time.LocalDateTime.now())
                                .messageVersion("3.0")
                                .issuer("some issuer")
                                .commonInputAttributes(self.EHEALTH_JVM.commonInputAttributes(1)) # TODO probably also needs some updates still
                                .build())       
        attestBuilder = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.attestv3.builders.RequestObjectBuilderFactory.getRequestObjectBuilder().buildSendAttestationRequest(
            send_attest_request
        )
        attestBuilderRequest = attestBuilder.getSendAttestationRequest()
        
        raw_request = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(attestBuilderRequest)
        callback_fn(raw_request, meta.set_call_type(CallType.ENCRYPTED_REQUEST))

        try:
            sendAttestationResponse = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.attestv3.session.AttestSessionServiceFactory.getAttestService().sendAttestation(attestBuilderRequest)
            if input_model.force_retryable:
                raise Exception("Force technical exception to test Duplicate service")
        except Exception as e:
            retryable = EAttestRetryableAttempt(
                input_reference_str=input_reference_str,
                template=template,
                ssin=ssin,
                attemptNumber=1
            )
            raise TechnicalEAttestException(
                message=str(e),
                retryable=retryable
            )
        
        return self.handle_send_attestation_response(
            attestBuilder=attestBuilder,
            template=template,
            raw_request=raw_request,
            sendAttestationResponse=sendAttestationResponse,
            meta=meta,
            callback_fn=callback_fn
            )
    
    def retry_send_attestation(self, token: str, input_model: EAttestRetryableAttempt,
                         callback_fn: Optional[Callable] = storage_callback):
        # increment attempt number
        input_model.attemptNumber += 1

        timestamp = datetime.datetime.now()
        meta = CallMetadata(
            type=ServiceType.EATTEST,
            timestamp=timestamp,
            call_type=CallType.UNENCRYPTED_REQUEST,
            ssin=input_model.ssin,
            registrationNumber=None,
            mutuality=None,
        )
            
        # obviously this is lazy ...
        with tempfile.NamedTemporaryFile(suffix='.xml', mode='w', delete=False) as tmp:
            tmp.write(input_model.template)

        inputReference = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.domain.InputReference(input_model.input_reference_str)
        
        send_attest_request = (self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.attestv3.builders.SendAttestationRequestInput
                               .builder()
                               .isTest(self.is_test)
                               .inputReference(inputReference)
                               .kmehrmessage(self.EHEALTH_JVM.getBytesFromFile(tmp.name))
                                .patientSsin(self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.domain.Ssin(input_model.ssin))
                                .referenceDate(self.GATEWAY.jvm.java.time.LocalDateTime.now())
                                .messageVersion("3.0")
                                .issuer("some issuer")
                                .commonInputAttributes(self.EHEALTH_JVM.commonInputAttributes(input_model.attemptNumber)) # TODO probably also needs some updates still
                                .build())       
        attestBuilder = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.attestv3.builders.RequestObjectBuilderFactory.getRequestObjectBuilder().buildSendAttestationRequest(
            send_attest_request
        )
        
        attestBuilderRequest = attestBuilder.getSendAttestationRequest()
        
        raw_request = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(attestBuilderRequest)
        callback_fn(raw_request, meta.set_call_type(CallType.ENCRYPTED_REQUEST))

        try:
            sendAttestationResponse = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.attestv3.session.AttestSessionServiceFactory.getAttestService().sendAttestation(attestBuilderRequest)
        except Exception as e:
            raise TechnicalEAttestException(
                message=str(e),
                retryable=input_model
            )
        
        return self.handle_send_attestation_response(
            attestBuilder=attestBuilder,
            template=input_model.template,
            raw_request=raw_request,
            sendAttestationResponse=sendAttestationResponse,
            meta=meta,
            callback_fn=callback_fn
            )


    def cancel_attestation(self, token: str, input_model: CancelEAttestInputModel,
                           callback_fn: Optional[Callable] = storage_callback):
        timestamp = datetime.datetime.now()
        meta = CallMetadata(
            type=ServiceType.CANCEL_EATTEST,
            timestamp=timestamp,
            call_type=CallType.UNENCRYPTED_REQUEST,
            ssin=input_model.patient.ssin,
            registrationNumber=input_model.patient.insurance_number,
            mutuality=input_model.patient.insurance_io,
        )

        now = datetime.datetime.now().replace(microsecond=0)
        practitioner = self.set_configuration_from_token(token)
        kmehrmessage_pydantic = SendTransactionRequest(
            request=self.render_request(practitioner, now),
            kmehrmessage=self.render_cancel_message(practitioner, now, input_model)
        )
        template = self.serialize_template(kmehrmessage_pydantic).replace('xmlns:xmlns="http://www.ehealth.fgov.be/messageservices/protocol/v1"', 'xmlns="http://www.ehealth.fgov.be/messageservices/protocol/v1"')
        callback_fn(template, meta)
        
        # obviously this is lazy ...
        with tempfile.NamedTemporaryFile(suffix='.xml', mode='w', delete=False) as tmp:
            tmp.write(template)

        input_reference_str = kmehrmessage_pydantic.request.id.value.split('.')[1]
        inputReference = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.domain.InputReference(input_reference_str)

        send_cancel_attest_request = (self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.attestv3.builders.CancelAttestationRequestInput
                               .builder()
                               .isTest(self.is_test)
                               .inputReference(inputReference)
                               .kmehrmessage(self.EHEALTH_JVM.getBytesFromFile(tmp.name))
                                .messageVersion("3.0")
                                .issuer("some issuer")
                                .commonInputAttributes(self.EHEALTH_JVM.commonInputAttributes(1)) # TODO probably also needs some updates still
                                .build())       


        cancelAttestationRequest = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.attestv3.builders.RequestObjectBuilderFactory.getRequestObjectBuilder().buildCancelAttestationRequest(
            send_cancel_attest_request
        )
        raw_request = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(cancelAttestationRequest)
        callback_fn(raw_request, meta.set_call_type(CallType.ENCRYPTED_REQUEST))
        
        try:
            cancelAttestationResponse = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.attestv3.session.AttestSessionServiceFactory.getAttestService().cancelAttestation(cancelAttestationRequest)
            if input_model.force_retryable:
                raise Exception("Force technical exception to test Duplicate service")
        except Exception as e:
            retryable = EAttestRetryableAttempt(
                input_reference_str=input_reference_str,
                template=template,
                ssin=input_model.patient.ssin,
                attemptNumber=1
            )
            raise TechnicalEAttestException(
                message=str(e),
                retryable=retryable
            )


        raw_response = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(cancelAttestationResponse)
        callback_fn(raw_response, meta.set_call_type(CallType.ENCRYPTED_RESPONSE))

        attestResponse = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.attestv3.builders.ResponseObjectBuilderFactory.getResponseObjectBuilder().handleCancelAttestationResponse(cancelAttestationResponse, cancelAttestationRequest)
        self.verify_result(attestResponse)
        response_string = self.GATEWAY.jvm.java.lang.String(attestResponse.getBusinessResponse(), "UTF-8")
        callback_fn(response_string, meta.set_call_type(CallType.UNENCRYPTED_RESPONSE))
        xades_response_string = self.GATEWAY.jvm.java.lang.String(attestResponse.getXadesT(), "UTF-8")
        callback_fn(xades_response_string, meta.set_call_type(CallType.XADES_RESPONSE))

        parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
        response_pydantic = parser.parse(StringIO(response_string), SendTransactionResponse)
        
        return EAttestV3(
            response=response_pydantic,
            transaction_request=template,
            transaction_response=response_string.replace('ns:', ''),
            soap_request=raw_request,
            soap_response=raw_response
        )

    def retry_cancel_attestation(self, token: str, input_model: EAttestRetryableAttempt,
                           callback_fn: Optional[Callable] = storage_callback):
        # increment attempt number
        input_model.attemptNumber += 1

        self.set_configuration_from_token(token)

        timestamp = datetime.datetime.now()
        meta = CallMetadata(
            type=ServiceType.CANCEL_EATTEST,
            timestamp=timestamp,
            call_type=CallType.UNENCRYPTED_REQUEST,
            ssin=input_model.ssin,
            registrationNumber=None,
            mutuality=None
        )

        callback_fn(input_model.template, meta)
        
        # obviously this is lazy ...
        with tempfile.NamedTemporaryFile(suffix='.xml', mode='w', delete=False) as tmp:
            tmp.write(input_model.template)

        inputReference = self.GATEWAY.jvm.be.ehealth.business.mycarenetdomaincommons.domain.InputReference(input_model.input_reference_str)

        send_cancel_attest_request = (self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.attestv3.builders.CancelAttestationRequestInput
                               .builder()
                               .isTest(self.is_test)
                               .inputReference(inputReference)
                               .kmehrmessage(self.EHEALTH_JVM.getBytesFromFile(tmp.name))
                                .messageVersion("3.0")
                                .issuer("some issuer")
                                .commonInputAttributes(self.EHEALTH_JVM.commonInputAttributes(input_model.attemptNumber)) # TODO probably also needs some updates still
                                .build())       
        
        cancelAttestationRequest = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.attestv3.builders.RequestObjectBuilderFactory.getRequestObjectBuilder().buildCancelAttestationRequest(
            send_cancel_attest_request
        )
        
        raw_request = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(cancelAttestationRequest)
        callback_fn(raw_request, meta.set_call_type(CallType.ENCRYPTED_REQUEST))
                
        try:
            cancelAttestationResponse = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.attestv3.session.AttestSessionServiceFactory.getAttestService().cancelAttestation(cancelAttestationRequest)
        except Exception as e:
            raise TechnicalEAttestException(
                message=str(e),
                retryable=input_model
            )


        raw_response = self.GATEWAY.jvm.be.ehealth.technicalconnector.utils.ConnectorXmlUtils.toString(cancelAttestationResponse)
        callback_fn(raw_response, meta.set_call_type(CallType.ENCRYPTED_RESPONSE))

        attestResponse = self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.attestv3.builders.ResponseObjectBuilderFactory.getResponseObjectBuilder().handleCancelAttestationResponse(cancelAttestationResponse, cancelAttestationRequest)
        self.verify_result(attestResponse)
        response_string = self.GATEWAY.jvm.java.lang.String(attestResponse.getBusinessResponse(), "UTF-8")
        callback_fn(response_string, meta.set_call_type(CallType.UNENCRYPTED_RESPONSE))
        xades_response_string = self.GATEWAY.jvm.java.lang.String(attestResponse.getXadesT(), "UTF-8")
        callback_fn(xades_response_string, meta.set_call_type(CallType.XADES_RESPONSE))

        parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
        response_pydantic = parser.parse(StringIO(response_string), SendTransactionResponse)
        
        return EAttestV3(
            response=response_pydantic,
            transaction_request=input_model.template,
            transaction_response=response_string.replace('ns:', ''),
            soap_request=raw_request,
            soap_response=raw_response
        )
