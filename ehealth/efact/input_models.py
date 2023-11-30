from pydantic import BaseModel
from typing import Optional, List

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
        to_str += self.referentiegegevens_netwerk_1.ljust(6, "0")
        to_str += self.referentiegegevens_netwerk_2.ljust(11, "0")
        to_str += self.referentiegegevens_netwerk_3.ljust(1, "0")
        to_str += self.referentiegegevens_netwerk_4.ljust(4, "0")
        to_str += self.referentiegegevens_netwerk_5.ljust(26, "0")
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

        control = "01" # constant?
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
    dienstcode: Optional[str] = "990" # for test??
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
    norm_voorschrijver: Optional[str] = "0"
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
        assert len(self.identificatie_voorschrijver) == 12
        to_str += self.identificatie_voorschrijver
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

        control = "06" # constant?
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

        control = "35" # constant?
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


        control_invoice = "13" # constant?
        to_str += control_invoice

        control_record = "62" # constant?
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

        control_message = "13" # constant?
        to_str += control_message
        control_record = "52" # constant?
        to_str += control_record
        return to_str

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

class Message200(BaseModel):
    header_200: Header200
    header_300: Header300
    record_10: Record10
    record_20: Record20
    record_50s: List[Record50]
    record_51s: List[Record51]
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

        assert len(self.record_50s) == len(self.record_51s)
        for a,b in zip(self.record_50s, self.record_51s):
            to_str += str(a)
            to_str += str(b)
        to_str += str(self.record_80)
        to_str += str(self.record_90)
        to_str += str(self.footer_95)
        to_str += str(self.footer_96)
        return to_str
