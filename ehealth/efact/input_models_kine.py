from pydantic import BaseModel
from typing import Optional, List, Union, Any
import logging
import datetime
from .input_models import Header200, Header300, Record10, Record20, Record50, Record52, Record80, Record90, Footer95, Footer96, Message200, calculate_invoice_control
logger = logging.getLogger(__name__)

class Header200Kine(BaseModel):
    reference: str
    version: Optional[str] = "01"
    type: Optional[str] = "92" # 92 for test, 12 for prd

    def to_header_200(self) -> Header200:
        return Header200(
            reference=self.reference,
            version=self.version,
            type=self.type
        )


class Header300Kine(BaseModel):
    num_invoice: str
    date_invoice: datetime.date
    is_test: Optional[bool] = True
    name_contact: str
    first_name_contact: str
    tel_contact: str
    hospital_care: Optional[bool] = False
    type_invoicing: Optional[str] = "01" # 1 bestand, 1 rekening

    def to_header_300(self) -> Header300:
        date_invoice = str(self.date_invoice.year) + str(self.date_invoice.month).rjust(2, "0") + str(self.date_invoice.day).rjust(2, "0")
        year_and_month = date_invoice[:6]
        return Header300(
            year_and_month=year_and_month,
            num_invoice=self.num_invoice,
            date_invoice=date_invoice,
            version_instructions="9991999" if self.is_test else "0001999",
            name_contact=self.name_contact,
            first_name_contact=self.first_name_contact,
            tel_contact=self.tel_contact,
            type_invoice="01" if self.hospital_care else "03",
            type_invoicing=self.type_invoicing
        )
    
class Record10Kine(BaseModel):
    is_test: Optional[bool] = True
    zendingsnummer: Optional[str] = "500" # no idea how this works
    nummer_derdebetalende: str # riziv nummer facturerende derde (maw riziv kine ...)
    beroepscode_facturerende_derde: str = "000" # TODO verplicht vanaf april! zie https://www.riziv.fgov.be/SiteCollectionDocuments/bevoegdheidscodes_kinesitherapeuten.pdf
    date_creation: datetime.date
    kbo_number: Optional[str] = "0000000000"
    bic_bank: str
    iban_bank: str

    def to_record_10(self) -> Record10:
        date_creation = str(self.date_creation.year) + str(self.date_creation.month).rjust(2, "0") + str(self.date_creation.day).rjust(2, "0")

        return Record10(
            num_record="000001",
            indexcode="0",
            version_file="9991999" if self.is_test else "0001999",
            inhoud_facturatie="040",
            zendingsnummer=self.zendingsnummer,
            reference="",
            nummer_derdebetalende=self.nummer_derdebetalende.rjust(12, "0"),
            beroepscode_facturerende_derde=self.beroepscode_facturerende_derde,
            date_creation=date_creation,
            kbo_number=self.kbo_number,
            bic_bank=self.bic_bank,
            iban_bank=self.iban_bank
        )

