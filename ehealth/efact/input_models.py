from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
from .error_constants import ERROR_CONSTANTS
from pydantic import BaseModel
from pydantic import Extra

logger = logging.getLogger(__name__)

class ErrorMessage(BaseModel):
    key: str
    value: str
    error_code: str
    message: Optional[str] = None
    type: Optional[str] = None
    verwerpingsletter: Optional[str] = None

def calculate_control(text) -> str:
    assert len(text) == 348, len(text) # always?? to check
    control = 0

    CHARS = [
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        " ",
        "a", "b", "c", "d", "e", "f",
        "g", "h", "i", "j", "k", "l",
        "m", "n", "o", "p", "q", "r",
        "s", "t", "u", "v", "w", "x",
        "y", "z"
    ]
    for c in text:
        try:
            control_number = CHARS.index(c.lower())
        except ValueError:
            control_number = 37
        control += control_number

    # commented in production
    # looks like their testfiles are actually
    # invalid ...
    # control += 10 # missing blank??

    control = control % 97
    if control == 0:
        control = 97
    return str(control).rjust(2, "0")

def calculate_invoice_control(nomenclatures) -> str:
    total = [0,0,0,0,0,0,0,]
    for n in nomenclatures:
        assert len(n) == 7
        for i, c in enumerate(n):
            total[i] += int(c)

    print(total)
    # shift left if > 10
    for i in (6, 5, 4, 3, 2, 1):
        if total[i] > 9:
            remainder = total[i] % 10
            shift_left = int((total[i] - remainder) / 10)
            print(f"{i}: {remainder} {shift_left}")
            total[i] = remainder
            total[i-1] = total[i-1] + shift_left
    print(total)
    control = int("".join([str(e) for e in total]))
    control = control % 97
    if control == 0:
        control = 97
    return str(control).rjust(2, "0")

class Header200(BaseModel):
    name: Optional[str] = "920000"
    error_name: Optional[str] = "00"
    version: Optional[str] = "01"
    error_version: Optional[str] = "00"
    type: Optional[str] = "92" # 92 for test, 12 for prd
    error_type: Optional[str] = "00"
    status: Optional[str] = "00"
    error_status: Optional[str] = "00"
    reference: str
    error_reference: Optional[str] = "00"
    reference_io: Optional[str] = "0" * 14
    error_reference_io: Optional[str] = "00"

    def __str__(self):
        to_str = ""
        assert len(self.name) == 6
        to_str += self.name
        assert len(self.error_name) == 2
        to_str += self.error_name
        assert len(self.version) == 2
        to_str += self.version
        assert len(self.error_version) == 2
        to_str += self.error_version
        assert len(self.type) == 2
        to_str += self.type
        assert len(self.error_type) == 2
        to_str += self.error_type
        assert len(self.status) == 2
        to_str += self.status
        assert len(self.error_status) == 2
        to_str += self.error_status
        assert len(self.reference) == 14
        to_str += self.reference
        assert len(self.error_reference) == 2
        to_str += self.error_reference
        assert len(self.reference_io) == 14
        to_str += self.reference_io
        assert len(self.error_reference_io) == 2
        to_str += self.error_reference_io

        reserve = "0" * 15
        to_str += reserve
        return to_str

    @classmethod
    def from_str(cls, msg: str) -> "Header200":
        assert len(msg) == 67
        return Header200(
            name = msg[:6],
            error_name = msg[6:8],
            version = msg[8:10],
            error_version = msg[10:12],
            type = msg[12:14],
            error_type = msg[14:16],
            status = msg[16:18],
            error_status = msg[18:20],
            reference = msg[20:34],
            error_reference = msg[34:36],
            reference_io = msg[36:50],
            error_reference_io = msg[50:52],
        )
    
    def _error_shared(self, key, error, value) -> Optional[Dict[str, Any]]:
        if error == "00":
            return None
        
        return {
            "type": self.name,
            "key": key,
            "value": value,
            "error_code": error,
            "message": ERROR_CONSTANTS.get(error)
        }

    def _error_name(self) -> Optional[Dict[str, Any]]:
        error = self.error_name
        value = self.name
        error_dict = self._error_shared("naam", error, value)

        if error_dict is None or error_dict.get("message") is not None:
            return error_dict
        
        msg = ""
        if error == "20":
            msg = "Codificatie onbekend"
        elif error == "21":
            msg = "Bericht niet toegelaten voor deze uitgever"
        elif error == "22":
            msg = "# van 920000"
        error_dict["message"] = msg
        return error_dict

    def _error_version(self) -> Optional[Dict[str, Any]]:
        error = self.error_version
        value = self.version
        error_dict = self._error_shared("versie", error, value)

        if error_dict is None or (error_dict.get("message") is not None and error_dict.get("message") != "20"):
            return error_dict
        
        msg = ""
        if error == "20":
            msg = "Nr. van de versie is niet meer van toepassing"
        elif error == "21":
            msg = "Nr. van de versie is nog niet van toepassing"
        elif error == "30":
            msg = "Nr. versie niet toegelaten voor deze stroom"
        error_dict["message"] = msg
        return error_dict

    def _error_type(self) -> Optional[Dict[str, Any]]:
        error = self.error_type
        value = self.type
        error_dict = self._error_shared("type", error, value)

        if error_dict is None or error_dict.get("message") is not None:
            return error_dict
        
        msg = ""
        if error == "30":
            msg = "Testbericht in een productie-buffer (1ste karakter zone 107 = P)"
        elif error == "31":
            msg = "Bericht van productie in een test-buffer (1ste karakter zone 107 = T)"
        error_dict["message"] = msg
        return error_dict

    def _error_status(self) -> Optional[Dict[str, Any]]:
        error = self.error_status
        value = self.status
        error_dict = self._error_shared("status", error, value)

        return error_dict

    def _error_reference(self) -> Optional[Dict[str, Any]]:
        error = self.error_reference
        value = self.reference
        return self._error_shared("referentie", error, value)

    def _error_reference_io(self) -> Optional[Dict[str, Any]]:
        error = self.error_reference_io
        value = self.reference_io
        return self._error_shared("referentie VI", error, value)
    
    def errors(self) -> List[Dict[str, Any]]:
        errors = [
            self._error_name(),
            self._error_version(),
            self._error_type(),
            self._error_status(),
            self._error_reference(),
            self._error_reference_io()
        ]
        return [ErrorMessage(**e) for e in errors if e is not None]



class Header300(BaseModel):
    year_and_month: str
    error_year_and_month: Optional[str] = "00"
    num_invoice: str
    error_num_invoice: Optional[str] = "00"
    date_invoice: str
    error_date_invoice: Optional[str] = "00"
    reference_invoice: Optional[str] = " " * 13
    error_reference_invoice: Optional[str] = "00"
    version_instructions: Optional[str] = "9991999" # 9991999 for test, 0001999 for prd
    error_version_instructions: Optional[str] = "00"
    name_contact: str
    error_name_contact: Optional[str] = "00"
    first_name_contact: str
    error_first_name_contact: Optional[str] = "00"
    tel_contact: str
    error_tel_contact: Optional[str] = "00"
    type_invoice: str
    error_type_invoice: Optional[str] = "00"
    type_invoicing: str
    error_type_invoicing: Optional[str] = "00"

    @classmethod
    def from_str(cls, msg: str) -> "Header300":
        assert len(msg) == 227-67
        return Header300(
            year_and_month = msg[:6],
            error_year_and_month = msg[6:8],
            num_invoice = msg[8:11],
            error_num_invoice = msg[11:13],
            date_invoice = msg[13:21],
            error_date_invoice = msg[21:23],
            reference_invoice = msg[23:36],
            error_reference_invoice = msg[36:38],
            version_instructions = msg[38:45],
            error_version_instructions = msg[45:47],
            name_contact = msg[47:92],
            error_name_contact = msg[92:94],
            first_name_contact = msg[94:118],
            error_first_name_contact = msg[118:120],
            tel_contact = msg[120:130],
            error_tel_contact = msg[130:132],
            type_invoice = msg[132:134],
            error_type_invoice = msg[134:136],
            type_invoicing = msg[136:138],
            error_type_invoicing = msg[138:140],
        )
    
    def __str__(self):
        to_str = ""
        assert len(self.year_and_month) == 6
        to_str += self.year_and_month
        assert len(self.error_year_and_month) == 2
        to_str += self.error_year_and_month
        assert len(self.num_invoice) == 3
        to_str += self.num_invoice
        assert len(self.error_num_invoice) == 2
        to_str += self.error_num_invoice
        assert len(self.date_invoice) == 8
        to_str += self.date_invoice
        assert len(self.error_date_invoice) == 2
        to_str += self.error_date_invoice
        assert len(self.reference_invoice) == 13
        to_str += self.reference_invoice
        assert len(self.error_reference_invoice) == 2
        to_str += self.error_reference_invoice
        assert len(self.version_instructions) == 7
        to_str += self.version_instructions
        assert len(self.error_version_instructions) == 2
        to_str += self.error_version_instructions

        # pad name to 45 characters
        to_str += self.name_contact.ljust(45)
        assert len(self.error_name_contact) == 2
        to_str += self.error_name_contact

        # pad first_name to 24 characters
        to_str += self.first_name_contact.ljust(24)
        assert len(self.error_first_name_contact) == 2
        to_str += self.error_first_name_contact

        assert len(self.tel_contact) == 10
        to_str += self.tel_contact
        assert len(self.error_tel_contact) == 2
        to_str += self.error_tel_contact

        assert len(self.type_invoice) == 2
        to_str += self.type_invoice
        assert len(self.error_type_invoice) == 2
        to_str += self.error_type_invoice

        assert len(self.type_invoicing) == 2
        to_str += self.type_invoicing
        assert len(self.error_type_invoicing) == 2
        to_str += self.error_type_invoicing

        reserve = "0" * 20
        to_str += reserve
        
        return to_str

    def _error_shared(self, key, error, value) -> Optional[Dict[str, Any]]:
        if error == "00":
            return None
        
        return {
            "key": key,
            "value": value,
            "error_code": error,
            "message": ERROR_CONSTANTS.get(error)
        }
 
    def _error_year_and_month(self) -> Optional[Dict[str, Any]]:
        error = self.error_year_and_month
        value = self.year_and_month
        return self._error_shared("jaar en maand", error, value)

    def _error_num_invoice(self) -> Optional[Dict[str, Any]]:
        error = self.error_num_invoice
        value = self.num_invoice
        error_dict = self._error_shared("nummer factuur", error, value)

        if error_dict is None or error_dict.get("message") is not None:
            return error_dict
        
        msg = ""
        if error == "40":
            msg = "Melding van een dubbele verzending van een facturatiebestand."
        
        error_dict["message"] = msg
        return error_dict

    def _error_date_invoice(self) -> Optional[Dict[str, Any]]:
        error = self.error_date_invoice
        value = self.date_invoice
        error_dict = self._error_shared("datum factuur", error, value)

        if error_dict is None or (error_dict.get("message") is not None and error_dict.get("message") != "20"):
            return error_dict
        
        msg = ""
        if error == "20":
            msg = "Datum > dag datum"
        elif error == "21":
            msg = "Onwaarschijnlijke datum (datum < 01/01/2002)."
        
        error_dict["message"] = msg
        return error_dict

    def _error_reference_invoice(self) -> Optional[Dict[str, Any]]:
        error = self.error_reference_invoice
        value = self.reference_invoice
        return self._error_shared("referentie factuur", error, value)

    def _error_version_instructions(self) -> Optional[Dict[str, Any]]:
        error = self.error_version_instructions
        value = self.version_instructions
        error_dict = self._error_shared("versie instructies", error, value)

        if error_dict is None or error_dict.get("message") is not None:
            return error_dict
        
        msg = ""
        if error == "21":
            msg = "Incompatibiliteit met de waarde vermeld in zone 202"
        
        error_dict["message"] = msg
        return error_dict

    def _error_name_contact(self) -> Optional[Dict[str, Any]]:
        error = self.error_name_contact
        value = self.name_contact
        return self._error_shared("naam contact", error, value)

    def _error_first_name_contact(self) -> Optional[Dict[str, Any]]:
        error = self.error_first_name_contact
        value = self.first_name_contact
        return self._error_shared("voornaam contact", error, value)

    def _error_tel_contact(self) -> Optional[Dict[str, Any]]:
        error = self.error_tel_contact
        value = self.tel_contact
        return self._error_shared("tel contact", error, value)

    def _error_type_invoice(self) -> Optional[Dict[str, Any]]:
        error = self.error_type_invoice
        value = self.type_invoice
        error_dict = self._error_shared("type factuur", error, value)

        if error_dict is None or (error_dict.get("message") is not None and error_dict.get("message") != "20"):
            return error_dict
        
        msg = ""
        if error == "20":
            msg = "Niet toegestane waarde in functie van de sector die het factuur heeft doorgestuurd."
        
        error_dict["message"] = msg
        return error_dict

    def _error_type_invoicing(self) -> Optional[Dict[str, Any]]:
        error = self.error_type_invoicing
        value = self.type_invoicing
        error_dict = self._error_shared("type facturering", error, value)

        if error_dict is None or (error_dict.get("message") is not None and error_dict.get("message") != "20"):
            return error_dict
        
        msg = ""
        if error == "20":
            msg = "Niet toegestane waarde in functie van de sector die het factuur heeft doorgestuurd."
        elif error == "30":
            msg = "Waarde # van 1, 2, 5 met nochtans zone 308 = 3"
        
        error_dict["message"] = msg
        return error_dict
    
    def errors(self) -> List[Dict[str, Any]]:
        errors = [
            self._error_year_and_month(),
            self._error_num_invoice(),
            self._error_date_invoice(),
            self._error_reference_invoice(),
            self._error_version_instructions(),
            self._error_name_contact(),
            self._error_first_name_contact(),
            self._error_tel_contact(),
            self._error_type_invoice(),
            self._error_type_invoicing(),
        ]
        return [ErrorMessage(**e) for e in errors if e is not None]


