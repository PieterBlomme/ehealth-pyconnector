from pydantic import BaseModel
from typing import Optional, Union, List
import datetime

class Practitioner(BaseModel):
    nihii: str
    givenname: str
    surname: str