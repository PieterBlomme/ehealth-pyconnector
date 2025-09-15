from pydantic import BaseModel
import datetime

class HealthCareParty(BaseModel):
    nihii: str
    inss: str
    type: str

class Patient(BaseModel):
    inss: str | None = None
    regNrWithMut: str | None = None
    mutuality:  str | None = None
    firstname: str
    lastname: str
    eidnumber: str | None = None
    isinumber: str | None = None
    sisCardNumber: str | None = None

class TherapeuticLink(BaseModel):
    start_date: datetime.date
    end_date: datetime.date
    type: str
    hcparty: HealthCareParty
    patient: Patient