class Record20Kine(BaseModel):
    num_record: str
    nummer_ziekenfonds_aansluiting: str
    insz_rechthebbende: str
    identificatie_rechthebbende_2: str # hoe wordt dit opgevuld
    geslacht_rechthebbende: str # 1 of 2
    hospital_care: Optional[bool] = False
    nummer_facturerende_instelling: str # riziv kine
    instelling_van_verblijf: Optional[str] = "000000000000" # indien hospitalisatie ...
    code_stuiten_verjaringstermijn: Optional[str] = "0"
    reden_behandeling: Optional[str] = "0000"
    nummer_ziekenfonds_bestemming: str
    nummer_individuele_factuur_1: str # eigen volgnummer
    cg1_cg2: str # op te halen uit MDA denk ik?
    referentiegegevens_netwerk_1: Optional[str] = "" # nummer verbintenis, zie MDA niet zeker of ik enkel _1 nodig heb

    def to_record_20(self) -> Record20:
        return Record20(
            num_record=self.num_record,
            nummer_ziekenfonds_aansluiting=self.nummer_ziekenfonds_aansluiting,
            identificatie_rechthebbende_1=self.insz_rechthebbende.rjust(12, "0"),
            identificatie_rechthebbende_2=self.identificatie_rechthebbende_2,
            geslacht_rechthebbende=self.geslacht_rechthebbende,
            type_factuur="1" if self.hospital_care else "3",
            dienst_721_bis="002" if self.hospital_care else "000",
            nummer_facturerende_instelling=self.nummer_facturerende_instelling.rjust(12, "0"),
            instelling_van_verblijf=self.instelling_van_verblijf,
            code_stuiten_verjaringstermijn=self.code_stuiten_verjaringstermijn,
            reden_behandeling=self.reden_behandeling,
            nummer_ziekenfonds_bestemming=self.nummer_ziekenfonds_bestemming,
            nummer_individuele_factuur_1=self.nummer_individuele_factuur_1,
            cg1_cg2=self.cg1_cg2,
            referentie_instelling='',
            referentiegegevens_netwerk_1=self.referentiegegevens_netwerk_1
        )
    
class Record50Kine(BaseModel):
    num_record: Optional[str] = "000003"
    nomenclatuur: str
    datum_eerste_verstrekking: datetime.date
    nummer_ziekenfonds_rechthebbende: str
    insz_rechthebbende: str
    identificatie_rechthebbende_2: str
    geslacht_rechthebbende: str
    hospital_care: Optional[bool] = False
    plaats_van_verstrekking: Optional[str] = "000000000000" # TODO not sure we will get away with this
    identificatie_verstrekker: str
    norm_verstrekker: Optional[str] = "1" # meestal 1 https://metadata.aim-ima.be/nl/app/vars/SS00340_Gz
    betrekkelijke_verstrekking_1: Optional[str] = "0000" # always 0 seems fine to me
    betrekkelijke_verstrekking_2: Optional[str] = "000" # always 0 seems fine to me
    bedrag_verzekeringstegemoetkoming: str
    datum_voorschrift: datetime.date
    persoonlijk_aandeel_patient: str
    bedrag_supplement: str
    code_facturering_persoonlijk_aandeel_of_supplement: Optional[str] = 0 # 0 indien patiënt zelf betaald zie https://www.riziv.fgov.be/SiteCollectionDocuments/instructies_elektronische_facturatiegegevens.pdf p 491
    geconventioneerde_verstrekker: Optional[bool] = True
    identificatie_voorschrijver: str
    norm_voorschrijver: Optional[str] = "1"

    def to_record_50(self) -> Record50:
        datum_eerste_verstrekking = str(self.datum_eerste_verstrekking.year) + str(self.datum_eerste_verstrekking.month).rjust(2, "0") + str(self.datum_eerste_verstrekking.day).rjust(2, "0")
        datum_voorschrift = str(self.datum_voorschrift.year) + str(self.datum_voorschrift.month).rjust(2, "0") + str(self.datum_voorschrift.day).rjust(2, "0")

        return Record50(
            num_record=self.num_record,
            nomenclatuur=self.nomenclatuur,
            datum_eerste_verstrekking=datum_eerste_verstrekking,
            datum_laatste_verstrekking=datum_eerste_verstrekking,
            nummer_ziekenfonds_rechthebbende=self.nummer_ziekenfonds_rechthebbende,
            identificatie_rechthebbende_1=self.insz_rechthebbende.rjust(12, "0"),
            identificatie_rechthebbende_2=self.identificatie_rechthebbende_2,
            geslacht_rechthebbende=self.geslacht_rechthebbende,
            dienstcode="002" if self.hospital_care else "990",
            plaats_van_verstrekking=self.plaats_van_verstrekking,
            identificatie_verstrekker=self.identificatie_verstrekker.rjust(12, "0"),
            norm_verstrekker=self.norm_verstrekker,
            betrekkelijke_verstrekking_1=self.betrekkelijke_verstrekking_1,
            betrekkelijke_verstrekking_2=self.betrekkelijke_verstrekking_2,
            bedrag_verzekeringstegemoetkoming=self.bedrag_verzekeringstegemoetkoming,
            datum_voorschrift=datum_voorschrift,
            aantal=1,
            persoonlijk_aandeel_patient=self.persoonlijk_aandeel_patient,
            referentie_instelling="",
            bedrag_supplement=self.bedrag_supplement,
            code_facturering_persoonlijk_aandeel_of_supplement=self.code_facturering_persoonlijk_aandeel_of_supplement,
            geconventioneerde_verstrekker="1" if self.geconventioneerde_verstrekker else "9",
            identificatie_voorschrijver=self.identificatie_voorschrijver,
            norm_voorschrijver=self.norm_voorschrijver
        )
    
