import logging
from io import StringIO
from typing import Any, Callable, List, Tuple, Union, Dict
from xsdata_pydantic.bindings import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from .input_models import Patient, AskAgreementInputModel
from .ask_agreement import Bundle as AskResponseBundle, Response as AskResponse
from .consult_agreement import Bundle as ConsultResponseBundle, Response as ConsultResponse
from .eagreement_base import AbstractEAgreementService

logger = logging.getLogger(__name__)

class FakeEAgreementService(AbstractEAgreementService):
    def __init__(
            self,
            faked: List[
                Tuple[Union[AskAgreementInputModel, Patient], Dict[str, List[str]], str]
                ], # (input, state, output)
            environment: str = "acc",
    ):
        super().__init__(environment=environment)
        self.faked = faked
        self._state = {}
    
    def set_state(self, ssin: str, state: Dict[str, List[str]]):
        self._state[ssin] = state

    def get_response_builder(self):
        return self.GATEWAY.jvm.be.ehealth.businessconnector.mycarenet.agreement.builders.ResponseObjectBuilderFactory.getResponseObjectBuilder()

    def convert_response_to_pydantic(self, response_string: str, target_class: Callable):
        parser = XmlParser(ParserConfig(fail_on_unknown_properties=False))
        try:
            return parser.parse(StringIO(response_string), target_class)  
        except:
            logger.error(response_string)
            raise
    
    def ask_agreement(
        self, 
        token: str,
        input_model: AskAgreementInputModel
        ) -> str:
        practitioner = self.set_configuration_from_token(token)
        template, id_ = self.render_ask_or_extend_agreement_bundle(
            practitioner=practitioner,
            input_model=input_model
        )

        patient_state = self._state.get(input_model.patient.ssin, {})

        for model, state, response_string in self.faked:
            if model == input_model.json() and state == patient_state:

                response_pydantic = self.convert_response_to_pydantic(response_string, AskResponseBundle)

                # TODO if response is agreement, update state

                return AskResponse(
                    response=response_pydantic,
                    transaction_request=template,
                    transaction_response=response_string,
                    soap_request="", # too much effort
                    soap_response="" # too much effort
                )
        raise NotImplementedError(f"Could not fake {input_model}")

    def consult_agreement(
        self, 
        token: str,
        input_model: Patient
        ) -> str:
        practitioner = self.set_configuration_from_token(token)
        template, id_ = self.render_consult_agreement_bundle(
            practitioner=practitioner,
            input_model=input_model
        )
        patient_state = self._state.get(input_model.ssin, {})

        for model, state, response_string in self.faked:
            if model == input_model.json() and state == patient_state:

                response_pydantic = self.convert_response_to_pydantic(response_string, ConsultResponseBundle)

                # TODO if response is agreement, update state

                return ConsultResponse(
                    response=response_pydantic,
                    transaction_request=template,
                    transaction_response=response_string,
                    soap_request="", # too much effort
                    soap_response="" # too much effort
                )
        raise NotImplementedError(f"Could not fake {input_model}")