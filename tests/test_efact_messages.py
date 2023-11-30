import logging
import pytest
from pathlib import Path
from ehealth.efact.input_models import (
    Header200, Message200, Header300, Record10, Record20, Record50,
    Record51, Record80, Record90, Footer95, Footer96,
    calculate_invoice_control
)

logger = logging.getLogger(__name__)

DATA_FOLDER = Path(__file__).parent.joinpath("data")

pydantic_with_files = [
    (
        DATA_FOLDER.joinpath('TFAC1SC09.509E'),
        Message200(
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
    ),
    (
        DATA_FOLDER.joinpath('TFAC1SC11.510E'),
        Message200(
            header_200=Header200(
                reference="20140000000001"
            ),
            header_300=Header300(
                year_and_month="201411",
                num_invoice="510",
                date_invoice="20141125",
                name_contact="DZIERGWA Yvan",
                first_name_contact="CIN",
                tel_contact="0028917263",
                type_invoice="03",
                type_invoicing="01"
            ),
            record_10=Record10(
                zendingsnummer="510",
                inhoud_facturatie="040", # ??? is this a fixed value?
                nummer_derdebetalende="018334780004",
                date_creation="20141125",
                reference="Fichier genere au CIN",
                bic_bank="GEBABEBB",
                iban_bank="BE10001232152604"
            ),
            record_20=Record20(
                nummer_ziekenfonds_aansluiting="131",
                identificatie_rechthebbende_1="008610313026",
                identificatie_rechthebbende_2="2",
                geslacht_rechthebbende="2",
                type_factuur=3, # ??? is this a fixed value?
                nummer_facturerende_instelling="018334780004", # zie ook record10
                nummer_ziekenfonds_bestemming="131",
                nummer_individuele_factuur_1="14100",
                nummer_individuele_factuur_2="0000001",
                cg1_cg2="0000110110",
                referentie_instelling="Fichier genere au CIN" # zie ook record10
            ),
            record_50s=[Record50(
                nomenclatuur="0101032",
                datum_eerste_verstrekking="20141118",
                datum_laatste_verstrekking="20141118",
                nummer_ziekenfonds_rechthebbende="131",
                identificatie_rechthebbende_1="008610313026",
                identificatie_rechthebbende_2="2",
                geslacht_rechthebbende="2",
                identificatie_verstrekker="018334780004",
                bedrag_verzekeringstegemoetkoming="1942",
                datum_voorschrift="00000000",
                aantal=1,
                identificatie_voorschrijver="000000000000",
                persoonlijk_aandeel_patient="0600",
                referentie_instelling="Fichier genere au CIN", # zie ook record10
                bedrag_supplement="0",
                uitzondering_derdebetalersregeling="2",
                geconventioneerde_verstrekker="1"
            )],
            record_51s=[Record51(
                nomenclatuur="0101032",
                datum_verstrekking="20141118",
                identificatie_rechthebbende_1="008610313026",
                identificatie_rechthebbende_2="2",
                identificatie_verstrekker="018334780004",
                bedrag_verzekeringstegemoetkoming="1942",
                code_gerechtigde="0000110110",
                nummer_akkoord_tariefverbintenis="537ZJN7Q5D9M0XLZ80F1DWJZ9LKI8K530000000000002000",
                datum_mededeling_informatie="20141125"
            )],
            record_80=Record80(
                nummer_ziekenfonds_aansluiting="131",
                identificatie_rechthebbende_1="008610313026",
                identificatie_rechthebbende_2="2",
                geslacht_rechthebbende="2",
                type_factuur=3, # ??? is this a fixed value?
                nummer_facturerende_instelling="018334780004", # zie ook record10
                bedrag_financieel_rekeningnummer_b="0",
                nummer_ziekenfonds_bestemming="131",
                bedrag_financieel_rekeningnummer_a="1942",
                nummer_individuele_factuur_1="14100",
                nummer_individuele_factuur_2="0000001",
                persoonlijk_aandeel_patient="0600",
                referentie_instelling="Fichier genere au CIN", # zie ook record10      
                bedrag_supplement="0",
                voorschot_financieel_rekeningnummer_a="0",
                control_invoice=calculate_invoice_control(["0101032", "0101032"])
            ),
            record_90=Record90(
                zendingsnummer="510",
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
    ),
    (
        DATA_FOLDER.joinpath('TFAC1SC12.518E'),
        Message200(
            header_200=Header200(
                reference="20140000000518"
            ),
            header_300=Header300(
                year_and_month="201411",
                num_invoice="518",
                date_invoice="20141125",
                name_contact="DZIERGWA Yvan",
                first_name_contact="CIN",
                tel_contact="0028917263",
                type_invoice="03",
                type_invoicing="01"
            ),
            record_10=Record10(
                zendingsnummer="518",
                inhoud_facturatie="040", # ??? is this a fixed value?
                nummer_derdebetalende="018334780004",
                date_creation="20141125",
                reference="Fichier genere au CIN",
                bic_bank="GEBABEBB",
                iban_bank="BE10001232152604"
            ),
            record_20=Record20(
                nummer_ziekenfonds_aansluiting="131",
                identificatie_rechthebbende_1="008610313026",
                identificatie_rechthebbende_2="2",
                geslacht_rechthebbende="2",
                type_factuur=3, # ??? is this a fixed value?
                nummer_facturerende_instelling="018334780004", # zie ook record10
                nummer_ziekenfonds_bestemming="131",
                nummer_individuele_factuur_1="14100",
                nummer_individuele_factuur_2="0000001",
                cg1_cg2="0000110110",
                referentie_instelling="Fichier genere au CIN" # zie ook record10
            ),
            record_50s=[Record50(
                nomenclatuur="0101032",
                datum_eerste_verstrekking="20141120",
                datum_laatste_verstrekking="20141120",
                nummer_ziekenfonds_rechthebbende="131",
                identificatie_rechthebbende_1="008610313026",
                identificatie_rechthebbende_2="2",
                geslacht_rechthebbende="2",
                identificatie_verstrekker="018334780004",
                norm_verstrekker="4",
                bedrag_verzekeringstegemoetkoming="1692",
                datum_voorschrift="00000000",
                aantal=1,
                identificatie_voorschrijver="000000000000",
                persoonlijk_aandeel_patient="0400",
                referentie_instelling="Fichier genere au CIN", # zie ook record10
                bedrag_supplement="0",
                uitzondering_derdebetalersregeling="7",
                geconventioneerde_verstrekker="1",
                identificatie_bijkomende_verstrekker="017385467004"
            )],
            record_51s=[Record51(
                nomenclatuur="0101032",
                datum_verstrekking="20141120",
                identificatie_rechthebbende_1="008610313026",
                identificatie_rechthebbende_2="2",
                identificatie_verstrekker="018334780004",
                bedrag_verzekeringstegemoetkoming="1692",
                code_gerechtigde="0000110110",
                nummer_akkoord_tariefverbintenis="5371INN117MM0S3A20ZPBCY09X75NK480000000000002000",
                datum_mededeling_informatie="20141125"
            )],
            record_80=Record80(
                nummer_ziekenfonds_aansluiting="131",
                identificatie_rechthebbende_1="008610313026",
                identificatie_rechthebbende_2="2",
                geslacht_rechthebbende="2",
                type_factuur=3, # ??? is this a fixed value?
                nummer_facturerende_instelling="018334780004", # zie ook record10
                bedrag_financieel_rekeningnummer_b="0",
                nummer_ziekenfonds_bestemming="131",
                bedrag_financieel_rekeningnummer_a="1692",
                nummer_individuele_factuur_1="14100",
                nummer_individuele_factuur_2="0000001",
                persoonlijk_aandeel_patient="0400",
                referentie_instelling="Fichier genere au CIN", # zie ook record10      
                bedrag_supplement="0",
                voorschot_financieel_rekeningnummer_a="0",
                control_invoice=calculate_invoice_control(["0101032", "0101032"])
            ),
            record_90=Record90(
                zendingsnummer="518",
                inhoud_facturatie="040", # ??? is this a fixed value?
                nummer_derdebetalende="018334780004",
                date_creation="20141125",
                reference="Fichier genere au CIN",
                bic_bank="GEBABEBB",
                iban_bank="BE10001232152604",
                bedrag_financieel_rekeningnummer_a="1692",
                bedrag_financieel_rekeningnummer_b="0",
                control_message=calculate_invoice_control(["0101032", "0101032"])
            ),
            footer_95=Footer95(
                nummer_mutualiteit="131",
                gevraagd_bedrag_a="1692",
                gevraagd_bedrag_b="0",
                gevraagd_bedrag_a_b_c="1692",
                aantal_records="6",
                controle_nummer_per_mutualiteit=calculate_invoice_control(["0101032", "0101032"])
            ),
            footer_96=Footer96(
                nummer_mutualiteit="199",
                gevraagd_bedrag_a="1692",
                gevraagd_bedrag_b="0",
                gevraagd_bedrag_a_b_c="1692",
                aantal_records="8",
                controle_nummer_per_mutualiteit=calculate_invoice_control(["0101032", "0101032"])
            )
        )
    ),
    (
        DATA_FOLDER.joinpath('TFAC1SC13.519E'),
        Message200(
            header_200=Header200(
                reference="20140000000519"
            ),
            header_300=Header300(
                year_and_month="201411",
                num_invoice="519",
                date_invoice="20141125",
                name_contact="DZIERGWA Yvan",
                first_name_contact="CIN",
                tel_contact="0028917263",
                type_invoice="03",
                type_invoicing="01"
            ),
            record_10=Record10(
                zendingsnummer="519",
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
                norm_verstrekker="1",
                bedrag_verzekeringstegemoetkoming="1942",
                datum_voorschrift="00000000",
                aantal=1,
                identificatie_voorschrijver="000000000000",
                persoonlijk_aandeel_patient="0150",
                referentie_instelling="Fichier genere au CIN", # zie ook record10
                bedrag_supplement="0",
                uitzondering_derdebetalersregeling="0",
                geconventioneerde_verstrekker="1",
            )],
            record_51s=[],
            record_80=Record80(
                num_record="000004",
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
                control_invoice=calculate_invoice_control(["0101032"])
            ),
            record_90=Record90(
                num_record="000005",
                zendingsnummer="519",
                inhoud_facturatie="040", # ??? is this a fixed value?
                nummer_derdebetalende="018334780004",
                date_creation="20141125",
                reference="Fichier genere au CIN",
                bic_bank="GEBABEBB",
                iban_bank="BE10001232152604",
                bedrag_financieel_rekeningnummer_a="1942",
                bedrag_financieel_rekeningnummer_b="0",
                control_message=calculate_invoice_control(["0101032"])
            ),
            footer_95=Footer95(
                nummer_mutualiteit="131",
                gevraagd_bedrag_a="1942",
                gevraagd_bedrag_b="0",
                gevraagd_bedrag_a_b_c="1942",
                aantal_records="6", # heh?
                controle_nummer_per_mutualiteit=calculate_invoice_control(["0101032"])
            ),
            footer_96=Footer96(
                nummer_mutualiteit="199",
                gevraagd_bedrag_a="1942",
                gevraagd_bedrag_b="0",
                gevraagd_bedrag_a_b_c="1942",
                aantal_records="8",
                controle_nummer_per_mutualiteit=calculate_invoice_control(["0101032"])
            )
        )
    ),
    (
        DATA_FOLDER.joinpath('TFAC1SC15.520E'),
        Message200(
            header_200=Header200(
                reference="20140000000520"
            ),
            header_300=Header300(
                year_and_month="201411",
                num_invoice="520",
                date_invoice="20141125",
                name_contact="DZIERGWA Yvan",
                first_name_contact="CIN",
                tel_contact="0028917263",
                type_invoice="03",
                type_invoicing="01"
            ),
            record_10=Record10(
                zendingsnummer="520",
                inhoud_facturatie="040", # ??? is this a fixed value?
                nummer_derdebetalende="018334780004",
                date_creation="20141125",
                reference="Fichier genere au CIN",
                bic_bank="GEBABEBB",
                iban_bank="BE10001232152604"
            ),
            record_20=Record20(
                nummer_ziekenfonds_aansluiting="131",
                identificatie_rechthebbende_1="008610313026",
                identificatie_rechthebbende_2="2",
                geslacht_rechthebbende="2",
                type_factuur=3, # ??? is this a fixed value?
                nummer_facturerende_instelling="018334780004", # zie ook record10
                nummer_ziekenfonds_bestemming="131",
                nummer_individuele_factuur_1="14100",
                nummer_individuele_factuur_2="0000001",
                cg1_cg2="0000110110",
                referentie_instelling="Fichier genere au CIN" # zie ook record10
            ),
            record_50s=[Record50(
                nomenclatuur="0101032",
                datum_eerste_verstrekking="20141118",
                datum_laatste_verstrekking="20141118",
                nummer_ziekenfonds_rechthebbende="131",
                identificatie_rechthebbende_1="008610313026",
                identificatie_rechthebbende_2="2",
                geslacht_rechthebbende="2",
                identificatie_verstrekker="018334780004",
                norm_verstrekker="1",
                bedrag_verzekeringstegemoetkoming="1942",
                datum_voorschrift="00000000",
                aantal=1,
                identificatie_voorschrijver="000000000000",
                persoonlijk_aandeel_patient="0650",
                referentie_instelling="Fichier genere au CIN", # zie ook record10
                bedrag_supplement="0",
                uitzondering_derdebetalersregeling="2",
                geconventioneerde_verstrekker="1",
            )],
            record_51s=[],
            record_80=Record80(
                num_record="000004",
                nummer_ziekenfonds_aansluiting="131",
                identificatie_rechthebbende_1="008610313026",
                identificatie_rechthebbende_2="2",
                geslacht_rechthebbende="2",
                type_factuur=3, # ??? is this a fixed value?
                nummer_facturerende_instelling="018334780004", # zie ook record10
                bedrag_financieel_rekeningnummer_b="0",
                nummer_ziekenfonds_bestemming="131",
                bedrag_financieel_rekeningnummer_a="1942",
                nummer_individuele_factuur_1="14100",
                nummer_individuele_factuur_2="0000001",
                persoonlijk_aandeel_patient="0650",
                referentie_instelling="Fichier genere au CIN", # zie ook record10      
                bedrag_supplement="0",
                voorschot_financieel_rekeningnummer_a="0",
                control_invoice=calculate_invoice_control(["0101032"])
            ),
            record_90=Record90(
                num_record="000005",
                zendingsnummer="520",
                inhoud_facturatie="040", # ??? is this a fixed value?
                nummer_derdebetalende="018334780004",
                date_creation="20141118",
                reference="Fichier genere au CIN",
                bic_bank="GEBABEBB",
                iban_bank="BE10001232152604",
                bedrag_financieel_rekeningnummer_a="1942",
                bedrag_financieel_rekeningnummer_b="0",
                control_message=calculate_invoice_control(["0101032"])
            ),
            footer_95=Footer95(
                nummer_mutualiteit="131",
                gevraagd_bedrag_a="1942",
                gevraagd_bedrag_b="0",
                gevraagd_bedrag_a_b_c="1942",
                aantal_records="6", # heh?
                controle_nummer_per_mutualiteit=calculate_invoice_control(["0101032"])
            ),
            footer_96=Footer96(
                nummer_mutualiteit="199",
                gevraagd_bedrag_a="1942",
                gevraagd_bedrag_b="0",
                gevraagd_bedrag_a_b_c="1942",
                aantal_records="8",
                controle_nummer_per_mutualiteit=calculate_invoice_control(["0101032"])
            )
        )
    ),
]

# TODO controlenummer mutualiteit

@pytest.mark.parametrize("fp, efact_message", pydantic_with_files)
def test_create_message(fp, efact_message):
    with open(fp) as f:
        target_message = f.read()
    # check that headers are equal
    assert target_message[:227] == str(efact_message)[:227]

    # https://www.riziv.fgov.be/SiteCollectionDocuments/instructies_elektronische_facturatiegegevens.pdf

    # record 10: identificatie van de zending
    assert target_message[227:227+350*1] == str(efact_message.record_10)

    # record 20: identificatie van de eerste factuur
    assert target_message[227+350*1:227+350*2] == str(efact_message.record_20)

    # record 50: verstrekkingen
    assert target_message[227+350*2:227+350*3] == str(efact_message.record_50s[0])

    # record 51: bijkomende tariefverbintenis
    r = target_message[227+350*3:227+350*4]
    if len(efact_message.record_51s) > 0:
        assert r == str(efact_message.record_51s[0])
    num_51s = len(efact_message.record_51s)

    # record 80: totaal bedrag eerste factuur
    r = target_message[227+350*(3+num_51s):227+350*(4+num_51s)]
    assert r == str(efact_message.record_80)

    # record 90: totaal bedrag van de zending
    r = target_message[227+350*(4+num_51s):227+350*(5+num_51s)]
    assert r == str(efact_message.record_90)

    # record 95
    r = target_message[227+350*(5+num_51s):227+350*(6+num_51s)]
    assert r == str(efact_message.footer_95)

    # record 96
    r = target_message[227+350*(6+num_51s):227+350*(7+num_51s)]
    assert r == str(efact_message.footer_96)

    assert str(efact_message)[2300:2500] == target_message[2300:2500]