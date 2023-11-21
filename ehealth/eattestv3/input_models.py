from pydantic import BaseModel
from typing import Optional, Union, List
import datetime

class Practitioner(BaseModel):
    nihii: str
    givenname: str
    surname: str
    ssin: str

class Patient(BaseModel):
    givenname: str
    surname: str
    gender: str
    # birth_date: datetime.date
    ssin: Optional[str]
    insurance_io: Optional[str]
    insurance_number: Optional[str]

class Transaction(BaseModel):
    amount: float
    bank_account: str
    nihdi: str
    claim: str
    relatedservice: Optional[str]
    decisionreference: str
    encounterdatetime: datetime.date

class EAttestInputModel(BaseModel):
    patient: Patient
    transaction: Transaction