class Header300Refusal(Header300):
    percentage_errors: str
    error_percentage_errors: Optional[str] = "00"
    refusal_type: str
    error_refusal_type: Optional[str] = "00"

    @classmethod
    def from_str(cls, msg: str) -> "Header300Refusal":
        assert len(msg) == 677-67
        return Header300Refusal(
            year_and_month = msg[:6],
            error_year_and_month = msg[6:8],
            num_invoice = msg[8:11],
            error_num_invoice = msg[11:13],
            date_invoice = msg[13:21],
            error_date_invoice = msg[21:23],
            reference_invoice = msg[23:36],
            error_reference_invoice = msg[36:38],
            version_instructions = msg[38:45],
            error_version_instructions = msg[45:47],
            name_contact = msg[47:92],
            error_name_contact = msg[92:94],
            first_name_contact = msg[94:118],
            error_first_name_contact = msg[118:120],
            tel_contact = msg[120:130],
            error_tel_contact = msg[130:132],
            type_invoice = msg[132:134],
            error_type_invoice = msg[134:136],
            type_invoicing = msg[136:138],
            error_type_invoicing = msg[138:140],
            percentage_errors = msg[140:145],
            error_percentage_errors = msg[145:147],
            refusal_type = msg[147:149],
            error_refusal_type = msg[149:151],
        )
    
    def __str__(self):
        to_str = ""
        assert len(self.year_and_month) == 6
        to_str += self.year_and_month
        assert len(self.error_year_and_month) == 2
        to_str += self.error_year_and_month
        assert len(self.num_invoice) == 3
        to_str += self.num_invoice
        assert len(self.error_num_invoice) == 2
        to_str += self.error_num_invoice
        assert len(self.date_invoice) == 8
        to_str += self.date_invoice
        assert len(self.error_date_invoice) == 2
        to_str += self.error_date_invoice
        assert len(self.reference_invoice) == 13
        to_str += self.reference_invoice
        assert len(self.error_reference_invoice) == 2
        to_str += self.error_reference_invoice
        assert len(self.version_instructions) == 7
        to_str += self.version_instructions
        assert len(self.error_version_instructions) == 2
        to_str += self.error_version_instructions

        # pad name to 45 characters
        to_str += self.name_contact.ljust(45)
        assert len(self.error_name_contact) == 2
        to_str += self.error_name_contact

        # pad first_name to 24 characters
        to_str += self.first_name_contact.ljust(24)
        assert len(self.error_first_name_contact) == 2
        to_str += self.error_first_name_contact

        assert len(self.tel_contact) == 10
        to_str += self.tel_contact
        assert len(self.error_tel_contact) == 2
        to_str += self.error_tel_contact

        assert len(self.type_invoice) == 2
        to_str += self.type_invoice
        assert len(self.error_type_invoice) == 2
        to_str += self.error_type_invoice

        assert len(self.type_invoicing) == 2
        to_str += self.type_invoicing
        assert len(self.error_type_invoicing) == 2
        to_str += self.error_type_invoicing

        assert len(self.percentage_errors) == 5
        to_str += self.percentage_errors
        assert len(self.error_percentage_errors) == 2
        to_str += self.error_percentage_errors

        assert len(self.refusal_type) == 2
        to_str += self.refusal_type
        assert len(self.error_refusal_type) == 2
        to_str += self.error_refusal_type

        reserve = " " * 459
        to_str += reserve
        
        return to_str

    def _error_shared(self, key, error, value) -> Optional[Dict[str, Any]]:
        if error == "00":
            return None
        
        return {
            "key": key,
            "value": value,
            "error_code": error,
            "message": ERROR_CONSTANTS.get(error)
        }
    
    def errors(self) -> List[Dict[str, Any]]:
        errors = [
            self._error_year_and_month(),
            self._error_num_invoice(),
            self._error_date_invoice(),
            self._error_reference_invoice(),
            self._error_version_instructions(),
            self._error_name_contact(),
            self._error_first_name_contact(),
            self._error_tel_contact(),
            self._error_type_invoice(),
            self._error_type_invoicing(),
        ]
        return [ErrorMessage(**e) for e in errors if e is not None]
    
class Record10(BaseModel):
    record: Optional[str] = "10"
    num_record: Optional[str] = "000001"
    indexcode: Optional[str] = "0"
    version_file: Optional[str] = "9991999" # 9991999 for test, 0001999 for prd
    financieel_rekeningnummer_a_1: Optional[str] = "00000000"
    financieel_rekeningnummer_a_2: Optional[str] = "0000"
    zendingsnummer: str # nummer mutualiteit
    financieel_rekeningnummer_b: Optional[str] = "000000000000"
    code_afschaffing_papieren_factuur: Optional[str] = "0"
    code_afrekeningsbestand: Optional[str] = "0"
    inhoud_facturatie: str
    nummer_derdebetalende: str
    nummer_accreditering_nic: Optional[str] = "000000000000"
    beroepscode_facturerende_derde: Optional[str] = "000"
    date_creation: str
    kbo_number: Optional[str] = "0000000000"
    reference: str
    bic_bank: str
    iban_bank: str
    bic_bank_2: Optional[str] = ""
    iban_bank_2: Optional[str] = ""

    @classmethod
    def _error_shared(cls, key, error, value, refusal_code) -> Optional[Dict[str, Any]]:
        if error == "00":
            return None
        
        _ERROR_CONSTANTS = {
            "01": "Gegeven niet numeriek",
            "02": "Controlecijfer foutief",
            "03": "Gegeven niet toegelaten",
            "09": "Verboden karakters",
            "20": "Gegeven niet gekend in bestand ziekenfonds",
        }
        
        return {
            "type": "10",
            "key": key,
            "value": value,
            "error_code": error,
            "message": _ERROR_CONSTANTS.get(error),
            "verwerpingsletter": refusal_code
        }
    
    @classmethod
    def errors_from_str(cls, record: str) -> List[Dict[str, Any]]:
        # I'm only going to bother to map the actual errors
        result = []
        for i in range(3):
            e = record[456+i*7:456+7+i*7]
            if e[0] == " ":
                # no more errors
                break
            else:
                # I'm only going to bother with fields that I actually encounter
                key_numeric = e[3:5]
                key = ""
                error = e[5:7]
                value = ""
                if key_numeric == "00":
                    continue # TODO?

                if key_numeric == "07":
                    key = "zendingsnummer"
                    value = record[32:35]
                elif key_numeric == "14":
                    key = "nummer derdebetalende"
                    value = record[55:67]
                elif key_numeric == "27":
                    key = "KBO nummer"
                    value = record[127:137]
                elif key_numeric == "31":
                    key = "BIC Bank"
                    value = record[166:174]
                elif key_numeric == "99":
                    key = "Controlecijfer"
                    value = record[348:350]
                else:
                    raise Exception(f"Numeric key {key_numeric} not yet mapped for Record10")

                e_dict = cls._error_shared(key, error, value, e[0])
            result.append(ErrorMessage(**e_dict))
        return result
    
    def __str__(self):
        to_str = ""
        assert len(self.record) == 2
        to_str += self.record
        assert len(self.num_record) == 6
        to_str += self.num_record
        assert len(self.indexcode) == 1
        to_str += self.indexcode
        assert len(self.version_file) == 7
        to_str += self.version_file
        assert len(self.financieel_rekeningnummer_a_1) == 8
        to_str += self.financieel_rekeningnummer_a_1
        assert len(self.financieel_rekeningnummer_a_2) == 4
        to_str += self.financieel_rekeningnummer_a_2

        reserve = "0" * 4
        to_str += reserve

        assert len(self.zendingsnummer) == 3
        to_str += self.zendingsnummer
        assert len(self.financieel_rekeningnummer_b) == 12
        to_str += self.financieel_rekeningnummer_b

        reserve = "0" * 1
        to_str += reserve

        assert len(self.code_afschaffing_papieren_factuur) == 1
        to_str += self.code_afschaffing_papieren_factuur
        assert len(self.code_afrekeningsbestand) == 1
        to_str += self.code_afrekeningsbestand

        reserve = "0" * 1
        to_str += reserve
        reserve = "0" * 1
        to_str += reserve

        assert len(self.inhoud_facturatie) == 3
        to_str += self.inhoud_facturatie
        assert len(self.nummer_derdebetalende) == 12
        to_str += self.nummer_derdebetalende
        assert len(self.nummer_accreditering_nic) == 12
        to_str += self.nummer_accreditering_nic

        reserve = "0" * 1
        to_str += reserve
        reserve = "0" * 4
        to_str += reserve

        assert len(self.beroepscode_facturerende_derde) == 3
        to_str += self.beroepscode_facturerende_derde

        reserve = "0" * 12
        to_str += reserve
        reserve = "0" * 7
        to_str += reserve
        reserve = "0" * 1
        to_str += reserve

        to_str += ("0" + self.date_creation[:4])
        to_str += self.date_creation[4:6]

        reserve = "0" * 5
        to_str += reserve

        # actually 7+1, but that's silly
        assert len(self.date_creation) == 8
        to_str += self.date_creation

        assert len(self.kbo_number) == 10
        to_str += self.kbo_number

        to_str += self.reference.ljust(25)

        reserve = "0" * 2
        to_str += reserve
        reserve = "0" * 2
        to_str += reserve

        # actually 8+1+1+1, but that's silly
        to_str += self.bic_bank.ljust(11)

        reserve = "0" * 1
        to_str += reserve

        # actually 1+3+12+10+2+6, but that's silly
        to_str += self.iban_bank.ljust(34)

        reserve = "0" * 6
        to_str += reserve

        to_str += self.bic_bank_2.ljust(11)

        reserve = "0" * 1
        to_str += reserve
        reserve = "0" * 4
        to_str += reserve

        # reserve staatshervorming
        reserve = "0" * 26
        to_str += reserve
        reserve = "0" * 1
        to_str += reserve
        reserve = "0" * 7
        to_str += reserve

        reserve = "0" * 1
        to_str += reserve
        reserve = "0" * 1
        to_str += reserve

        to_str += self.iban_bank_2.ljust(34)

        # reserve staatshervorming
        reserve = "0" * 8
        to_str += reserve
        reserve = "0" * 3
        to_str += reserve

        # the remainder in one go
        reserve = "0" * 33
        to_str += reserve

        control = calculate_control(to_str)
        to_str += control

        return to_str

