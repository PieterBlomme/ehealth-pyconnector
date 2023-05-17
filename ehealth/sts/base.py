from abc import abstractmethod
from contextlib import contextmanager
import logging

class KeyStoreException(Exception):
    pass

logger = logging.getLogger(__name__)
class AbstractSTSService:
    @abstractmethod
    def get_serialized_token(self, path: str, pwd: str, ssin: str, quality: str = "physiotherapy") -> str:
        pass

    @contextmanager
    def session(self, token: str, path: str, pwd: str) -> str:
        pass
            