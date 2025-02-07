from pydantic import BaseModel

class EAttestRetryableAttempt(BaseModel):
    input_reference_str: str
    template: str
    ssin: str
    attemptNumber: int

class TechnicalEAttestException(Exception):
    def __init__(
        self,
        message: str,
        retryable: EAttestRetryableAttempt
    ):
        super().__init__(message)
        self.retryable = retryable