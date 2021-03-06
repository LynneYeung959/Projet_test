import unittest
from Crypto.PublicKey import RSA
from Crypto import Random

from client.crypto import KeyPair


class TestCrypto(unittest.TestCase):

    keypair1024 = KeyPair.generate(1024)
    keypair2048 = KeyPair.generate(2048)
    keypair4096 = KeyPair.generate(4096)

    # Tests sur la génération des clés privées et publiques

    def test_key_creation(self):
        self.assertIsNotNone(self.keypair1024)
        self.assertIsNotNone(self.keypair2048)
        self.assertIsNotNone(self.keypair4096)

        # tentative de creation a partir d'une clé publique
        self.assertRaises(AssertionError, KeyPair, RSA.generate(1024, Random.new().read).publickey())

    def test_key_size(self):
        # Taille minium de 1024 bits
        self.assertIsNone(KeyPair.generate(0))
        self.assertIsNone(KeyPair.generate(512))
        self.assertIsNone(KeyPair.generate(1023))

        self.assertIsInstance(self.keypair1024, KeyPair)
        self.assertIsInstance(self.keypair2048, KeyPair)
        self.assertIsInstance(self.keypair4096, KeyPair)

        # Vérification de la taille des clés
        self.assertEqual(RSA.import_key(self.keypair1024.public).n.bit_length(), 1024)
        self.assertEqual(RSA.import_key(self.keypair1024.private).n.bit_length(), 1024)

        self.assertEqual(RSA.import_key(self.keypair2048.public).n.bit_length(), 2048)
        self.assertEqual(RSA.import_key(self.keypair2048.private).n.bit_length(), 2048)

        self.assertEqual(RSA.import_key(self.keypair4096.public).n.bit_length(), 4096)
        self.assertEqual(RSA.import_key(self.keypair4096.private).n.bit_length(), 4096)

    def test_key_unique(self):
        # Unicité des clés privées et publiques
        self.assertNotEqual(self.keypair1024.public, KeyPair.generate(1024).public)
        self.assertNotEqual(self.keypair2048.private, KeyPair.generate(2048).private)
        self.assertNotEqual(self.keypair4096.public, KeyPair.generate(4096).private)

        self.assertNotEqual(self.keypair1024.public, self.keypair1024.private)
        self.assertNotEqual(self.keypair2048.public, self.keypair2048.private)
        self.assertNotEqual(self.keypair4096.public, self.keypair4096.private)

    # Tests sur le chiffrement d'un message

    def test_encryption_message(self):
        # Vérification du format du message à chiffrer
        msg = "abcdefghijklmnopqrstuvwxyzAZERTYUIOP\n1234567890 &éçàèùïüö\t,?;.:/!§%*µ£=+})°]@"
        self.assertIsInstance(self.keypair2048.encrypt("A"), str)
        self.assertIsInstance(self.keypair2048.encrypt(msg), str)
        self.assertEqual(self.keypair2048.encrypt(""), "")

    def test_encryption_key(self):
        # Vérification de la clé
        self.assertIsInstance(self.keypair2048.encrypt("message"), str)

    def test_encryption_content(self):
        # Vérification du chiffrement (différent du message d'origine)
        long_msg = "abcdefghijklmnopqrstuvwxyzAZERTYUIOP\n1234567890 &éçàèùïüö\t,?;.:/!§%*µ£=+})°]@"
        self.assertNotEqual(self.keypair1024.encrypt("a"), "a")
        self.assertNotEqual(self.keypair2048.encrypt("message"), "message")
        self.assertNotEqual(self.keypair2048.encrypt(long_msg), long_msg)

    # Tests sur le déchiffrement d'un message

    def test_decryption_message(self):
        # Vérification du format du message à déchiffrer
        self.assertIsNone(self.keypair2048.decrypt("Fake_crypt_msg:CBVscPeuYkXW4/jjhinp"))
        self.assertEqual(self.keypair2048.decrypt(""), "")
        self.assertIsInstance(self.keypair2048.decrypt(self.keypair2048.encrypt("A")), str)

    def test_decryption_key(self):
        # Vérification de la clé
        self.assertIsNone(self.keypair1024.decrypt(self.keypair2048.encrypt("A")))
        self.assertIsNone(self.keypair4096.decrypt(self.keypair2048.encrypt("A")))

    def test_decryption_content(self):
        # Vérification du déchiffrement
        msg = "abcdefghijklmnopqrstuvwxyzAZERTYUIOP\n1234567890 &éçàèùïüö\t,?;.:/!§%*µ£=+})°]@"
        self.assertEqual(self.keypair2048.decrypt(self.keypair2048.encrypt("a")), "a")
        self.assertEqual(self.keypair2048.decrypt(self.keypair2048.encrypt("Hello World !")), "Hello World !")
        self.assertEqual(self.keypair2048.decrypt(self.keypair2048.encrypt(msg)), msg)


if __name__ == '__main__':
    unittest.main()
