import unittest
from Crypto.PublicKey import RSA

from client.crypto import KeyPair


class TestCrypto(unittest.TestCase):

    keypair4096 = KeyPair.generate(4096)
    keypair2048 = KeyPair.generate(2048)
    keypair1024 = KeyPair.generate(1024)

    # Tests sur la génération des clés privées et publiques

    def test_minimum_key_size(self):
        # Taille minium de 1024 bits
        self.assertIsNone(KeyPair.generate(0))
        self.assertIsNone(KeyPair.generate(512))
        self.assertIsNone(KeyPair.generate(1023))

        self.assertIsInstance(self.keypair1024, KeyPair)
        self.assertIsInstance(self.keypair2048, KeyPair)
        self.assertIsInstance(self.keypair4096, KeyPair)

    def test_key_size(self):
        # Vérification de la taille des clés
        self.assertEqual(RSA.import_key(self.keypair1024.public).n.bit_length(), 1024)
        self.assertEqual(RSA.import_key(self.keypair1024.private).n.bit_length(), 1024)

        self.assertEqual(RSA.import_key(self.keypair2048.public).n.bit_length(), 2048)
        self.assertEqual(RSA.import_key(self.keypair2048.private).n.bit_length(), 2048)

        self.assertEqual(RSA.import_key(self.keypair4096.public).n.bit_length(), 4096)
        self.assertEqual(RSA.import_key(self.keypair4096.private).n.bit_length(), 4096)

    def test_key_unique(self):
        # Unicité des clés privées et publiques
        self.assertNotEqual(self.keypair1024, KeyPair.generate(1024))
        self.assertNotEqual(self.keypair2048, KeyPair.generate(2048))
        self.assertNotEqual(self.keypair4096, KeyPair.generate(4096))

        self.assertNotEqual(self.keypair1024.public, self.keypair1024.private)
        self.assertNotEqual(self.keypair2048.public, self.keypair2048.private)
        self.assertNotEqual(self.keypair4096.public, self.keypair4096.private)

    # Tests sur le chiffrement d'un message

    def test_encryption_message(self):
        # Vérification du format du message à chiffrer
        msg = "abcdefghijklmnopqrstuvwxyzAZERTYUIOP\n1234567890 &éçàèùïüö\t,?;.:/!§%*µ£=+})°]@"
        self.assertIsNone(self.keypair2048.encrypt(""))
        self.assertIsInstance(self.keypair2048.encrypt("A"), str)
        self.assertIsInstance(self.keypair2048.encrypt(msg), str)

    def test_encryption_key(self):
        # Vérification de la clé
        fake_keypair = KeyPair("FakePubKey:CBVscPeuYkXW4/jjhinp", "FakePrivKey:CBVscPeuYkXW4/jjhinp")
        self.assertIsNone(fake_keypair.encrypt("message"))
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
        self.assertIsNone(self.keypair2048.decrypt(""))
        self.assertIsNone(self.keypair2048.decrypt("Fake_crypt_msg:CBVscPeuYkXW4/jjhinp"))
        self.assertIsInstance(self.keypair2048.decrypt(self.keypair2048.encrypt("A")), str)

    def test_decryption_key(self):
        # Vérification de la clé
        fake_keypair = KeyPair("FakePubKey:CBVscPeuYkXW4/jjhinp", "FakePrivKey:CBVscPeuYkXW4/jjhinp")
        self.assertIsNone(self.keypair1024.decrypt(self.keypair2048.encrypt("A")))
        self.assertIsNone(self.keypair4096.decrypt(self.keypair2048.encrypt("A")))
        self.assertIsNone(fake_keypair.decrypt(self.keypair2048.encrypt("A")))

    def test_decryption_content(self):
        # Vérification du déchiffrement
        msg = "abcdefghijklmnopqrstuvwxyzAZERTYUIOP\n1234567890 &éçàèùïüö\t,?;.:/!§%*µ£=+})°]@"
        self.assertEqual(self.keypair2048.decrypt(self.keypair2048.encrypt("a")), "a")
        self.assertEqual(self.keypair2048.decrypt(self.keypair2048.encrypt("Hello World !")), "Hello World !")
        self.assertEqual(self.keypair2048.decrypt(self.keypair2048.encrypt(msg)), msg)


if __name__ == '__main__':
    unittest.main()