class Record52Kine(BaseModel):
    num_record: Optional[str] = "000004"
    nomenclatuur: str
    datum_verstrekking: datetime.date
    insz_rechthebbende: str
    identificatie_rechthebbende_2: str
    riziv_nummer: str
    nummer_akkoord: str

    def to_record_52(self) -> Record52:
        datum_verstrekking = str(self.datum_verstrekking.year) + str(self.datum_verstrekking.month).rjust(2, "0") + str(self.datum_verstrekking.day).rjust(2, "0")

        return Record52(
            num_record=self.num_record,
            nomenclatuur=self.nomenclatuur,
            datum_verstrekking=datum_verstrekking,
            identificatie_rechthebbende_1=self.insz_rechthebbende.rjust(12, "0"),
            identificatie_rechthebbende_2=self.identificatie_rechthebbende_2,
            riziv_nummer=self.riziv_nummer.rjust(12, "0"),
            nummer_akkoord=self.nummer_akkoord
        )

class Record80Kine(BaseModel):
    num_record: Optional[str] = "000004"
    nummer_ziekenfonds_aansluiting: str
    insz_rechthebbende: str
    identificatie_rechthebbende_2: str # hoe wordt dit opgevuld
    geslacht_rechthebbende: str # 1 of 2
    hospital_care: Optional[bool] = False
    nummer_facturerende_instelling: str # riziv kine
    reden_behandeling: Optional[str] = "0000"
    nummer_ziekenfonds_bestemming: str
    nummer_individuele_factuur_1: str # eigen volgnummer
    cg1_cg2: str # op te halen uit MDA denk ik?
    referentiegegevens_netwerk_1: Optional[str] = "" # nummer verbintenis, zie MDA niet zeker of ik enkel _1 nodig heb
    totaal: str
    totaal_persoonlijk_aandeel: str
    totaal_supplement: str
    control_invoice: str

    def to_record_80(self) -> Record80:
        return Record80(
            num_record=self.num_record,
            nummer_ziekenfonds_aansluiting=self.nummer_ziekenfonds_aansluiting,
            identificatie_rechthebbende_1=self.insz_rechthebbende.rjust(12, "0"),
            identificatie_rechthebbende_2=self.identificatie_rechthebbende_2,
            geslacht_rechthebbende=self.geslacht_rechthebbende,
            type_factuur="1" if self.hospital_care else "3",
            dienst_721_bis="002" if self.hospital_care else "000",
            nummer_facturerende_instelling=self.nummer_facturerende_instelling.rjust(12, "0"),
            bedrag_financieel_rekeningnummer_b="0",
            reden_behandeling=self.reden_behandeling,
            nummer_ziekenfonds_bestemming=self.nummer_ziekenfonds_bestemming,
            bedrag_financieel_rekeningnummer_a=self.totaal,
            nummer_individuele_factuur_1=self.nummer_individuele_factuur_1,
            persoonlijk_aandeel_patient=self.totaal_persoonlijk_aandeel,
            referentie_instelling='',
            bedrag_supplement=self.totaal_supplement,
            voorschot_financieel_rekeningnummer_a="0",
            control_invoice=self.control_invoice
        )
    

