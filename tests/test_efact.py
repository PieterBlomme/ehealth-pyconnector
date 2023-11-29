from xsdata.models.datatype import XmlDate
import os
import datetime
import pytest
import logging
from pathlib import Path
from ehealth.efact.efact import EFactService
from ehealth.efact.input_models import Header200, Message200, Header300, Record10
from .conftest import MYCARENET_PWD, MYCARENET_USER

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
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        efact_service.send_efact(
            token,
        )

def test_create_message():
    fp = DATA_FOLDER.joinpath('TFAC1SC09.509E')
    with open(fp) as f:
        target_message = f.read()

    efact_message = Message200(
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
            inhoud_facturatie="040",
            nummer_derdebetalende="018334780004",
            date_creation="20141125",
            reference="Fichier genere au CIN",
            bic_bank="GEBABEBB",
            iban_bank="BE10001232152604"
        ),
        remainder=""
    )
    # check that headers are equal
    assert target_message[:227] == str(efact_message)[:227]

    # check that record10 matches
    logger.info(target_message[227:227+350])
    logger.info(str(efact_message.record_10))
    assert target_message[227:227+350].startswith(str(efact_message.record_10))
    assert target_message[227:227+350] == str(efact_message.record_10)


    # https://www.riziv.fgov.be/SiteCollectionDocuments/instructies_elektronische_facturatiegegevens.pdf
    # record 10: identificatie van de zending
    # record 20: identificatie van de eerste factuur
    # record 50: verstrekkingen
    # record 51: bijkomende tariefverbintenis
    # record 80: totaal bedrag eerste factuur
    # record 90: totaal bedrag van de zending
    for i in range(6):
        logger.info(target_message[227+i*350:227+(i+1)*350])

    # assert str(efact_message) == target_message