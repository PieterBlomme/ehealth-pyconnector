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

class CGDItem(BaseModel):
    claim: str
    decisionreference: str
    encounterdatetime: datetime.date
    amount: float
    requestor: Requestor
    location: Optional[Location] = None
    supplement: Optional[float] = None

class Transaction(BaseModel):
    bank_account: str
    relatedservice: Optional[str]
    cgds: List[CGDItem]

class EAttestInputModel(BaseModel):
    patient: Patient
    transaction: Transaction