class Record90Kine(BaseModel):
    num_record: Optional[str] = "000004"
    zendingsnummer: Optional[str] = "500" # no idea how this works
    nummer_derdebetalende: str # riziv nummer facturerende derde (maw riziv kine ...)
    totaal: str
    date_creation: datetime.date
    kbo_number: Optional[str] = "0000000000"
    bic_bank: str
    iban_bank: str
    control_message: str

    def to_record_90(self) -> Record90:
        date_creation = str(self.date_creation.year) + str(self.date_creation.month).rjust(2, "0") + str(self.date_creation.day).rjust(2, "0")

        return Record90(
            num_record=self.num_record,
            zendingsnummer=self.zendingsnummer,
            nummer_derdebetalende=self.nummer_derdebetalende.rjust(12, "0"),
            bedrag_financieel_rekeningnummer_b="0",
            bedrag_financieel_rekeningnummer_a=self.totaal,
            date_creation=date_creation,
            kbo_number=self.kbo_number,
            reference="", # optional
            bic_bank=self.bic_bank,
            iban_bank=self.iban_bank,
            control_message=self.control_message
        )
    
class Footer95Kine(BaseModel):
    nummer_mutualiteit: str
    totaal: str
    aantal_records: str
    controle_nummer_per_mutualiteit: str

    def to_footer_95(self) -> Footer95:
        return Footer95(
            nummer_mutualiteit=self.nummer_mutualiteit,
            nummer_verzamelfactuur="1", # TODO unsure?
            gevraagd_bedrag_a=self.totaal,
            gevraagd_bedrag_b="0",
            gevraagd_bedrag_a_b_c=self.totaal,
            aantal_records=self.aantal_records,
            controle_nummer_per_mutualiteit=self.controle_nummer_per_mutualiteit
        )

class Footer96Kine(BaseModel):
    nummer_mutualiteit: str
    totaal: str
    aantal_records: str # som + 2 ( rec 10 en 90) van het aantal records vermeld in elke record “95” zone 409
    controle_nummer_per_mutualiteit: str

    def to_footer_96(self) -> Footer96:
        return Footer96(
            nummer_mutualiteit=self.nummer_mutualiteit,
            nummer_verzamelfactuur="1", # TODO unsure?
            gevraagd_bedrag_a=self.totaal,
            gevraagd_bedrag_b="0",
            gevraagd_bedrag_a_b_c=self.totaal,
            aantal_records=self.aantal_records,
            controle_nummer_per_mutualiteit=self.controle_nummer_per_mutualiteit
        )

