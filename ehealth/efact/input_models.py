from pydantic import BaseModel
from typing import Optional

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
    inhoud_facturatie: str # code mutualiteit?
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

        control = "20" # constant?
        to_str += control

        return to_str
    
class Message200(BaseModel):
    header_200: Header200
    header_300: Header300
    record_10: Record10

    remainder: str

    def from_str(self):
        raise NotImplementedError
    
    def __str__(self):
        # add assertions
        assert len(f'{str(self.header_200)}{str(self.header_300)}') == 227
        return f'{str(self.header_200)}{str(self.header_300)}{self.remainder}'
