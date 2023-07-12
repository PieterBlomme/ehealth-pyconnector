from ehealth.sts import STSService
from ehealth.eagreement import EAgreementService
from pathlib import Path
import os
import pytest
import datetime
import logging

logger = logging.getLogger(__name__)

TEST_DATA_FOLDER = Path(__file__).parent.joinpath("data")
KEYSTORE_PASSPHRASE = os.environ.get("KEYSTORE_PASSPHRASE")
KEYSTORE_SSIN = os.environ.get("KEYSTORE_SSIN")
KEYSTORE_PATH = "valid.acc-p12"
MYCARENET_USER = os.environ.get("MYCARENET_USER")
MYCARENET_PWD = os.environ.get("MYCARENET_PWD")

@pytest.fixture
def sts_service():
    return STSService()

@pytest.fixture
def eagreement_service():
    return EAgreementService(
        mycarenet_license_username=MYCARENET_USER,
        mycarenet_license_password=MYCARENET_PWD,
    )

@pytest.fixture()
def token(sts_service):
    return sts_service.get_serialized_token(KEYSTORE_PATH, KEYSTORE_PASSPHRASE, KEYSTORE_SSIN)


def test_eagreement__ask_agreement__happy_path(sts_service, token, eagreement_service):
    with sts_service.session(token, KEYSTORE_PATH, KEYSTORE_PASSPHRASE) as session:
        logger.info(session.getSession().getEncryptionCredential())
        # session.loadEncryptionKeys("system")
        logger.info(sts_service.config_validator.getProperty("sessionmanager.encryption.keystore"))
        logger.info(sts_service.config_validator.getProperty("sessionmanager.encryption.alias"))


            #         String pathKeystore = this.config.getProperty("sessionmanager.encryption.keystore");
            # String privateKeyAlias = this.config.getProperty("sessionmanager.encryption.alias", "authentication");
            # KeyStoreInfo ksInfo = new KeyStoreInfo(pathKeystore, password, privateKeyAlias, password);
            # KeyStoreManager encryptionKeystoreManager = new KeyStoreManager(ksInfo);
            # Map<String, PrivateKey> encryptionPrivateKeys = KeyManager.getDecryptionKeys(
            #    encryptionKeystoreManager.getKeyStore(), ksInfo.getPrivateKeyPassword()
            # );
            # this.session.setEncryptionCredential(new KeyStoreCredential(ksInfo));
            # this.session.setEncryptionPrivateKeys(encryptionPrivateKeys);
            # fetchEtk(KeyDepotManager.EncryptionTokenType.ENCRYPTION, encryptionPrivateKeys, this.config);
        response = eagreement_service.ask_agreement(
            token=token,
            # bundleLocation=str(TEST_DATA_FOLDER.joinpath('AskAgreementRequestContent.xml'))
            bundleLocation=str(TEST_DATA_FOLDER.joinpath('AskAgreementRequestContent.xml'))
        )
        logger.info(response)