class DetailRecord(BaseModel):
    nomenclatuur: str
    datum_eerste_verstrekking: datetime.date
    bedrag_verzekeringstegemoetkoming: str
    datum_voorschrift: datetime.date
    persoonlijk_aandeel_patient: str
    bedrag_supplement: str
    voorschrijver: Optional[str] = "0"
    norm_voorschrijver: Optional[str] = "1"
    code_facturering_persoonlijk_aandeel_of_supplement: Optional[str] = 0 # 0 indien patiënt zelf betaald zie https://www.riziv.fgov.be/SiteCollectionDocuments/instructies_elektronische_facturatiegegevens.pdf p 491
    nummer_akkoord: Optional[str] = None
    errors: Any

    def to_record_50(self, 
                     i: int,
                     nummer_ziekenfonds_rechthebbende: str,
                     insz_rechthebbende: str,
                     identificatie_rechthebbende_2: str,
                     geslacht_rechthebbende: str,
                     hospital_care: bool,
                     identificatie_verstrekker: str,
                     geconventioneerde_verstrekker: bool,
                     norm_verstrekker: Optional[str] = "1", # meestal 1 https://metadata.aim-ima.be/nl/app/vars/SS00340_Gz
                     ) -> Record50Kine:
        return Record50Kine(
            num_record=str(i).rjust(6, "0"),
            nomenclatuur=self.nomenclatuur.rjust(7, "0"),
            datum_eerste_verstrekking=self.datum_eerste_verstrekking,
            nummer_ziekenfonds_rechthebbende=nummer_ziekenfonds_rechthebbende,
            insz_rechthebbende=insz_rechthebbende,
            identificatie_rechthebbende_2=identificatie_rechthebbende_2,
            geslacht_rechthebbende=geslacht_rechthebbende,
            hospital_care=hospital_care,
            identificatie_verstrekker=identificatie_verstrekker,
            norm_verstrekker=norm_verstrekker,
            bedrag_verzekeringstegemoetkoming=self.bedrag_verzekeringstegemoetkoming,
            datum_voorschrift=self.datum_voorschrift,
            persoonlijk_aandeel_patient=self.persoonlijk_aandeel_patient,
            bedrag_supplement=self.bedrag_supplement,
            code_facturering_persoonlijk_aandeel_of_supplement=self.code_facturering_persoonlijk_aandeel_of_supplement,
            geconventioneerde_verstrekker=geconventioneerde_verstrekker,
            identificatie_voorschrijver=self.voorschrijver,
            norm_voorschrijver=self.norm_voorschrijver
        )

    def to_record_52(self, 
                     i: int,
                     insz_rechthebbende: str,
                     identificatie_rechthebbende_2: str,
                     riziv_nummer: str,
                     nummer_akkoord: str, # MDA akkooord
                     ) -> Record52Kine:
        return Record52Kine(
            num_record=str(i).rjust(6, "0"),
            nomenclatuur=self.nomenclatuur.rjust(7, "0"),
            datum_verstrekking=self.datum_eerste_verstrekking,
            datum_lezing_identiteitsdocument=self.datum_eerste_verstrekking,
            insz_rechthebbende=insz_rechthebbende,
            identificatie_rechthebbende_2=identificatie_rechthebbende_2,
            riziv_nummer=riziv_nummer,
            nummer_akkoord=nummer_akkoord            
        )

