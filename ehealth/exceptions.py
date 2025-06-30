class DecryptionException(Exception):
    """Base class for signature-related exceptions."""
    def __init__(self):
        super().__init__("Could not decrypt message")