class Record20(BaseModel):
    record: Optional[str] = "20"
    num_record: Optional[str] = "000002"
    toestemming_derdebetalende: Optional[str] = "0"
    uur_van_opname: Optional[str] = "0000000"
    datum_van_opname: Optional[str] = "00000000"
    datum_van_ontslag_1: Optional[str] = "0000"
    datum_van_ontslag_2: Optional[str] = "0000"
    nummer_ziekenfonds_aansluiting: str
    identificatie_rechthebbende_1: str
    identificatie_rechthebbende_2: str
    geslacht_rechthebbende: str
    type_factuur: str
    type_facturering: Optional[str] = "0"
    dienst_721_bis: Optional[str] = "000"
    nummer_facturerende_instelling: str
    instelling_van_verblijf: Optional[str] = "000000000000"
    code_stuiten_verjaringstermijn: Optional[str] = "0"
    reden_behandeling: Optional[str] = "0000"
    nummer_ziekenfonds_bestemming: str
    nummer_opname: Optional[str] = "000000000000"
    datum_akkoord_revalidatie_1: Optional[str] = "0000000"
    datum_akkoord_revalidatie_2: Optional[str] = "0"
    uur_van_ontslag: Optional[str] = "00000"
    nummer_individuele_factuur_1: str
    nummer_individuele_factuur_2: Optional[str] = "0000000"
    toepassing_sociale_franchise: Optional[str] = "0"
    cg1_cg2: str
    referentie_instelling: str
    nummer_vorige_factuur_1: Optional[str] = "00"
    nummer_vorige_factuur_2: Optional[str] = "00"
    nummer_vorige_factuur_3: Optional[str] = "00000000"
    flag_identificatie_rechthebbende: Optional[str] = "1"
    nummer_vorige_zending_1: Optional[str] = "0"
    nummer_vorige_zending_2: Optional[str] = "0"
    nummer_vorige_zending_3: Optional[str] = "0"
    nummer_ziekenfonds_vorige_facturering: Optional[str] = "000"
    referentie_ziekenfonds_financieel_rekeningnummer_a_1: Optional[str] = ""
    referentie_ziekenfonds_financieel_rekeningnummer_a_2: Optional[str] = ""
    vorig_gefactureerd_jaar_en_maand: Optional[str] = "000000"
    referentiegegevens_netwerk_1: Optional[str] = ""
    referentiegegevens_netwerk_2: Optional[str] = ""
    referentiegegevens_netwerk_3: Optional[str] = ""
    referentiegegevens_netwerk_4: Optional[str] = ""
    referentiegegevens_netwerk_5: Optional[str] = ""
    datum_facturering_1: Optional[str] = "0000000"
    datum_facturering_2: Optional[str] = "0"
    referentie_ziekenfonds_financieel_rekeningnummer_b_1: Optional[str] = ""
    referentie_ziekenfonds_financieel_rekeningnummer_b_2: Optional[str] = ""
    referentie_ziekenfonds_financieel_rekeningnummer_b_2bis: Optional[str] = ""
    referentie_ziekenfonds_financieel_rekeningnummer_b_3: Optional[str] = ""
    opnamenummer_moeder: Optional[str] = "000000000000"
    begindatum_verzekerbaarheid: Optional[str] = "00000000"
    einddatum_verzekerbaarheid_1: Optional[str] = "000"
    einddatum_verzekerbaarheid_2: Optional[str] = "0"
    einddatum_verzekerbaarheid_3: Optional[str] = "0000"
    datum_mededeling_informatie: Optional[str] = "00000000"
    maf_lopend_jaar: Optional[str] = "0000"
    maf_lopend_jaar_min1: Optional[str] = "0000"
    maf_lopend_jaar_min2: Optional[str] = "0000"

    @classmethod
    def _error_shared(cls, key, error, value, refusal_code) -> Optional[Dict[str, Any]]:
        if error == "00":
            return None
        
        _ERROR_CONSTANTS = {
            "01": "Gegeven niet numeriek",
            "02": "Controlecijfer foutief",
            "03": "Gegeven niet toegelaten",
            "09": "Verboden karakters",
            "20": "Gegeven niet gekend in bestand ziekenfonds",
        }
        
        return {
            "type": "20",
            "key": key,
            "value": value,
            "error_code": error,
            "message": _ERROR_CONSTANTS.get(error),
            "verwerpingsletter": refusal_code
        }
    
    @classmethod
    def errors_from_str(cls, record: str) -> List[Dict[str, Any]]:
        # I'm only going to bother to map the actual errors
        result = []
        for i in range(3):
            e = record[456+i*7:456+7+i*7]
            if e[0] == " ":
                # no more errors
                break
            else:
                # I'm only going to bother with fields that I actually encounter
                key_numeric = e[3:5]
                key = ""
                error = e[5:7]
                value = ""
                if key_numeric == "00":
                    continue # TODO?

                if key_numeric == "07":
                    key = "nummer ziekenfonds van aansluiting"
                    value = record[32:35]
                elif key_numeric == "08":
                    key = "identificatie rechthebbende"
                    value = record[35:47]
                elif key_numeric == "09":
                    key = "geslacht rechthebbende"
                    value = record[48:49]
                elif key_numeric == "18":
                    key = "nummer ziekenfonds van bestemming"
                    value = record[84:87]
                elif key_numeric == "99":
                    key = "controlecijfer record"
                    value = record[348:350]
                else:
                    raise Exception(f"Numeric key {key_numeric} not yet mapped for Record20")

                e_dict = cls._error_shared(key, error, value, e[0])
            result.append(ErrorMessage(**e_dict))
        return result
    
    def __str__(self):
        to_str = ""
        assert len(self.record) == 2
        to_str += self.record
        assert len(self.num_record) == 6
        to_str += self.num_record
        assert len(self.toestemming_derdebetalende) == 1
        to_str += self.toestemming_derdebetalende
        assert len(self.uur_van_opname) == 7
        to_str += self.uur_van_opname
        assert len(self.datum_van_opname) == 8
        to_str += self.datum_van_opname
        assert len(self.datum_van_ontslag_1) == 4
        to_str += self.datum_van_ontslag_1
        assert len(self.datum_van_ontslag_2) == 4
        to_str += self.datum_van_ontslag_2

        assert len(self.nummer_ziekenfonds_aansluiting) == 3
        to_str += self.nummer_ziekenfonds_aansluiting
        assert len(self.identificatie_rechthebbende_1) == 12
        to_str += self.identificatie_rechthebbende_1
        assert len(self.identificatie_rechthebbende_2) == 1
        to_str += self.identificatie_rechthebbende_2
        assert len(self.geslacht_rechthebbende) == 1
        to_str += self.geslacht_rechthebbende

        assert len(self.type_factuur) == 1
        to_str += self.type_factuur
        assert len(self.type_facturering) == 1
        to_str += self.type_facturering
        reserve = "0" * 1
        to_str += reserve
        assert len(self.dienst_721_bis) == 3
        to_str += self.dienst_721_bis

        assert len(self.nummer_facturerende_instelling) == 12
        to_str += self.nummer_facturerende_instelling
        assert len(self.instelling_van_verblijf) == 12
        to_str += self.instelling_van_verblijf
        assert len(self.code_stuiten_verjaringstermijn) == 1
        to_str += self.code_stuiten_verjaringstermijn
        assert len(self.reden_behandeling) == 4
        to_str += self.reden_behandeling

        assert len(self.nummer_ziekenfonds_bestemming) == 3
        to_str += self.nummer_ziekenfonds_bestemming
        assert len(self.nummer_opname) == 12
        to_str += self.nummer_opname
        assert len(self.datum_akkoord_revalidatie_1) == 7
        to_str += self.datum_akkoord_revalidatie_1
        assert len(self.datum_akkoord_revalidatie_2) == 1
        to_str += self.datum_akkoord_revalidatie_2

        assert len(self.uur_van_ontslag) == 5
        to_str += self.uur_van_ontslag
        reserve = "0" * 2
        to_str += reserve
        assert len(self.nummer_individuele_factuur_1) == 5
        to_str += self.nummer_individuele_factuur_1
        assert len(self.nummer_individuele_factuur_2) == 7
        to_str += self.nummer_individuele_factuur_2

        assert len(self.toepassing_sociale_franchise) == 1
        to_str += self.toepassing_sociale_franchise
        assert len(self.cg1_cg2) == 10
        to_str += self.cg1_cg2
        to_str += self.referentie_instelling.ljust(25)

        assert len(self.nummer_vorige_factuur_1) == 2
        to_str += self.nummer_vorige_factuur_1
        assert len(self.nummer_vorige_factuur_2) == 2
        to_str += self.nummer_vorige_factuur_2
        assert len(self.nummer_vorige_factuur_3) == 8
        to_str += self.nummer_vorige_factuur_3

        assert len(self.flag_identificatie_rechthebbende) == 1
        to_str += self.flag_identificatie_rechthebbende
        reserve = "0" * 1
        to_str += reserve
        assert len(self.nummer_vorige_zending_1) == 1
        to_str += self.nummer_vorige_zending_1
        assert len(self.nummer_vorige_zending_2) == 1
        to_str += self.nummer_vorige_zending_2
        assert len(self.nummer_vorige_zending_3) == 1
        to_str += self.nummer_vorige_zending_3

        assert len(self.nummer_ziekenfonds_vorige_facturering) == 3
        to_str += self.nummer_ziekenfonds_vorige_facturering
        to_str += self.referentie_ziekenfonds_financieel_rekeningnummer_a_1.ljust(12)
        to_str += self.referentie_ziekenfonds_financieel_rekeningnummer_a_2.ljust(10)
        reserve = "0" * 2
        to_str += reserve

        assert len(self.vorig_gefactureerd_jaar_en_maand) == 6
        to_str += self.vorig_gefactureerd_jaar_en_maand
        to_str += self.referentiegegevens_netwerk_1.ljust(48, "0") # TODO incorrect!!
        reserve = "0" * 1
        to_str += reserve

        assert len(self.datum_facturering_1) == 7
        to_str += self.datum_facturering_1
        assert len(self.datum_facturering_2) == 1
        to_str += self.datum_facturering_2
        reserve = "0" * 1
        to_str += reserve 

        to_str += self.referentie_ziekenfonds_financieel_rekeningnummer_b_1.ljust(12)
        to_str += self.referentie_ziekenfonds_financieel_rekeningnummer_b_2.ljust(3)
        to_str += self.referentie_ziekenfonds_financieel_rekeningnummer_b_2bis.ljust(1)
        to_str += self.referentie_ziekenfonds_financieel_rekeningnummer_b_3.ljust(6)

        assert len(self.opnamenummer_moeder) == 12
        to_str += self.opnamenummer_moeder
        assert len(self.begindatum_verzekerbaarheid) == 8
        to_str += self.begindatum_verzekerbaarheid
        assert len(self.einddatum_verzekerbaarheid_1) == 3
        to_str += self.einddatum_verzekerbaarheid_1
        assert len(self.einddatum_verzekerbaarheid_2) == 1
        to_str += self.einddatum_verzekerbaarheid_2
        assert len(self.einddatum_verzekerbaarheid_3) == 4
        to_str += self.einddatum_verzekerbaarheid_3

        assert len(self.datum_mededeling_informatie) == 8
        to_str += self.datum_mededeling_informatie
        assert len(self.maf_lopend_jaar) == 4
        to_str += self.maf_lopend_jaar
        assert len(self.maf_lopend_jaar_min1) == 4
        to_str += self.maf_lopend_jaar_min1
        assert len(self.maf_lopend_jaar_min2) == 4
        to_str += self.maf_lopend_jaar_min2

        reserve = "0" * 6
        to_str += reserve 
        reserve = "0" * 2
        to_str += reserve

        control = calculate_control(to_str)

        to_str += control
        return to_str

