from pydantic import BaseModel

class Practitioner(BaseModel):
    nihii: str
    givenname: str
    surname: str

class Patient(BaseModel):
    ssin: str
    givenname: str
    surname: str
    gender: str

class AskAgreementInputModel(BaseModel):
    patient: Patient
    physician: Practitioner