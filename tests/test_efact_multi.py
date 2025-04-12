import os
import datetime
import pytest
import random
import logging
from pathlib import Path
from typing import Any
from ehealth.efact.efact import EFactService
from .conftest import MYCARENET_PWD, MYCARENET_USER
from ehealth.efact.input_models_kine import Message200KineNoPractitioner, PatientBlock, DetailRecord
from ehealth.sts import STSService

from .test_mda import build_mda_input

logger = logging.getLogger(__name__)

KEYSTORE_PASSPHRASE = os.environ.get("KEYSTORE_PASSPHRASE")
KEYSTORE_SSIN = "90121320026"
KEYSTORE_PATH = "valid-eattest.acc-p12"
DATA_FOLDER = Path(__file__).parent.joinpath("data/faked_eagreement")

@pytest.fixture
def sts_service():
    return STSService()

@pytest.fixture()
def token(sts_service):
    return sts_service.get_serialized_token(KEYSTORE_PATH, KEYSTORE_PASSPHRASE, KEYSTORE_SSIN)

@pytest.fixture
def efact_service():
    return EFactService(
        mycarenet_license_username=MYCARENET_USER,
        mycarenet_license_password=MYCARENET_PWD,
    )

def test_send_efact(sts_service, token, efact_service):
    today = datetime.date.today()
    today_numeric = today.isoformat().replace("-", "")
    random_id = str(random.randint(1, 999999)).rjust(6, "0")
    reference = f"{today_numeric}{random_id}"
    logger.info(f"Posting message with reference {reference}")

    input_model_kine = Message200KineNoPractitioner(
        reference=reference,
        kbo_number="0503827601",
        num_invoice="001",
        tel_contact="0487179464",
        zendingsnummer="500",
        bic_bank="GKCCBEBB",
        iban_bank="BE19063539637812",
        nummer_individuele_factuur_1="00001",
        geconventioneerde_verstrekker=True,
        nummer_ziekenfonds="940",
        patient_blocks=[PatientBlock(
            hopsital_care=False,
            nummer_ziekenfonds="940", 
            insz_rechthebbende="6804200077", 
            identificatie_rechthebbende_2="3",
            geslacht_rechthebbende="1", 
            nummer_individuele_factuur_1="00001", 
            cg1_cg2="110110".rjust(10, "0"),
            referentiegegevens_netwerk_1="80001DCAVOABTVMMJCNSWCRAAQGG8U74", 
            geconventioneerde_verstrekker=True, 
            nummer_akkoord="90094042025101000023", 
            detail_records=[DetailRecord(
                voorschrijver="19733263004",
                nomenclatuur="567011",
                datum_eerste_verstrekking=datetime.date.today() - datetime.timedelta(days=2),
                bedrag_verzekeringstegemoetkoming="2455",
                datum_voorschrift=datetime.date.today() - datetime.timedelta(days=5),
                persoonlijk_aandeel_patient="625",
                bedrag_supplement="0",
            )]
        ), PatientBlock(
            hopsital_care=False,
            nummer_ziekenfonds="910", 
            insz_rechthebbende="6804211093", 
            identificatie_rechthebbende_2="8",
            geslacht_rechthebbende="1", 
            nummer_individuele_factuur_1="00002", 
            cg1_cg2="110110".rjust(10, "0"),
            referentiegegevens_netwerk_1="80001XQT035SSW0JBBHMF6HADNRNPJ", 
            geconventioneerde_verstrekker=True, 
            nummer_akkoord="90091042025101000075", 
            detail_records=[DetailRecord(
                voorschrijver="19733263004",
                nomenclatuur="567011",
                datum_eerste_verstrekking=datetime.date.today() - datetime.timedelta(days=2),
                bedrag_verzekeringstegemoetkoming="2455",
                datum_voorschrift=datetime.date.today() - datetime.timedelta(days=5),
                persoonlijk_aandeel_patient="625",
                bedrag_supplement="0",
            )]
        )]
    )
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        efact_service.send_efact(
            token, input_model_kine
        )

def test_get_messages(sts_service, token, efact_service):
    # 20250412298565 message that we wait for
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        messages = efact_service.get_messages(token)
        logger.info(f"num messages: {len(messages)}")
        for m in messages:
            logger.info(m.type)
            logger.info(m.base64_hash)
            logger.info(m.reference)
            if m.type == "message":
                logger.info(m.errors)
                logger.info(m.raw[:10])

def test_confirm_message(sts_service, token, efact_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE):
        base64_hash = "7qMDPZBldp6WcrRV8UuMJHLB7vQYo98kqSkn535rCxI="
        messages = efact_service.confirm_message(token, base64_hash, tack=False)