class PatientBlock(BaseModel):
    hospital_care: Optional[bool] = False # YES
    nummer_ziekenfonds: str # YES
    insz_rechthebbende: str # YES
    identificatie_rechthebbende_2: str # hoe wordt dit opgevuld # YES
    geslacht_rechthebbende: str # 1 of 2 # YES
    nummer_facturerende_instelling: Optional[str] = "" # riziv kine # YES
    instelling_van_verblijf: Optional[str] = "000000000000" # indien hospitalisatie ... # YES
    nummer_individuele_factuur_1: str # eigen volgnummer # YES
    cg1_cg2: str # op te halen uit MDA denk ik? # YES
    referentiegegevens_netwerk_1: Optional[str] = "" # nummer verbintenis, zie MDA niet zeker of ik enkel _1 nodig heb # YES
    geconventioneerde_verstrekker: bool # YES
    nummer_akkoord: str # YES

    detail_records: List[DetailRecord]

    def to_patient_records(self, i_start) -> List[Union[Record20Kine, Record50Kine, Record52Kine, Record80Kine]]:
        ziekenfonds_bestemming = "300" if self.nummer_ziekenfonds.startswith("3") else self.nummer_ziekenfonds
        i = i_start # starting point
        record_20 = Record20Kine(
            num_record=str(i).rjust(6, "0"),
            nummer_ziekenfonds_aansluiting=self.nummer_ziekenfonds,
            insz_rechthebbende=self.insz_rechthebbende,
            identificatie_rechthebbende_2=self.identificatie_rechthebbende_2,
            geslacht_rechthebbende=self.geslacht_rechthebbende,
            hospital_care=self.hospital_care,
            nummer_facturerende_instelling=self.nummer_facturerende_instelling,
            instelling_van_verblijf=self.instelling_van_verblijf,
            code_stuiten_verjaringstermijn="0",
            reden_behandeling="0000", # TODO ????
            nummer_ziekenfonds_bestemming=ziekenfonds_bestemming,
            nummer_individuele_factuur_1=self.nummer_individuele_factuur_1,
            cg1_cg2=self.cg1_cg2,
            referentiegegevens_netwerk_1=self.referentiegegevens_netwerk_1
        ).to_record_20()

        invoice_control_inputs = []

        records_50s_and_52s = []


        totaal = 0
        totaal_persoonlijk_aandeel = 0
        totaal_supplement = 0
        for dr in self.detail_records:
            i += 1
            record_50 = dr.to_record_50(
                i=i,
                nummer_ziekenfonds_rechthebbende=self.nummer_ziekenfonds,
                insz_rechthebbende=self.insz_rechthebbende,
                identificatie_rechthebbende_2=self.identificatie_rechthebbende_2,
                geslacht_rechthebbende=self.geslacht_rechthebbende,
                hospital_care=self.hospital_care,
                identificatie_verstrekker=self.nummer_facturerende_instelling,
                geconventioneerde_verstrekker=self.geconventioneerde_verstrekker,
                norm_verstrekker="1", # meestal 1 https://metadata.aim-ima.be/nl/app/vars/SS00340_Gz
                     ).to_record_50()
            records_50s_and_52s.append(record_50)
            invoice_control_inputs.append(dr.nomenclatuur.rjust(7, "0"))

            i += 1
            record_52 = dr.to_record_52(
                i=i,
                insz_rechthebbende=self.insz_rechthebbende,
                identificatie_rechthebbende_2=self.identificatie_rechthebbende_2,
                riziv_nummer=self.nummer_facturerende_instelling,
                nummer_akkoord=dr.nummer_akkoord or self.nummer_akkoord
                     ).to_record_52()
            records_50s_and_52s.append(record_52)
            invoice_control_inputs.append(dr.nomenclatuur.rjust(7, "0"))

            totaal += int(dr.bedrag_verzekeringstegemoetkoming)
            totaal_persoonlijk_aandeel += int(dr.persoonlijk_aandeel_patient)
            totaal_supplement += int(dr.bedrag_supplement)

        i += 1
        record_80 = Record80Kine(
            num_record=str(i).rjust(6, "0"),
            nummer_ziekenfonds_aansluiting=self.nummer_ziekenfonds,
            insz_rechthebbende=self.insz_rechthebbende,
            identificatie_rechthebbende_2=self.identificatie_rechthebbende_2,
            geslacht_rechthebbende=self.geslacht_rechthebbende,
            hospital_care=self.hospital_care,
            nummer_facturerende_instelling=self.nummer_facturerende_instelling,
            reden_behandeling="0000", # TODO ????
            nummer_ziekenfonds_bestemming=ziekenfonds_bestemming,
            nummer_individuele_factuur_1=self.nummer_individuele_factuur_1,
            cg1_cg2=self.cg1_cg2,
            referentiegegevens_netwerk_1=self.referentiegegevens_netwerk_1,
            totaal=totaal,
            totaal_persoonlijk_aandeel=totaal_persoonlijk_aandeel,
            totaal_supplement=totaal_supplement,
            control_invoice=calculate_invoice_control(invoice_control_inputs)
        ).to_record_80()
        logger.info(f"Totaal voor Record 80: {totaal}")

        return [record_20, *records_50s_and_52s, record_80], invoice_control_inputs, totaal, totaal_persoonlijk_aandeel, totaal_supplement