class Record50(BaseModel):
    record: Optional[str] = "50"
    num_record: Optional[str] = "000003"
    norm_vertrekking: Optional[str] = "0"
    nomenclatuur: str
    datum_eerste_verstrekking: str
    datum_laatste_verstrekking: str
    nummer_ziekenfonds_rechthebbende: str
    identificatie_rechthebbende_1: str
    identificatie_rechthebbende_2: str
    geslacht_rechthebbende: str
    bevalling: Optional[str] = "0"
    verwijzing_financieel_rekeningnummer: Optional[str] = "0"
    nacht_weekeinde_feestdag: Optional[str] = "0"
    dienstcode: Optional[str] = "990"
    plaats_van_verstrekking: Optional[str] = "000000000000"
    identificatie_verstrekker: str
    norm_verstrekker: Optional[str] = "1"
    betrekkelijke_verstrekking_1: Optional[str] = "0000"
    betrekkelijke_verstrekking_2: Optional[str] = "000"
    bedrag_verzekeringstegemoetkoming: str
    datum_voorschrift: str
    aantal: int
    afwijking_maximaal_aantal_of_identieke_prestatie: Optional[str] = "00"
    identificatie_voorschrijver: str
    norm_voorschrijver: Optional[str] = "1"
    persoonlijk_aandeel_patient: str
    referentie_instelling: str
    behandelde_tand: Optional[str] = "00"
    bedrag_supplement: str
    uitzondering_derdebetalersregeling: Optional[str] = "0"
    code_facturering_persoonlijk_aandeel_of_supplement: Optional[str] = "0"
    behandeld_lid: Optional[str] = "0"
    geconventioneerde_verstrekker: str
    uur_van_prestatie: Optional[str] = "0000"
    identificatie_toediener_bloed: Optional[str] = "000000000000"
    nummer_attest_van_toediening: Optional[str] = "0" * 12
    nummer_afleveringsbon: Optional[str] = "0" * 12
    code_implant: Optional[str] = "0" * 12
    omschrijving_product: Optional[str] = "+" * 30
    norm_plafond: Optional[str] = "0"
    basiswaarde_verstrekking: Optional[str] = "0" * 8
    transplantatie: Optional[str] = "0"
    identificatie_bijkomende_verstrekker: Optional[str] = "0" * 12
    aandeel_in_forfait: Optional[str] = "0" * 3
    aanduiding_prestatie_in_kader_lectuur_eid: Optional[str] = "0"
    ziekenhuissite: Optional[str] = "0" * 6
    identificatie_associatie_zorggebied: Optional[str] = "0" * 12
    ritnummer: Optional[str] = "0" * 11
    flag_gps: Optional[str] = "0"
    notificatiecode_implantaat: Optional[str] = "0" * 12
    registratiecode: Optional[str] = "0" * 14
    flag_btw: Optional[str] = "00"

    @classmethod
    def _error_shared(cls, key, error, value, refusal_code) -> Optional[Dict[str, Any]]:
        if error == "00":
            return None
        
        _ERROR_CONSTANTS = {
            "01": "Gegeven niet numeriek",
            "02": "Controlecijfer foutief",
            "03": "Gegeven niet toegelaten",
            "09": "Verboden karakters",
            "20": "Gegeven niet gekend in bestand ziekenfonds",
        }
        
        return {
            "type": "50",
            "key": key,
            "value": value,
            "error_code": error,
            "message": _ERROR_CONSTANTS.get(error),
            "verwerpingsletter": refusal_code
        }
    
    @classmethod
    def errors_from_str(cls, record: str) -> List[Dict[str, Any]]:
        # I'm only going to bother to map the actual errors
        result = []
        for i in range(3):
            e = record[456+i*7:456+7+i*7]
            if e[0] == " ":
                # no more errors
                break
            else:
                # I'm only going to bother with fields that I actually encounter
                key_numeric = e[3:5]
                key = ""
                error = e[5:7]
                value = ""
                if key_numeric == "00":
                    continue # TODO?

                if key_numeric == "01":
                    # see mail 20240228
                    # only present to indicate there    
                    # is an error in this record
                    continue
                elif key_numeric == "08":
                    key = "identificatie rechthebbende"
                    value = record[35:47]
                elif key_numeric == "19":
                    key = "Teken en bedrag verzekeringstegemoetkoming"
                    value = record[87:99]
                elif key_numeric == "20":
                    key = "Datum voorschrift"
                    value = record[99:107]
                elif key_numeric == "24":
                    key = "Identificatie voorschrijver"
                    value = record[114:119]
                elif key_numeric == "26":
                    key = "Norm voorschrijver"
                    value = record[126:127]
                elif key_numeric == "27":
                    key = "Teken en bedrag persoonlijk aandeel patiënt"
                    value = record[127:137]
                elif key_numeric == "28":
                    key = "Referentie instelling"
                    value = record[137:162]
                elif key_numeric == "30":
                    key = "Teken en bedrag persoonlijk supplement"
                    value = record[164:174]
                elif key_numeric == "99":
                    key = "controlecijfer record"
                    value = record[348:350]
                else:
                    raise Exception(f"Numeric key {key_numeric} not yet mapped for Record50 {e}")

                e_dict = cls._error_shared(key, error, value, e[0])
            result.append(ErrorMessage(**e_dict))
        return result
    
    def __str__(self):
        to_str = ""
        assert len(self.record) == 2
        to_str += self.record
        assert len(self.num_record) == 6
        to_str += self.num_record

        assert len(self.norm_vertrekking) == 1
        to_str += self.norm_vertrekking
        assert len(self.nomenclatuur) == 7
        to_str += self.nomenclatuur
        assert len(self.datum_eerste_verstrekking) == 8
        to_str += self.datum_eerste_verstrekking
        assert len(self.datum_laatste_verstrekking) == 8
        to_str += self.datum_laatste_verstrekking

        assert len(self.nummer_ziekenfonds_rechthebbende) == 3
        to_str += self.nummer_ziekenfonds_rechthebbende
        assert len(self.identificatie_rechthebbende_1) == 12
        to_str += self.identificatie_rechthebbende_1
        assert len(self.identificatie_rechthebbende_2) == 1
        to_str += self.identificatie_rechthebbende_2
        assert len(self.geslacht_rechthebbende) == 1
        to_str += self.geslacht_rechthebbende

        assert len(self.bevalling) == 1
        to_str += self.bevalling
        assert len(self.verwijzing_financieel_rekeningnummer) == 1
        to_str += self.verwijzing_financieel_rekeningnummer
        assert len(self.nacht_weekeinde_feestdag) == 1
        to_str += self.nacht_weekeinde_feestdag
        assert len(self.dienstcode) == 3
        to_str += self.dienstcode
        assert len(self.plaats_van_verstrekking) == 12
        to_str += self.plaats_van_verstrekking

        assert len(self.identificatie_verstrekker) == 12
        to_str += self.identificatie_verstrekker
        assert len(self.norm_verstrekker) == 1
        to_str += self.norm_verstrekker
        assert len(self.betrekkelijke_verstrekking_1) == 4
        to_str += self.betrekkelijke_verstrekking_1
        assert len(self.betrekkelijke_verstrekking_2) == 3
        to_str += self.betrekkelijke_verstrekking_2

        to_str += ("+" + self.bedrag_verzekeringstegemoetkoming.rjust(11, "0"))
        assert len(self.datum_voorschrift) == 8
        to_str += self.datum_voorschrift

        to_str += ("+" + str(self.aantal).rjust(4, "0"))
        assert len(self.afwijking_maximaal_aantal_of_identieke_prestatie) == 2
        to_str += self.afwijking_maximaal_aantal_of_identieke_prestatie

        to_str += self.identificatie_voorschrijver.rjust(12, "0")
        assert len(self.norm_voorschrijver) == 1
        to_str += self.norm_voorschrijver

        to_str += ("+" + self.persoonlijk_aandeel_patient.rjust(9, "0"))
        to_str += self.referentie_instelling.ljust(25)

        assert len(self.behandelde_tand) == 2
        to_str += self.behandelde_tand
        to_str += ("+" + self.bedrag_supplement.rjust(9, "0"))
        assert len(self.uitzondering_derdebetalersregeling) == 1
        to_str += self.uitzondering_derdebetalersregeling
        assert len(self.code_facturering_persoonlijk_aandeel_of_supplement) == 1
        to_str += self.code_facturering_persoonlijk_aandeel_of_supplement
        assert len(self.behandeld_lid) == 1
        to_str += self.behandeld_lid
        assert len(self.geconventioneerde_verstrekker) == 1
        to_str += self.geconventioneerde_verstrekker
        assert len(self.uur_van_prestatie) == 4
        to_str += self.uur_van_prestatie
        assert len(self.identificatie_toediener_bloed) == 12
        to_str += self.identificatie_toediener_bloed
        assert len(self.nummer_attest_van_toediening) == 12
        to_str += self.nummer_attest_van_toediening
        assert len(self.nummer_afleveringsbon) == 12
        to_str += self.nummer_attest_van_toediening
        assert len(self.code_implant) == 12
        to_str += self.code_implant
        assert len(self.omschrijving_product) == 30
        to_str += self.omschrijving_product

        assert len(self.norm_plafond) == 1
        to_str += self.norm_plafond
        assert len(self.basiswaarde_verstrekking) == 8
        to_str += self.basiswaarde_verstrekking
        assert len(self.transplantatie) == 1
        to_str += self.transplantatie
        assert len(self.identificatie_bijkomende_verstrekker) == 12
        to_str += self.identificatie_bijkomende_verstrekker

        assert len(self.aandeel_in_forfait) == 3
        to_str += self.aandeel_in_forfait
        assert len(self.aanduiding_prestatie_in_kader_lectuur_eid) == 1
        to_str += self.aanduiding_prestatie_in_kader_lectuur_eid
        assert len(self.ziekenhuissite) == 6
        to_str += self.ziekenhuissite
        assert len(self.identificatie_associatie_zorggebied) == 12
        to_str += self.identificatie_associatie_zorggebied

        assert len(self.ritnummer) == 11
        to_str += self.ritnummer
        assert len(self.flag_gps) == 1
        to_str += self.flag_gps
        
        reserve = "0" * 4
        to_str += reserve

        assert len(self.notificatiecode_implantaat) == 12
        to_str += self.notificatiecode_implantaat
        assert len(self.registratiecode) == 14
        to_str += self.registratiecode
        assert len(self.flag_btw) == 2
        to_str += self.flag_btw

        control = calculate_control(to_str)
        to_str += control
        return to_str


