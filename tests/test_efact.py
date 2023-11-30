import os
import datetime
import pytest
import logging
from pathlib import Path
from ehealth.efact.efact import EFactService
from .conftest import MYCARENET_PWD, MYCARENET_USER
from ehealth.efact.input_models import (
    Header200, Message200, Header300, Record10, Record20, Record50,
    Record51, Record80, Record90, Footer95, Footer96,
    calculate_invoice_control
)

logger = logging.getLogger(__name__)

KEYSTORE_PASSPHRASE = os.environ.get("KEYSTORE_PASSPHRASE")
KEYSTORE_SSIN = os.environ.get("KEYSTORE_SSIN")
KEYSTORE_PATH = "valid.acc-p12"
DATA_FOLDER = Path(__file__).parent.joinpath("data")

@pytest.fixture
def efact_service():
    return EFactService(
        mycarenet_license_username=MYCARENET_USER,
        mycarenet_license_password=MYCARENET_PWD,
    )

def test_dummy(sts_service, token, efact_service):
    input_model = Message200(
            header_200=Header200(
                reference="20140000000001"
            ),
            header_300=Header300(
                year_and_month="201411",
                num_invoice="509",
                date_invoice="20141125",
                name_contact="DZIERGWA Yvan",
                first_name_contact="CIN",
                tel_contact="0028917263",
                type_invoice="03",
                type_invoicing="01"
            ),
            record_10=Record10(
                zendingsnummer="509",
                inhoud_facturatie="040", # ??? is this a fixed value?
                nummer_derdebetalende="018334780004",
                date_creation="20141125",
                reference="Fichier genere au CIN",
                bic_bank="GEBABEBB",
                iban_bank="BE10001232152604"
            ),
            record_20=Record20(
                nummer_ziekenfonds_aansluiting="131",
                identificatie_rechthebbende_1="003612101539",
                identificatie_rechthebbende_2="6",
                geslacht_rechthebbende="1",
                type_factuur=3, # ??? is this a fixed value?
                nummer_facturerende_instelling="018334780004", # zie ook record10
                nummer_ziekenfonds_bestemming="131",
                nummer_individuele_factuur_1="14100",
                nummer_individuele_factuur_2="0000001",
                cg1_cg2="0000131131",
                referentie_instelling="Fichier genere au CIN" # zie ook record10
            ),
            record_50s=[Record50(
                nomenclatuur="0101032",
                datum_eerste_verstrekking="20141125",
                datum_laatste_verstrekking="20141125",
                nummer_ziekenfonds_rechthebbende="131",
                identificatie_rechthebbende_1="003612101539",
                identificatie_rechthebbende_2="6",
                geslacht_rechthebbende="1",
                identificatie_verstrekker="018334780004",
                bedrag_verzekeringstegemoetkoming="1942",
                datum_voorschrift="00000000",
                aantal=1,
                identificatie_voorschrijver="000000000000",
                persoonlijk_aandeel_patient="0150",
                referentie_instelling="Fichier genere au CIN", # zie ook record10
                bedrag_supplement="0",
                geconventioneerde_verstrekker="1"
            )],
            record_51s=[Record51(
                nomenclatuur="0101032",
                datum_verstrekking="20141125",
                identificatie_rechthebbende_1="003612101539",
                identificatie_rechthebbende_2="6",
                identificatie_verstrekker="018334780004",
                bedrag_verzekeringstegemoetkoming="1942",
                code_gerechtigde="0000131131",
                nummer_akkoord_tariefverbintenis="547KCNOI4P5M04NFJ0CVLCXP9FZLLK450000000000002000",
                datum_mededeling_informatie="20141125"
            )],
            record_80=Record80(
                nummer_ziekenfonds_aansluiting="131",
                identificatie_rechthebbende_1="003612101539",
                identificatie_rechthebbende_2="6",
                geslacht_rechthebbende="1",
                type_factuur=3, # ??? is this a fixed value?
                nummer_facturerende_instelling="018334780004", # zie ook record10
                bedrag_financieel_rekeningnummer_b="0",
                nummer_ziekenfonds_bestemming="131",
                bedrag_financieel_rekeningnummer_a="1942",
                nummer_individuele_factuur_1="14100",
                nummer_individuele_factuur_2="0000001",
                persoonlijk_aandeel_patient="0150",
                referentie_instelling="Fichier genere au CIN", # zie ook record10      
                bedrag_supplement="0",
                voorschot_financieel_rekeningnummer_a="0",
                control_invoice=calculate_invoice_control(["0101032", "0101032"])
            ),
            record_90=Record90(
                zendingsnummer="509",
                inhoud_facturatie="040", # ??? is this a fixed value?
                nummer_derdebetalende="018334780004",
                date_creation="20141125",
                reference="Fichier genere au CIN",
                bic_bank="GEBABEBB",
                iban_bank="BE10001232152604",
                bedrag_financieel_rekeningnummer_a="1942",
                bedrag_financieel_rekeningnummer_b="0",
                control_message=calculate_invoice_control(["0101032", "0101032"])
            ),
            footer_95=Footer95(
                nummer_mutualiteit="131",
                gevraagd_bedrag_a="1942",
                gevraagd_bedrag_b="0",
                gevraagd_bedrag_a_b_c="1942",
                aantal_records="6",
                controle_nummer_per_mutualiteit=calculate_invoice_control(["0101032", "0101032"])
            ),
            footer_96=Footer96(
                nummer_mutualiteit="199",
                gevraagd_bedrag_a="1942",
                gevraagd_bedrag_b="0",
                gevraagd_bedrag_a_b_c="1942",
                aantal_records="8",
                controle_nummer_per_mutualiteit=calculate_invoice_control(["0101032", "0101032"])
            )
        )
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        efact_service.send_efact(
            token, input_model
        )