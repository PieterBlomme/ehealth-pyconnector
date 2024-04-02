from pydantic import BaseModel
from typing import Optional, Union, List
import datetime

class Practitioner(BaseModel):
    nihii: str
    givenname: str
    surname: str

class Patient(BaseModel):
    ssin: Optional[str]
    insurancymembership: Optional[str]
    insurancenumber: Optional[str]
    givenname: str
    surname: str
    gender: str

class Prescription(BaseModel):
    data_base64: Optional[str]
    data_mimetype: Optional[str] = "application/pdf"
    # TODO wip eg. prescription number
    snomed_category: int
    snomed_code: int
    identifier: Optional[str]
    date: Optional[datetime.date]
    quantity: Optional[int]

class Attachment(BaseModel):
    data_base64: str
    mimetype: Optional[str] = "application/pdf"
    type: str
    title: str

class ClaimAsk(BaseModel):
    transaction: Optional[str] = "claim-ask"
    product_or_service: str
    sub_type: Optional[str] = None
    billable_period: Optional[datetime.date]
    serviced_date: Optional[datetime.date]
    prescription: Optional[Prescription] = None # modeling TODO
    previous_prescription: Optional[Prescription] = None # modeling TODO
    pre_auth_ref: Optional[str] = None # in case of extend
    attachments: Optional[List[Attachment]] = []
    supporting_infos: Optional[List[str]] = []

class AskAgreementInputModel(BaseModel):
    patient: Patient
    physician: Optional[Practitioner]
    claim: ClaimAsk
    io_routing: Optional[bool] = False