class Record51(BaseModel):
    record: Optional[str] = "51"
    num_record: Optional[str] = "000004"
    nomenclatuur: str
    datum_verstrekking: str
    identificatie_rechthebbende_1: str
    identificatie_rechthebbende_2: str
    identificatie_verstrekker: str
    betrekkelijke_verstrekking: Optional[str] = "0000000"
    bedrag_verzekeringstegemoetkoming: str
    code_gerechtigde: str
    nummer_akkoord_tariefverbintenis: str
    datum_mededeling_informatie: str

    @classmethod
    def _error_shared(cls, key, error, value, refusal_code) -> Optional[Dict[str, Any]]:
        if error == "00":
            return None
        
        _ERROR_CONSTANTS = {
            "01": "Gegeven niet numeriek",
            "02": "Controlecijfer foutief",
            "03": "Gegeven niet toegelaten",
            "09": "Verboden karakters",
            "20": "Gegeven niet gekend in bestand ziekenfonds",
        }
        
        return {
            "type": "51",
            "key": key,
            "value": value,
            "error_code": error,
            "message": _ERROR_CONSTANTS.get(error),
            "verwerpingsletter": refusal_code
        }
    
    @classmethod
    def errors_from_str(cls, record: str) -> List[Dict[str, Any]]:
        # I'm only going to bother to map the actual errors
        result = []
        for i in range(3):
            e = record[456+i*7:456+7+i*7]
            if e[0] == " ":
                # no more errors
                break
            else:
                # I'm only going to bother with fields that I actually encounter
                key_numeric = e[3:5]
                key = ""
                error = e[5:7]
                value = ""

                if key_numeric == "00":
                    continue # TODO?

                if key_numeric == "01":
                    key = "recordtype"
                    value = record[0:2]
                elif key_numeric == "05":
                    key = "datum verstrekking"
                    value = record[16:24]
                elif key_numeric == "08":
                    key = "identificatie rechthebbende"
                    value = record[35:47]
                elif key_numeric == "15":
                    key = "identificatie verstrekker"
                    value = record[67:79]
                elif key_numeric == "19":
                    key = "Teken + bedrag verzekeringstegemoetkoming"
                    value = record[87:99]
                elif key_numeric == "28":
                    key = "Reserve"
                    value = record[137:162]
                elif key_numeric == "27":
                    key = "Code gerechtigde"
                    value = record[127:137]
                elif key_numeric == "55":
                    key = "Datum mededeling informatie"
                    value = record[320:328]
                elif key_numeric == "99":
                    key = "controlecijfer record"
                    value = record[348:350]
                else:
                    raise Exception(f"Numeric key {key_numeric} not yet mapped for Record51")

                e_dict = cls._error_shared(key, error, value, e[0])
            result.append(ErrorMessage(**e_dict))
        return result
    
    def __str__(self):
        to_str = ""
        assert len(self.record) == 2
        to_str += self.record
        assert len(self.num_record) == 6
        to_str += self.num_record
        
        reserve = "0" * 1
        to_str += reserve

        assert len(self.nomenclatuur) == 7
        to_str += self.nomenclatuur
        assert len(self.datum_verstrekking) == 8
        to_str += self.datum_verstrekking

        reserve = "0" * 11
        to_str += reserve

        assert len(self.identificatie_rechthebbende_1) == 12
        to_str += self.identificatie_rechthebbende_1
        assert len(self.identificatie_rechthebbende_2) == 1
        to_str += self.identificatie_rechthebbende_2

        reserve = "0" * 19
        to_str += reserve

        assert len(self.identificatie_verstrekker) == 12
        to_str += self.identificatie_verstrekker
        reserve = "0" * 1
        to_str += reserve
        assert len(self.betrekkelijke_verstrekking) == 7
        to_str += self.betrekkelijke_verstrekking

        to_str += ("+" + self.bedrag_verzekeringstegemoetkoming.rjust(11, "0"))
        reserve = "0" * 28
        to_str += reserve

        assert len(self.code_gerechtigde) == 10
        to_str += self.code_gerechtigde
        reserve = "0" * 75
        to_str += reserve

        assert len(self.nummer_akkoord_tariefverbintenis) == 48
        to_str += self.nummer_akkoord_tariefverbintenis
        reserve = "0" * 60
        to_str += reserve


        assert len(self.datum_mededeling_informatie) == 8
        to_str += self.datum_mededeling_informatie
        reserve = "0" * 20
        to_str += reserve

        control = calculate_control(to_str)
        to_str += control
        return to_str

class Record52(BaseModel):
    record: Optional[str] = "52"
    num_record: Optional[str] = "000004"
    reden_manuele_invoering: Optional[str] = "0"
    nomenclatuur: str
    datum_verstrekking: str
    datum_lezing_identiteitsdocument: Optional[str] = "00000000"
    identificatie_rechthebbende_1: str
    identificatie_rechthebbende_2: str
    
    type_lezing_identiteitsdocument: Optional[str] = "0"
    type_drager_identiteitsdocument: Optional[str] = "0"
    reden_gebruik_vignet: Optional[str] = "0"
    uur_lezing_identiteitsdocument: Optional[str] = "0000"

    riziv_nummer: Optional[str] = "000000000000"
    serienummer_drager: Optional[str] = "000000000000000"
    nummer_bewijsstuk: Optional[str] = "0" * 25
    uniek_nummer_medische_beeldvorming: Optional[str] = "0" * 12
    nummer_akkoord: str

    @classmethod
    def _error_shared(cls, key, error, value, refusal_code) -> Optional[Dict[str, Any]]:
        if error == "00":
            return None
        
        _ERROR_CONSTANTS = {
            "01": "Gegeven niet numeriek",
            "02": "Controlecijfer foutief",
            "03": "Gegeven niet toegelaten",
            "09": "Verboden karakters",
            "20": "Gegeven niet gekend in bestand ziekenfonds",
        }
        
        message = None
        if key == "nummer akkoord":
            if error == "02":
                message = "Nummer akkoord met foutief controlecijfer"
            elif error == "04":
                message = "Nummer akkoord ontbreekt terwijl het noodzakelijk is"
            elif error == "20":
                message = "Nummer akkoord niet gekend in bestand VI op moment van prestatie"
            elif error == "21":
                message = "Nummer akkoord niet gekend in bestand VI"
            elif error == "22":
                message = "Nummer akkoord niet gekend in bestand VI voor deze rechthebbende en/of deze nomenclatuurcode"
        
        return {
            "type": "52",
            "key": key,
            "value": value,
            "error_code": error,
            "message": message or _ERROR_CONSTANTS.get(error),
            "verwerpingsletter": refusal_code
        }
    
    @classmethod
    def errors_from_str(cls, record: str) -> List[Dict[str, Any]]:
        # I'm only going to bother to map the actual errors
        result = []
        for i in range(3):
            e = record[456+i*7:456+7+i*7]
            if e[0] == " ":
                # no more errors
                break
            else:
                # I'm only going to bother with fields that I actually encounter
                key_numeric = e[3:5]
                key = ""
                error = e[5:7]
                value = ""

                if key_numeric == "00":
                    continue # TODO?

                if key_numeric == "01":
                    # see mail 20240228
                    # only present to indicate there    
                    # is an error in this record
                    continue
                elif key_numeric == "04":
                    key = "Nomenclatuurcode"
                    value = record[9:16]
                elif key_numeric == "19":
                    key = "Nummer akkoord"
                    value = record[131:151]
                elif key_numeric == "99":
                    key = "Controlecijfer record"
                    value = record[348:350]
                else:
                    raise Exception(f"Numeric key {key_numeric} not yet mapped for Record52")

                e_dict = cls._error_shared(key, error, value, e[0])
            
            if e_dict not in [r.dict() for r in result]:
                # sometimes duplicate errors
                result.append(ErrorMessage(**e_dict))
        return result
    
    def __str__(self):
        to_str = ""
        assert len(self.record) == 2
        to_str += self.record
        assert len(self.num_record) == 6
        to_str += self.num_record
        assert len(self.reden_manuele_invoering) == 1
        to_str += self.reden_manuele_invoering
        assert len(self.nomenclatuur) == 7
        to_str += self.nomenclatuur
        assert len(self.datum_verstrekking) == 8
        to_str += self.datum_verstrekking
        assert len(self.datum_lezing_identiteitsdocument) == 8
        to_str += self.datum_lezing_identiteitsdocument

        reserve = "0" * 3
        to_str += reserve

        assert len(self.identificatie_rechthebbende_1) == 12
        to_str += self.identificatie_rechthebbende_1
        assert len(self.identificatie_rechthebbende_2) == 1
        to_str += self.identificatie_rechthebbende_2
        assert len(self.type_lezing_identiteitsdocument) == 1
        to_str += self.type_lezing_identiteitsdocument
        assert len(self.type_drager_identiteitsdocument) == 1
        to_str += self.type_drager_identiteitsdocument
        assert len(self.reden_gebruik_vignet) == 1
        to_str += self.reden_gebruik_vignet
        assert len(self.uur_lezing_identiteitsdocument) == 4
        to_str += self.uur_lezing_identiteitsdocument

        reserve = "0" * 12
        to_str += reserve

        assert len(self.riziv_nummer) == 12
        to_str += self.riziv_nummer
        assert len(self.serienummer_drager) == 15
        to_str += self.serienummer_drager
        assert len(self.nummer_bewijsstuk) == 25
        to_str += self.nummer_bewijsstuk
        assert len(self.uniek_nummer_medische_beeldvorming) == 12
        to_str += self.uniek_nummer_medische_beeldvorming
        assert len(self.nummer_akkoord) == 20
        to_str += self.nummer_akkoord

        reserve = "0" * 197 # doc incorrect
        to_str += reserve

        control = calculate_control(to_str)
        to_str += control
        return to_str
    
class Record80(BaseModel):
    record: Optional[str] = "80"
    num_record: Optional[str] = "000005"
    uur_van_opname: Optional[str] = "0000000"
    datum_van_opname: Optional[str] = "00000000"
    datum_van_ontslag: Optional[str] = "00000000"
    nummer_ziekenfonds_aansluiting: str
    identificatie_rechthebbende_1: str
    identificatie_rechthebbende_2: str
    geslacht_rechthebbende: str
    type_factuur: str
    dienst_721_bis: Optional[str] = "000"
    nummer_facturerende_instelling: str
    bedrag_financieel_rekeningnummer_b: str
    reden_behandeling: Optional[str] = "0000"
    nummer_ziekenfonds_bestemming: str
    bedrag_financieel_rekeningnummer_a: str
    factuurdatum: Optional[str] = "00000000"
    uur_van_ontslag: Optional[str] = "00000"
    nummer_individuele_factuur_1: Optional[str] = "00000"
    nummer_individuele_factuur_2: Optional[str] = "0000000"
    persoonlijk_aandeel_patient: str
    referentie_instelling: str
    bedrag_supplement: str
    flag_identificatie_rechthebbende: Optional[str] = "1"
    voorschot_financieel_rekeningnummer_a: str
    control_invoice: str

    @classmethod
    def _error_shared(cls, key, error, value, refusal_code) -> Optional[Dict[str, Any]]:
        if error == "00":
            return None
        
        _ERROR_CONSTANTS = {
            "01": "Gegeven niet numeriek",
            "02": "Controlecijfer foutief",
            "03": "Gegeven niet toegelaten",
            "09": "Verboden karakters",
            "20": "Gegeven niet gekend in bestand ziekenfonds",
        }
        
        return {
            "type": "80",
            "key": key,
            "value": value,
            "error_code": error,
            "message": _ERROR_CONSTANTS.get(error),
            "verwerpingsletter": refusal_code
        }
    
    @classmethod
    def errors_from_str(cls, record: str) -> List[Dict[str, Any]]:
        # I'm only going to bother to map the actual errors
        result = []
        for i in range(3):
            e = record[456+i*7:456+7+i*7]
            if e[0] == " ":
                # no more errors
                break
            else:
                # I'm only going to bother with fields that I actually encounter
                key_numeric = e[3:5]
                key = ""
                error = e[5:7]
                value = ""
                if key_numeric == "00":
                    continue # TODO?

                if key_numeric == "98":
                    key = "Controlecijfer factuur"
                    value = record[346:348]
                elif key_numeric == "19":
                    key = "teken + bedrag financieel rekeningnummer a"
                    value = record[87:99]
                elif key_numeric == "27":
                    key = "teken + bedrag persoonlijk aandeel patient"
                    value = record[127:137]
                elif key_numeric == "30":
                    key = "teken + bedrag supplement"
                    value = record[164:166]
                elif key_numeric == "99":
                    key = "Controlecijfer record"
                    value = record[348:350]
                else:
                    raise Exception(f"Numeric key {key_numeric} not yet mapped for Record80")

                e_dict = cls._error_shared(key, error, value, e[0])
            result.append(ErrorMessage(**e_dict))
        return result
    
    def __str__(self):
        to_str = ""
        assert len(self.record) == 2
        to_str += self.record
        assert len(self.num_record) == 6
        to_str += self.num_record
        reserve = "0" * 1
        to_str += reserve

        assert len(self.uur_van_opname) == 7
        to_str += self.uur_van_opname
        assert len(self.datum_van_opname) == 8
        to_str += self.datum_van_opname
        assert len(self.datum_van_ontslag) == 8
        to_str += self.datum_van_ontslag

        assert len(self.nummer_ziekenfonds_aansluiting) == 3
        to_str += self.nummer_ziekenfonds_aansluiting
        assert len(self.identificatie_rechthebbende_1) == 12
        to_str += self.identificatie_rechthebbende_1
        assert len(self.identificatie_rechthebbende_2) == 1
        to_str += self.identificatie_rechthebbende_2
        assert len(self.geslacht_rechthebbende) == 1
        to_str += self.geslacht_rechthebbende
        assert len(self.type_factuur) == 1
        to_str += self.type_factuur

        reserve = "0" * 2
        to_str += reserve
        assert len(self.dienst_721_bis) == 3
        to_str += self.dienst_721_bis
        assert len(self.nummer_facturerende_instelling) == 12
        to_str += self.nummer_facturerende_instelling

        to_str += ("+" + self.bedrag_financieel_rekeningnummer_b.rjust(11, "0"))
        reserve = "0" * 1
        to_str += reserve
        assert len(self.reden_behandeling) == 4
        to_str += self.reden_behandeling
        assert len(self.nummer_ziekenfonds_bestemming) == 3
        to_str += self.nummer_ziekenfonds_bestemming
        to_str += ("+" + self.bedrag_financieel_rekeningnummer_a.rjust(11, "0"))

        assert len(self.factuurdatum) == 8
        to_str += self.factuurdatum
        assert len(self.uur_van_ontslag) == 5
        to_str += self.uur_van_ontslag
        reserve = "0" * 2
        to_str += reserve
        assert len(self.nummer_individuele_factuur_1) == 5
        to_str += self.nummer_individuele_factuur_1
        assert len(self.nummer_individuele_factuur_2) == 7
        to_str += self.nummer_individuele_factuur_2
        reserve = "0" * 1
        to_str += reserve
        to_str += ("+" + self.persoonlijk_aandeel_patient.rjust(9, "0"))
        to_str += self.referentie_instelling.ljust(25)
        reserve = "0" * 2
        to_str += reserve
        to_str += ("+" + self.bedrag_supplement.rjust(9, "0"))
        assert len(self.flag_identificatie_rechthebbende) == 1
        to_str += self.flag_identificatie_rechthebbende
        reserve = "0" * 7
        to_str += reserve
        to_str += ("+" + self.voorschot_financieel_rekeningnummer_a.rjust(11, "0"))
        reserve = "0" * 152
        to_str += reserve


        assert len(self.control_invoice) == 2
        to_str += self.control_invoice

        control_record = calculate_control(to_str)
        to_str += control_record
        return to_str

