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

class UnsealException(Exception):
    """Exception raised when decryption fails during handleSendAttestionResponse.
    
    This exception captures the encrypted request and response data to allow
    for later retry via decrypt_send_attestation_response.
    """
    def __init__(
        self,
        message: str,
        encrypted_response: str,
        encrypted_request: str,
        input_reference_str: str,
        ssin: str,
    ):
        super().__init__(message)
        self.encrypted_response = encrypted_response
        self.encrypted_request = encrypted_request
        self.input_reference_str = input_reference_str
        self.ssin = ssin