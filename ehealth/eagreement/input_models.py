from pydantic import BaseModel
from typing import Optional, Any, List
import datetime

class Practitioner(BaseModel):
    nihii: str
    givenname: str
    surname: str

class Patient(BaseModel):
    ssin: str
    givenname: str
    surname: str
    gender: str

class Prescription(BaseModel):
    # TODO wip eg. prescription number
    data_base64: str
    data_mimetype: Optional[str] = "application/pdf"
    snomed_category: int
    snomed_code: int
    date: datetime.date
    quantity: int

class Attachment(BaseModel):
    data_base64: str
    mimetype: Optional[str] = "application/pdf"
    type: str
    title: str

class ClaimAsk(BaseModel):
    transaction: Optional[str] = "claim-ask"
    product_or_service: str
    billable_period: datetime.date
    serviced_date: datetime.date
    prescription: Optional[Prescription] = None # modeling TODO
    pre_auth_ref: Optional[str] = None # in case of extend
    attachments: Optional[List[Attachment]] = []

class AskAgreementInputModel(BaseModel):
    patient: Patient
    physician: Practitioner
    claim: ClaimAsk