class Record90(BaseModel):
    record: Optional[str] = "90"
    num_record: Optional[str] = "000006"
    financieel_rekeningnummer_a_1: Optional[str] = "00000000"
    financieel_rekeningnummer_a_2: Optional[str] = "0000"
    zendingsnummer: str # nummer mutualiteit
    financieel_rekeningnummer_b: Optional[str] = "000000000000"
    nummer_derdebetalende: str
    bedrag_financieel_rekeningnummer_b: str
    bedrag_financieel_rekeningnummer_a: str
    date_creation: str
    kbo_number: Optional[str] = "0000000000"
    reference: str
    bic_bank: str
    iban_bank: str
    bic_bank_2: Optional[str] = ""
    iban_bank_2: Optional[str] = ""
    control_message: str

    @classmethod
    def _error_shared(cls, key, error, value, refusal_code) -> Optional[Dict[str, Any]]:
        if error == "00":
            return None
        
        _ERROR_CONSTANTS = {
            "01": "Gegeven niet numeriek",
            "02": "Controlecijfer foutief",
            "03": "Gegeven niet toegelaten",
            "09": "Verboden karakters",
            "20": "Gegeven niet gekend in bestand ziekenfonds",
        }
        
        return {
            "type": "90",
            "key": key,
            "value": value,
            "error_code": error,
            "message": _ERROR_CONSTANTS.get(error),
            "verwerpingsletter": refusal_code
        }
    
    @classmethod
    def errors_from_str(cls, record: str) -> List[Dict[str, Any]]:
        # I'm only going to bother to map the actual errors
        result = []
        for i in range(3):
            e = record[456+i*7:456+7+i*7]
            if e[0] == " ":
                # no more errors
                break
            else:
                # I'm only going to bother with fields that I actually encounter
                key_numeric = e[3:5]
                key = ""
                error = e[5:7]
                value = ""
                if key_numeric == "00":
                    continue # TODO?

                if key_numeric == "19":
                    key = "teken + totaal bedrag financieel rekeningnummer a"
                    value = record[87:99]
                elif key_numeric == "23":
                    key = "gefactureerde maand"
                    value = record[112:114]
                elif key_numeric == "98":
                    key = "controlecijfer factuur"
                    value = record[346:348]
                elif key_numeric == "99":
                    key = "controlecijfer record"
                    value = record[348:350]
                else:
                    raise Exception(f"Numeric key {key_numeric} not yet mapped for Record90")

                e_dict = cls._error_shared(key, error, value, e[0])
            result.append(ErrorMessage(**e_dict))
        return result
    
    def __str__(self):
        to_str = ""
        assert len(self.record) == 2
        to_str += self.record
        assert len(self.num_record) == 6
        to_str += self.num_record
        reserve = "0" * 8
        to_str += reserve
        assert len(self.financieel_rekeningnummer_a_1) == 8
        to_str += self.financieel_rekeningnummer_a_1
        assert len(self.financieel_rekeningnummer_a_2) == 4
        to_str += self.financieel_rekeningnummer_a_2

        reserve = "0" * 4
        to_str += reserve

        assert len(self.zendingsnummer) == 3
        to_str += self.zendingsnummer
        assert len(self.financieel_rekeningnummer_b) == 12
        to_str += self.financieel_rekeningnummer_b

        reserve = "0" * 8
        to_str += reserve

        assert len(self.nummer_derdebetalende) == 12
        to_str += self.nummer_derdebetalende
        to_str += ("+" + self.bedrag_financieel_rekeningnummer_b.rjust(11, "0"))
        reserve = "0" * 8
        to_str += reserve
        to_str += ("+" + self.bedrag_financieel_rekeningnummer_a.rjust(11, "0"))
        reserve = "0" * 8
        to_str += reserve

        to_str += ("0" + self.date_creation[:4]) # year
        to_str += self.date_creation[4:6] # month

        reserve = "0" * 13
        to_str += reserve

        assert len(self.kbo_number) == 10
        to_str += self.kbo_number

        to_str += self.reference.ljust(25)

        reserve = "0" * 4
        to_str += reserve

        # actually 8+1+1+1, but that's silly
        to_str += self.bic_bank.ljust(11)

        reserve = "0" * 1
        to_str += reserve

        # actually 1+3+12+10+2+6, but that's silly
        to_str += self.iban_bank.ljust(34)

        reserve = "0" * 6
        to_str += reserve

        to_str += self.bic_bank_2.ljust(11)

        reserve = "0" * 5
        to_str += reserve

        # reserve staatshervorming
        reserve = "0" * 34
        to_str += reserve

        reserve = "0" * 2
        to_str += reserve

        to_str += self.iban_bank_2.ljust(34)

        # reserve staatshervorming
        reserve = "0" * 11
        to_str += reserve

        # the remainder in one go
        reserve = "0" * 31
        to_str += reserve
        
        assert len(self.control_message) == 2
        to_str += self.control_message
        control_record = calculate_control(to_str)
        to_str += control_record
        return to_str


class Record91(BaseModel):
    recordtype: str
    error_recordtype: str
    nummer_mutualiteit: str
    error_nummer_mutualiteit: str
    nummer_verzamelfactuur: str
    error_nummer_verzamelfactuur: str

    teken_gevraagd_bedrag_rekening_a: str
    gevraagd_bedrag_rekening_a: str
    error_gevraagd_bedrag_rekening_a: str

    teken_gevraagd_bedrag_rekening_b: str
    gevraagd_bedrag_rekening_b: str
    error_gevraagd_bedrag_rekening_b: str

    teken_totaal_gevraagd_bedrag_rekening_a_b_c: str
    totaal_gevraagd_bedrag_rekening_a_b_c: str
    error_totaal_gevraagd_bedrag_rekening_a_b_c: str

    aantal_records: str
    error_aantal_records: str
    controle_nummer_per_mutualiteit: str
    error_controle_nummer_per_mutualiteit: str

    teken_aanvaard_bedrag_rekening_a: str
    aanvaard_bedrag_rekening_a: str
    error_aanvaard_bedrag_rekening_a: str
    teken_geweigerd_bedrag_rekening_a: str
    geweigerd_bedrag_rekening_a: str
    error_geweigerd_bedrag_rekening_a: str

    teken_aanvaard_bedrag_rekening_b: str
    aanvaard_bedrag_rekening_b: str
    error_aanvaard_bedrag_rekening_b: str
    teken_geweigerd_bedrag_rekening_b: str
    geweigerd_bedrag_rekening_b: str
    error_geweigerd_bedrag_rekening_b: str

    teken_totaal_aanvaard_bedrag_rekening_a_b_c: str
    totaal_aanvaard_bedrag_rekening_a_b_c: str
    error_totaal_aanvaard_bedrag_rekening_a_b_c: str
    teken_totaal_geweigerd_bedrag_rekening_a_b_c: str
    totaal_geweigerd_bedrag_rekening_a_b_c: str
    error_totaal_geweigerd_bedrag_rekening_a_b_c: str

    referentie_betaling_rekening_a: str
    error_referentie_betaling_rekening_a: str
    referentie_betaling_rekening_b: str
    error_referentie_betaling_rekening_b: str

    teken_gevraagd_bedrag_rekening_c: str
    gevraagd_bedrag_rekening_c: str
    error_gevraagd_bedrag_rekening_c: str
    teken_aanvaard_bedrag_rekening_c: str
    aanvaard_bedrag_rekening_c: str
    error_aanvaard_bedrag_rekening_c: str
    teken_geweigerd_bedrag_rekening_c: str
    geweigerd_bedrag_rekening_c: str
    error_geweigerd_bedrag_rekening_c: str

    referentie_betaling_rekening_c: str
    error_referentie_betaling_rekening_c: str

    @classmethod
    def from_str(cls, msg: str) -> "Record91":
        assert len(msg) == 800
        return Record91(
                recordtype=msg[:2],
                error_recordtype=msg[2:4],
                nummer_mutualiteit=msg[4:7],
                error_nummer_mutualiteit=msg[7:9],
                nummer_verzamelfactuur=msg[9:21],
                error_nummer_verzamelfactuur=msg[21:23],

                teken_gevraagd_bedrag_rekening_a=msg[23],
                gevraagd_bedrag_rekening_a=msg[24:35],
                error_gevraagd_bedrag_rekening_a=msg[35:37],

                teken_gevraagd_bedrag_rekening_b=msg[37],
                gevraagd_bedrag_rekening_b=msg[38:49],
                error_gevraagd_bedrag_rekening_b=msg[49:51],

                teken_totaal_gevraagd_bedrag_rekening_a_b_c=msg[51],
                totaal_gevraagd_bedrag_rekening_a_b_c=msg[52:63],
                error_totaal_gevraagd_bedrag_rekening_a_b_c=msg[63:65],

                aantal_records=msg[65:73],
                error_aantal_records=msg[73:75],
                controle_nummer_per_mutualiteit=msg[75:77],
                error_controle_nummer_per_mutualiteit=msg[77:79],

                teken_aanvaard_bedrag_rekening_a=msg[79],
                aanvaard_bedrag_rekening_a=msg[80:91],
                error_aanvaard_bedrag_rekening_a=msg[91:93],
                teken_geweigerd_bedrag_rekening_a=msg[93],
                geweigerd_bedrag_rekening_a=msg[94:105],
                error_geweigerd_bedrag_rekening_a=msg[105:107],

                teken_aanvaard_bedrag_rekening_b=msg[107],
                aanvaard_bedrag_rekening_b=msg[108:119],
                error_aanvaard_bedrag_rekening_b=msg[119:121],
                teken_geweigerd_bedrag_rekening_b=msg[121],
                geweigerd_bedrag_rekening_b=msg[121:133],
                error_geweigerd_bedrag_rekening_b=msg[133:135],

                teken_totaal_aanvaard_bedrag_rekening_a_b_c=msg[135],
                totaal_aanvaard_bedrag_rekening_a_b_c=msg[136:147],
                error_totaal_aanvaard_bedrag_rekening_a_b_c=msg[147:149],
                teken_totaal_geweigerd_bedrag_rekening_a_b_c=msg[149],
                totaal_geweigerd_bedrag_rekening_a_b_c=msg[150:161],
                error_totaal_geweigerd_bedrag_rekening_a_b_c=msg[161:163],

                referentie_betaling_rekening_a=msg[163:185],
                error_referentie_betaling_rekening_a=msg[185:187],
                referentie_betaling_rekening_b=msg[187:209],
                error_referentie_betaling_rekening_b=msg[209:211],

                teken_gevraagd_bedrag_rekening_c=msg[211],
                gevraagd_bedrag_rekening_c=msg[212:223],
                error_gevraagd_bedrag_rekening_c=msg[223:225],
                teken_aanvaard_bedrag_rekening_c=msg[225],
                aanvaard_bedrag_rekening_c=msg[226:237],
                error_aanvaard_bedrag_rekening_c=msg[237:239],
                teken_geweigerd_bedrag_rekening_c=msg[239],
                geweigerd_bedrag_rekening_c=msg[240:251],
                error_geweigerd_bedrag_rekening_c=msg[251:253],

                referentie_betaling_rekening_c=msg[253:275],
                error_referentie_betaling_rekening_c=msg[275:277],
        )
    
    # TODO Errors cf header/footer
    # and then append them to existing errors

