from pydantic import BaseModel
from typing import Optional, List
import datetime

class Practitioner(BaseModel):
    nihii: str
    givenname: str
    surname: str
    ssin: Optional[str] = None

class Requestor(Practitioner):
    date_prescription: datetime.date
    norm: Optional[int] = 1

class Patient(BaseModel):
    givenname: str
    surname: str
    gender: str
    # birth_date: datetime.date
    ssin: Optional[str]
    insurance_io: Optional[str]
    insurance_number: Optional[str]

class Location(BaseModel):
    nihii: str
    code_hc: str
    dienstcode: Optional[str]

class CGDItem(BaseModel):
    claim: str
    claim_norm: Optional[int] = 0
    decisionreference: str
    encounterdatetime: datetime.date
    amount: float
    requestor: Requestor
    location: Optional[Location] = None
    supplement: Optional[float] = None

class Transaction(BaseModel):
    kbo_number: str
    relatedservice: Optional[str]
    cgds: List[CGDItem]

class EAttestInputModel(BaseModel):
    patient: Patient
    transaction: Transaction
