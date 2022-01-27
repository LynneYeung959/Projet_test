import base64
from typing import Optional

from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

class KeyPair:
    @staticmethod
    def generate(size: int):
        """ Generate a private / public pair of keys. Size argument must be greater or equal to 1024 """
        if size < 1024:
            return None
        return KeyPair(RSA.generate(size, Random.new().read))

    def __init__(self, rsa_key):
        """ Initialize a KeyPair from a private RSA key """
        assert rsa_key.has_private()
        self.__key_private = rsa_key
        self.__key_public = rsa_key.publickey()

    @property
    def public(self) -> str:
        return self.__key_public.export_key().decode()

    @property
    def private(self) -> str:
        return self.__key_private.export_key().decode()


def encrypt(public_key: str, message: str) -> Optional[str]:
    """
    Returns the message encrypted using the public key (string)
    """
    if message == "":
        return ""

    # Convert public_key to RSA_key_format if valid
    try:
        key = RSA.importKey(public_key)
    except ValueError:
        return None

    encryptor = PKCS1_OAEP.new(key)
    try:
        msg_crypt = base64.b64encode(encryptor.encrypt(message.encode()))
    except ValueError:
        return None

    # Convert to text (string)
    msg_crypt_str = msg_crypt.decode()

    return msg_crypt_str

def decrypt(private_key: str, message: str) -> Optional[str]:
    """
    Returns the plain text message decrypted using the private key
    """
    if message == "":
        return ""

    # Convert private_key to RSA_key_format if valid
    try:
        key = RSA.importKey(private_key)
    except ValueError:
        return None

    decryptor = PKCS1_OAEP.new(key)

    try:
        message = decryptor.decrypt(base64.b64decode(message.encode()))
    except ValueError:
        return None


    # Convert to text (string)
    message_str = message.decode()

    return message_str


def sign(private_key: str, message: str) -> Optional[str]:

    try:
        key = RSA.importKey(private_key)
    except ValueError:
        return None

    hasher = SHA256.new(message.encode())
    signer = PKCS1_v1_5.new(key)

    try:
        signature = base64.b64encode(signer.sign(hasher))
    except TypeError:
        return None

    return signature.decode()

def verify(public_key: str, message: str, signature: str) -> Optional[str]:

    try:
        key = RSA.importKey(public_key)
    except ValueError:
        return None

    hasher = SHA256.new(message.encode())
    verifier = PKCS1_v1_5.new(key)

    try:
        verifier.verify(hasher, base64.b64decode(signature.encode()))
    except ValueError:
        return None

    return "OK"