class Record92(BaseModel):
    recordtype: str
    error_recordtype: str
    nummer_mutualiteit: str
    error_nummer_mutualiteit: str
    not_used: str
    error_not_used: str

    teken_totaal_gevraagde_bedragen_rekening_a: str
    totaal_gevraagde_bedragen_rekening_a: str
    error_totaal_gevraagde_bedragen_rekening_a: str

    teken_totaal_gevraagde_bedragen_rekening_b: str
    totaal_gevraagde_bedragen_rekening_b: str
    error_totaal_gevraagde_bedragen_rekening_b: str

    teken_totaal_gevraagde_bedragen_rekening_a_b_c: str
    totaal_gevraagde_bedragen_rekening_a_b_c: str
    error_totaal_gevraagde_bedragen_rekening_a_b_c: str

    aantal_registraties: str
    error_aantal_registraties: str
    controle_nummer_zending: str
    error_controle_nummer_zending: str

    teken_totaal_aanvaarde_bedragen_rekening_a: str
    totaal_aanvaarde_bedragen_rekening_a: str
    error_totaal_aanvaarde_bedragen_rekening_a: str
    teken_totaal_geweigerde_bedragen_rekening_a: str
    totaal_geweigerde_bedragen_rekening_a: str
    error_totaal_geweigerde_bedragen_rekening_a: str

    teken_totaal_aanvaarde_bedragen_rekening_b: str
    totaal_aanvaarde_bedragen_rekening_b: str
    error_totaal_aanvaarde_bedragen_rekening_b: str
    teken_totaal_geweigerde_bedragen_rekening_b: str
    totaal_geweigerde_bedragen_rekening_b: str
    error_totaal_geweigerde_bedragen_rekening_b: str

    teken_totaal_aanvaarde_bedragen_rekening_a_b_c: str
    totaal_aanvaarde_bedragen_rekening_a_b_c: str
    error_totaal_aanvaarde_bedragen_rekening_a_b_c: str
    teken_totaal_geweigerde_bedragen_rekening_a_b_c: str
    totaal_geweigerde_bedragen_rekening_a_b_c: str
    error_totaal_geweigerde_bedragen_rekening_a_b_c: str

    teken_gevraagd_bedrag_rekening_c: str
    gevraagd_bedrag_rekening_c: str
    error_gevraagd_bedrag_rekening_c: str
    teken_aanvaard_bedrag_rekening_c: str
    aanvaard_bedrag_rekening_c: str
    error_aanvaard_bedrag_rekening_c: str
    teken_geweigerd_bedrag_rekening_c: str
    geweigerd_bedrag_rekening_c: str
    error_geweigerd_bedrag_rekening_c: str

    @classmethod
    def from_str(cls, msg: str) -> "Record92":
        assert len(msg) == 800
        return Record92(
                recordtype=msg[:2],
                error_recordtype=msg[2:4],
                nummer_mutualiteit=msg[4:7],
                error_nummer_mutualiteit=msg[7:9],
                not_used=msg[9:21],
                error_not_used=msg[21:23],

                teken_totaal_gevraagde_bedragen_rekening_a=msg[23],
                totaal_gevraagde_bedragen_rekening_a=msg[24:35],
                error_totaal_gevraagde_bedragen_rekening_a=msg[35:37],

                teken_totaal_gevraagde_bedragen_rekening_b=msg[37],
                totaal_gevraagde_bedragen_rekening_b=msg[38:49],
                error_totaal_gevraagde_bedragen_rekening_b=msg[49:51],

                teken_totaal_gevraagde_bedragen_rekening_a_b_c=msg[51],
                totaal_gevraagde_bedragen_rekening_a_b_c=msg[52:63],
                error_totaal_gevraagde_bedragen_rekening_a_b_c=msg[63:65],

                aantal_registraties=msg[65:73],
                error_aantal_registraties=msg[73:75],
                controle_nummer_zending=msg[75:77],
                error_controle_nummer_zending=msg[77:79],

                teken_totaal_aanvaarde_bedragen_rekening_a=msg[79],
                totaal_aanvaarde_bedragen_rekening_a=msg[80:91],
                error_totaal_aanvaarde_bedragen_rekening_a=msg[91:93],
                teken_totaal_geweigerde_bedragen_rekening_a=msg[93],
                totaal_geweigerde_bedragen_rekening_a=msg[94:105],
                error_totaal_geweigerde_bedragen_rekening_a=msg[105:107],

                teken_totaal_aanvaarde_bedragen_rekening_b=msg[107],
                totaal_aanvaarde_bedragen_rekening_b=msg[108:119],
                error_totaal_aanvaarde_bedragen_rekening_b=msg[119:121],
                teken_totaal_geweigerde_bedragen_rekening_b=msg[121],
                totaal_geweigerde_bedragen_rekening_b=msg[121:133],
                error_totaal_geweigerde_bedragen_rekening_b=msg[133:135],

                teken_totaal_aanvaarde_bedragen_rekening_a_b_c=msg[135],
                totaal_aanvaarde_bedragen_rekening_a_b_c=msg[136:147],
                error_totaal_aanvaarde_bedragen_rekening_a_b_c=msg[147:149],
                teken_totaal_geweigerde_bedragen_rekening_a_b_c=msg[149],
                totaal_geweigerde_bedragen_rekening_a_b_c=msg[150:161],
                error_totaal_geweigerde_bedragen_rekening_a_b_c=msg[161:163],

                teken_gevraagd_bedrag_rekening_c=msg[163],
                gevraagd_bedrag_rekening_c=msg[164:175],
                error_gevraagd_bedrag_rekening_c=msg[175:177],
                teken_aanvaard_bedrag_rekening_c=msg[177],
                aanvaard_bedrag_rekening_c=msg[178:189],
                error_aanvaard_bedrag_rekening_c=msg[189:191],
                teken_geweigerd_bedrag_rekening_c=msg[191],
                geweigerd_bedrag_rekening_c=msg[192:2023],
                error_geweigerd_bedrag_rekening_c=msg[203:205],
        )
    
class Footer95(BaseModel):
    name: Optional[str] = "95"
    error_name: Optional[str] = "00"
    nummer_mutualiteit: str
    error_nummer_mutualiteit: Optional[str] = "00"
    nummer_verzamelfactuur: Optional[str] = "3"
    error_nummer_verzamelfactuur: Optional[str] = "00"
    teken_gevraagd_bedrag_a: Optional[str] = "+"
    gevraagd_bedrag_a: str
    error_gevraagd_bedrag_a: Optional[str] = "00"
    teken_gevraagd_bedrag_b: Optional[str] = "+"
    gevraagd_bedrag_b: str
    error_gevraagd_bedrag_b: Optional[str] = "00"
    teken_gevraagd_bedrag_a_b_c: Optional[str] = "+"
    gevraagd_bedrag_a_b_c: Optional[str] = "0"
    error_gevraagd_bedrag_a_b_c: Optional[str] = "00"
    aantal_records: str
    error_aantal_records: Optional[str] = "00"
    controle_nummer_per_mutualiteit: str
    error_controle_nummer: Optional[str] = "00"

    @classmethod
    def from_str(cls, msg: str) -> "Footer95":
        assert len(msg) == 350
        return Footer95(
            name = msg[:2],
            error_name = msg[2:4],
            nummer_mutualiteit = msg[4:7],
            error_nummer_mutualiteit = msg[7:9],
            nummer_verzamelfactuur=msg[9:21],
            error_nummer_verzamelfactuur=msg[21:23],
            teken_gevraagd_bedrag_a=msg[23:24],
            gevraagd_bedrag_a=msg[24:35],
            error_gevraagd_bedrag_a=msg[35:37],
            teken_gevraagd_bedrag_b=msg[37:38],
            gevraagd_bedrag_b=msg[38:49],
            error_gevraagd_bedrag_b=msg[49:51],
            teken_gevraagd_bedrag_a_b_c=msg[51:52],
            gevraagd_bedrag_a_b_c=msg[52:63],
            error_gevraagd_bedrag_a_b_c=msg[63:65],
            aantal_records=msg[65:73],
            error_aantal_records=msg[73:75],
            controle_nummer_per_mutualiteit=msg[75:77],
            error_controle_nummer=msg[77:79],
        )
    
    def __str__(self):
        to_str = ""
        assert len(self.name) == 2
        to_str += self.name
        assert len(self.error_name) == 2
        to_str += self.error_name
        assert len(self.nummer_mutualiteit) == 3
        to_str += self.nummer_mutualiteit
        assert len(self.error_nummer_mutualiteit) == 2
        to_str += self.error_nummer_mutualiteit
        to_str += self.nummer_verzamelfactuur.rjust(12, "0")
        assert len(self.error_nummer_verzamelfactuur) == 2
        to_str += self.error_nummer_verzamelfactuur
        assert len(self.teken_gevraagd_bedrag_a) == 1
        to_str += self.teken_gevraagd_bedrag_a
        to_str += self.gevraagd_bedrag_a.rjust(11, "0")
        assert len(self.error_gevraagd_bedrag_a) == 2
        to_str += self.error_gevraagd_bedrag_a
        assert len(self.teken_gevraagd_bedrag_b) == 1
        to_str += self.teken_gevraagd_bedrag_b
        to_str += self.gevraagd_bedrag_b.rjust(11, "0")
        assert len(self.error_gevraagd_bedrag_b) == 2
        to_str += self.error_gevraagd_bedrag_b
        assert len(self.teken_gevraagd_bedrag_a_b_c) == 1
        to_str += self.teken_gevraagd_bedrag_a_b_c
        to_str += self.gevraagd_bedrag_a_b_c.rjust(11, "0")
        assert len(self.error_gevraagd_bedrag_a_b_c) == 2
        to_str += self.error_gevraagd_bedrag_a_b_c

        to_str += self.aantal_records.rjust(8, "0")
        assert len(self.error_aantal_records) == 2
        to_str += self.error_aantal_records

        assert len(self.controle_nummer_per_mutualiteit) == 2
        to_str += self.controle_nummer_per_mutualiteit
        assert len(self.error_controle_nummer) == 2
        to_str += self.error_controle_nummer

        # bedrag c we fill with 0s
        reserve = " ".ljust(14)
        to_str += reserve

        reserve = " ".ljust(257)
        to_str += reserve
        return to_str

    def _error_shared(self, key, error, value) -> Optional[Dict[str, Any]]:
        if error == "00":
            return None
        
        return {
            "type": self.name,
            "key": key,
            "value": value,
            "error_code": error,
            "message": ERROR_CONSTANTS.get(error)
        }

    def _error_name(self) -> Optional[Dict[str, Any]]:
        error = self.error_name
        value = self.name
        return self._error_shared("record type", error, value)

    def _error_nummer_mutualiteit(self) -> Optional[Dict[str, Any]]:
        error = self.error_nummer_mutualiteit
        value = self.nummer_mutualiteit
        error_dict = self._error_shared("nummer mutualiteit", error, value)

        if error_dict is None or (error_dict.get("message") is not None and error_dict.get("messages") != "20"):
            return error_dict
        
        msg = ""
        if error == "20":
            msg = "Nummer onbekend"
        elif error == "21":
            msg = "Nummer ziekenfonds niet teruggevonden in het detail van de factuur"
        error_dict["message"] = msg
        return error_dict
    
    def _error_nummer_verzamelfactuur(self) -> Optional[Dict[str, Any]]:
        error = self.error_nummer_verzamelfactuur
        value = self.nummer_verzamelfactuur
        return self._error_shared("nummer verzamelfactuur", error, value)

    def _error_gevraagd_bedrag_a(self) -> Optional[Dict[str, Any]]:
        error = self.error_gevraagd_bedrag_a
        value = self.teken_gevraagd_bedrag_a + self.gevraagd_bedrag_a
        error_dict = self._error_shared("gevraagd bedrag a", error, value)

        if error_dict is None or error_dict.get("message") is not None:
            return error_dict
        
        msg = ""
        if error == "40":
            msg = "Tekencode is niet gelijk aan “+” of niet gelijk aan “-“"
        elif error == "41":
            msg = "Geen overeenstemming tussen het bedrag in deze zone en het totaal van het facturatiebestand voor het ziekenfonds"
        error_dict["message"] = msg
        return error_dict

    def _error_gevraagd_bedrag_b(self) -> Optional[Dict[str, Any]]:
        error = self.error_gevraagd_bedrag_b
        value = self.teken_gevraagd_bedrag_b + self.gevraagd_bedrag_b
        error_dict = self._error_shared("gevraagd bedrag b", error, value)

        if error_dict is None or error_dict.get("message") is not None:
            return error_dict
        
        msg = ""
        if error == "15":
            msg = "Zone # 0 indien de uitgever geen verzorgingsinstelling is"
        elif error == "40":
            msg = "Tekencode is niet gelijk aan “+” of niet gelijk aan “-“"
        elif error == "41":
            msg = "Geen overeenstemming tussen het bedrag in deze zone en het totaal van het facturatiebestand voor het ziekenfonds"
        error_dict["message"] = msg
        return error_dict

    def _error_gevraagd_bedrag_a_b_c(self) -> Optional[Dict[str, Any]]:
        error = self.error_gevraagd_bedrag_a_b_c
        value = self.teken_gevraagd_bedrag_a_b_c + self.gevraagd_bedrag_a_b_c
        error_dict = self._error_shared("gevraagd bedrag a+b+c", error, value)

        if error_dict is None or error_dict.get("message") is not None:
            return error_dict
        
        msg = ""
        if error == "20":
            msg = "Bedrag # som van de bedragen rekening A, rekening B en rekening C"
        elif error == "40":
            msg = "Tekencode is niet gelijk aan “+” of niet gelijk aan “-“"
        error_dict["message"] = msg
        return error_dict
    
    def _error_aantal_records(self) -> Optional[Dict[str, Any]]:
        error = self.error_aantal_records
        value = self.aantal_records
        return self._error_shared("aantal detailrecords", error, value)

    def _error_controle_nummer(self) -> Optional[Dict[str, Any]]:
        error = self.error_controle_nummer
        value = self.controle_nummer_per_mutualiteit
        return self._error_shared("controle nummer per mutualiteit", error, value)
    
    def errors(self) -> List[Dict[str, Any]]:
        errors = [
            self._error_name(),
            self._error_nummer_mutualiteit(),
            self._error_nummer_verzamelfactuur(),
            self._error_gevraagd_bedrag_a(),
            self._error_gevraagd_bedrag_b(),
            self._error_gevraagd_bedrag_a_b_c(),
            self._error_aantal_records(),
            self._error_controle_nummer()
        ]
        return [ErrorMessage(**e) for e in errors if e is not None]

