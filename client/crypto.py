import base64
from typing import Optional

from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


class KeyPair:
    @staticmethod
    def generate(size: int):
        """ Generate a private / public pair of keys. Size argument must be greater or equal to 1024 """
        if size < 1024:
            return None
        return KeyPair(RSA.generate(size, Random.new().read))

    def __init__(self, rsa_key: RSA.RsaKey):
        """ Initialize a KeyPair from a private RSA key """
        assert rsa_key.has_private()
        self.__key_private = rsa_key
        self.__key_public = rsa_key.publickey()
        self.__encryptor = PKCS1_OAEP.new(self.__key_public)
        self.__decryptor = PKCS1_OAEP.new(self.__key_private)

    @property
    def public(self) -> str:
        return self.__key_public.export_key().decode()

    @property
    def private(self) -> str:
        return self.__key_private.export_key().decode()

    def encrypt(self, message: str) -> Optional[str]:
        """ Returns the message encrypted using the public key and encoded in base64 """
        if message == "":
            return ""

        try:
            crypted_msg = self.__encryptor.encrypt(message.encode())
        except ValueError:
            return None

        return base64.b64encode(crypted_msg).decode()

    def decrypt(self, b64_message: str) -> Optional[str]:
        """ Returns the plain text message decrypted using the private key """
        if b64_message == "":
            return ""

        message = base64.b64decode(b64_message.encode())

        try:
            decrypted_msg = self.__decryptor.decrypt(message)
        except ValueError:
            return None

        return decrypted_msg.decode()