class Message200KineNoPractitioner(BaseModel):
    """
    Now what do we need in general to complete these records
    """
    version: Optional[str] = "01" # YES
    reference: str # YES
    num_invoice: str # YES
    date_invoice: Optional[datetime.date] = datetime.date.today() # YES
    is_test: Optional[bool] = True # YES
    tel_contact: str # YES
    hospital_care: Optional[bool] = False # YES
    beroepscode_facturerende_derde: str = "000" # TODO verplicht vanaf april! zie https://www.riziv.fgov.be/SiteCollectionDocuments/bevoegdheidscodes_kinesitherapeuten.pdf  # YES
    kbo_number: str  # YES
    bic_bank: str  # YES
    iban_bank: str  # YES
    nummer_ziekenfonds: str # YES
    patient_blocks: List[PatientBlock]
    
class Message200Kine(Message200KineNoPractitioner):
    name_contact: str
    first_name_contact: str
    nummer_derdebetalende: str # riziv nummer facturerende derde (maw riziv kine ...)
    nummer_facturerende_instelling: str # riziv kine
    
    def to_message200(self) -> Message200:
        header_200 = Header200Kine(
            reference=self.reference,
            version=self.version,
            type="92" if self.is_test else "12"
        ).to_header_200()

        # see mail Brigitte Goossens 20240228
        if self.nummer_ziekenfonds.startswith("3") and not self.nummer_ziekenfonds.startswith("306"):
            ziekenfonds_bestemming = "300"
        else:
            ziekenfonds_bestemming = self.nummer_ziekenfonds

        i = 1
        header_300 = Header300Kine(
            num_invoice=self.num_invoice,
            date_invoice=self.date_invoice,
            is_test=self.is_test,
            name_contact=self.name_contact,
            first_name_contact=self.first_name_contact,
            tel_contact=self.tel_contact,
            hospital_care=self.hospital_care,
            type_invoicing="01"
        ).to_header_300()
        
        i += 1
        record_10 = Record10Kine(
            is_test=self.is_test,
            zendingsnummer=self.num_invoice,
            nummer_derdebetalende=self.nummer_derdebetalende,
            date_creation=self.date_invoice,
            kbo_number=self.kbo_number,
            bic_bank=self.bic_bank,
            iban_bank=self.iban_bank,
            beroepscode_facturerende_derde=self.beroepscode_facturerende_derde
        ).to_record_10()
        
        records = []
        invoice_control_inputs = []
        totaal = 0
        for pb in self.patient_blocks:
            patient_records, patient_invoice_control_inputs, patient_totaal, _, _ = pb.to_patient_records(i_start=i)
            records.extend(patient_records)
            invoice_control_inputs.extend(patient_invoice_control_inputs)
            i += len(patient_records)
            totaal += patient_totaal
            
        record_90 = Record90Kine(
            num_record=str(i).rjust(6, "0"),
            zendingsnummer=self.num_invoice,
            nummer_derdebetalende=self.nummer_derdebetalende,
            totaal=totaal,
            date_creation=self.date_invoice,
            kbo_number=self.kbo_number,
            bic_bank=self.bic_bank,
            iban_bank=self.iban_bank,
            control_message=calculate_invoice_control(invoice_control_inputs)
        ).to_record_90()
        logger.info(f"Totaal voor Record 90: {totaal}")


        aantal_records_95 = 4
        for block in self.patient_blocks:
            aantal_records_95 += len(block.detail_records)

        footer_95 = Footer95Kine(
            nummer_mutualiteit=ziekenfonds_bestemming,
            totaal=totaal,
            aantal_records=aantal_records_95,
            controle_nummer_per_mutualiteit=calculate_invoice_control(invoice_control_inputs)
        ).to_footer_95()

        aantal_records_95 +=  2
        footer_96 = Footer96Kine(
            nummer_mutualiteit=self.nummer_ziekenfonds[0] + "99",
            totaal=totaal,
            aantal_records=aantal_records_95,
            controle_nummer_per_mutualiteit=calculate_invoice_control(invoice_control_inputs)
        ).to_footer_96()

        return Message200(
            header_200=header_200,
            header_300=header_300,
            record_10=record_10,
            records=records,
            record_90=record_90,
            footer_95=footer_95,
            footer_96=footer_96
        )