class Footer96(BaseModel):
    name: Optional[str] = "96"
    error_name: Optional[str] = "00"
    nummer_mutualiteit: str
    error_nummer_mutualiteit: Optional[str] = "00"
    error_nummer_verzamelfactuur: Optional[str] = "00"
    teken_gevraagd_bedrag_a: Optional[str] = "+"
    gevraagd_bedrag_a: str
    error_gevraagd_bedrag_a: Optional[str] = "00"
    teken_gevraagd_bedrag_b: Optional[str] = "+"
    gevraagd_bedrag_b: str
    error_gevraagd_bedrag_b: Optional[str] = "00"
    teken_gevraagd_bedrag_a_b_c: Optional[str] = "+"
    gevraagd_bedrag_a_b_c: Optional[str] = "0"
    error_gevraagd_bedrag_a_b_c: Optional[str] = "00"
    aantal_records: str
    error_aantal_records: Optional[str] = "00"
    controle_nummer_per_mutualiteit: str
    error_controle_nummer: Optional[str] = "00"
    
    @classmethod
    def from_str(cls, msg: str) -> "Footer96":
        assert len(msg) == 350
        return Footer96(
            name = msg[:2],
            error_name = msg[2:4],
            nummer_mutualiteit = msg[4:7],
            error_nummer_mutualiteit = msg[7:9],
            error_nummer_verzamelfactuur=msg[21:23],
            teken_gevraagd_bedrag_a=msg[23:24],
            gevraagd_bedrag_a=msg[24:35],
            error_gevraagd_bedrag_a=msg[35:37],
            teken_gevraagd_bedrag_b=msg[37:38],
            gevraagd_bedrag_b=msg[38:49],
            error_gevraagd_bedrag_b=msg[49:51],
            teken_gevraagd_bedrag_a_b_c=msg[51:52],
            gevraagd_bedrag_a_b_c=msg[52:63],
            error_gevraagd_bedrag_a_b_c=msg[63:65],
            aantal_records=msg[65:73],
            error_aantal_records=msg[73:75],
            controle_nummer_per_mutualiteit=msg[75:77],
            error_controle_nummer=msg[77:79],
        )
    
    def __str__(self):
        to_str = ""
        assert len(self.name) == 2
        to_str += self.name
        assert len(self.error_name) == 2
        to_str += self.error_name
        assert len(self.nummer_mutualiteit) == 3
        to_str += self.nummer_mutualiteit
        assert len(self.error_nummer_mutualiteit) == 2
        to_str += self.error_nummer_mutualiteit

        reserve = "0" * 12
        to_str += reserve
        assert len(self.error_nummer_verzamelfactuur) == 2
        to_str += self.error_nummer_verzamelfactuur
        assert len(self.teken_gevraagd_bedrag_a) == 1
        to_str += self.teken_gevraagd_bedrag_a
        to_str += self.gevraagd_bedrag_a.rjust(11, "0")
        assert len(self.error_gevraagd_bedrag_a) == 2
        to_str += self.error_gevraagd_bedrag_a
        assert len(self.teken_gevraagd_bedrag_b) == 1
        to_str += self.teken_gevraagd_bedrag_b
        to_str += self.gevraagd_bedrag_b.rjust(11, "0")
        assert len(self.error_gevraagd_bedrag_b) == 2
        to_str += self.error_gevraagd_bedrag_b
        assert len(self.teken_gevraagd_bedrag_a_b_c) == 1
        to_str += self.teken_gevraagd_bedrag_a_b_c
        to_str += self.gevraagd_bedrag_a_b_c.rjust(11, "0")
        assert len(self.error_gevraagd_bedrag_a_b_c) == 2
        to_str += self.error_gevraagd_bedrag_a_b_c

        to_str += self.aantal_records.rjust(8, "0")
        assert len(self.error_aantal_records) == 2
        to_str += self.error_aantal_records

        assert len(self.controle_nummer_per_mutualiteit) == 2
        to_str += self.controle_nummer_per_mutualiteit
        assert len(self.error_controle_nummer) == 2
        to_str += self.error_controle_nummer

        # bedrag c we fill with 0s
        reserve = " ".ljust(14)
        to_str += reserve

        reserve = " ".ljust(257)
        to_str += reserve
        return to_str


    def _error_shared(self, key, error, value) -> Optional[Dict[str, Any]]:
        if error == "00":
            return None
        
        return {
            "type": self.name,
            "key": key,
            "value": value,
            "error_code": error,
            "message": ERROR_CONSTANTS.get(error)
        }

    def _error_name(self) -> Optional[Dict[str, Any]]:
        error = self.error_name
        value = self.name
        return self._error_shared("record type", error, value)

    def _error_nummer_mutualiteit(self) -> Optional[Dict[str, Any]]:
        error = self.error_nummer_mutualiteit
        value = self.nummer_mutualiteit
        error_dict = self._error_shared("nummer mutualiteit", error, value)

        if error_dict is None or (error_dict.get("message") is not None and error_dict.get("messages") != "20"):
            return error_dict
        
        msg = ""
        if error == "20":
            msg = "Nummer onbekend of codificatie fout"
        error_dict["message"] = msg
        return error_dict
    
    def _error_nummer_verzamelfactuur(self) -> Optional[Dict[str, Any]]:
        error = self.error_nummer_verzamelfactuur
        value = ""
        return self._error_shared("nummer verzamelfactuur", error, value)

    def _error_gevraagd_bedrag_a(self) -> Optional[Dict[str, Any]]:
        error = self.error_gevraagd_bedrag_a
        value = self.teken_gevraagd_bedrag_a + self.gevraagd_bedrag_a
        error_dict = self._error_shared("gevraagd bedrag a", error, value)

        if error_dict is None or error_dict.get("message") is not None:
            return error_dict
        
        msg = ""
        if error == "40":
            msg = "Tekencode is niet gelijk aan “+” of niet gelijk aan “-“"
        error_dict["message"] = msg
        return error_dict

    def _error_gevraagd_bedrag_b(self) -> Optional[Dict[str, Any]]:
        error = self.error_gevraagd_bedrag_b
        value = self.teken_gevraagd_bedrag_b + self.gevraagd_bedrag_b
        error_dict = self._error_shared("gevraagd bedrag b", error, value)

        if error_dict is None or error_dict.get("message") is not None:
            return error_dict
        
        msg = ""
        if error == "15":
            msg = "Zone # 0 indien de uitgever geen verzorgingsinstelling is"
        elif error == "40":
            msg = "Tekencode is niet gelijk aan “+” of niet gelijk aan “-“"
        error_dict["message"] = msg
        return error_dict

    def _error_gevraagd_bedrag_a_b_c(self) -> Optional[Dict[str, Any]]:
        error = self.error_gevraagd_bedrag_a_b_c
        value = self.teken_gevraagd_bedrag_a_b_c + self.gevraagd_bedrag_a_b_c
        error_dict = self._error_shared("gevraagd bedrag a+b+c", error, value)

        if error_dict is None or error_dict.get("message") is not None:
            return error_dict
        
        msg = ""
        if error == "20":
            msg = "Bedrag # bedrag rekening A, bedrag rekening B en rekening C"
        elif error == "40":
            msg = "Tekencode is niet gelijk aan “+” of niet gelijk aan “-“"
        error_dict["message"] = msg
        return error_dict
    
    def _error_aantal_records(self) -> Optional[Dict[str, Any]]:
        error = self.error_aantal_records
        value = self.aantal_records
        return self._error_shared("aantal detailrecords", error, value)

    def _error_controle_nummer(self) -> Optional[Dict[str, Any]]:
        error = self.error_controle_nummer
        value = self.controle_nummer_per_mutualiteit
        return self._error_shared("controle nummer per mutualiteit", error, value)
    
    def errors(self) -> List[Dict[str, Any]]:
        errors = [
            self._error_name(),
            self._error_nummer_mutualiteit(),
            self._error_nummer_verzamelfactuur(),
            self._error_gevraagd_bedrag_a(),
            self._error_gevraagd_bedrag_b(),
            self._error_gevraagd_bedrag_a_b_c(),
            self._error_aantal_records(),
            self._error_controle_nummer()
        ]
        return [ErrorMessage(**e) for e in errors if e is not None]
    
class Message200(BaseModel):
    header_200: Header200
    header_300: Header300
    record_10: Record10
    record_20: Record20
    record_50s: List[Record50]
    record_51s: Optional[List[Record51]] = []
    record_52s: Optional[List[Record52]] = []
    record_80: Record80
    record_90: Record90
    footer_95: Footer95
    footer_96: Footer96

    def from_str(self):
        raise NotImplementedError
    
    def __str__(self):
        # add assertions
        to_str = f'{str(self.header_200)}{str(self.header_300)}'
        to_str += str(self.record_10)
        to_str += str(self.record_20)
        
        for a in self.record_50s:
            to_str += str(a)
        for b in self.record_51s:
            to_str += str(b)
        for c in self.record_52s:
            to_str += str(c)
        to_str += str(self.record_80)
        to_str += str(self.record_90)
        to_str += str(self.footer_95)
        to_str += str(self.footer_96)
        return to_str
