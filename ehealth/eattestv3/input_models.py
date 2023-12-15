from pydantic import BaseModel
from typing import Optional, Union, List
import datetime

class Practitioner(BaseModel):
    nihii: str
    givenname: str
    surname: str
    ssin: Optional[str] = None

class Patient(BaseModel):
    givenname: str
    surname: str
    gender: str
    # birth_date: datetime.date
    ssin: Optional[str]
    insurance_io: Optional[str]
    insurance_number: Optional[str]

class CGDItem(BaseModel):
    claim: str
    decisionreference: str
    encounterdatetime: datetime.date
    amount: float
    requestor: Practitioner

class Transaction(BaseModel):
    bank_account: str
    relatedservice: Optional[str]
    cgds: List[CGDItem]

class EAttestInputModel(BaseModel):
    patient: Patient
    transaction: Transaction