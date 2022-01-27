import unittest
from Crypto.PublicKey import RSA
from Crypto import Random

from client.crypto import KeyPair, encrypt, decrypt, sign, verify


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
        self.assertIsInstance(encrypt(self.keypair2048.public, "A"), str)
        self.assertIsInstance(encrypt(self.keypair2048.public, msg), str)
        self.assertEqual(encrypt(self.keypair2048.public, ""), "")

    def test_encryption_key(self):
        # Vérification de la clé
        self.assertEqual(encrypt("Fake key:CBVscPeuYkXW4/jjhinp", "message"), None)
        self.assertIsInstance(encrypt(self.keypair2048.public, "message"), str)

    def test_encryption_content(self):
        # Vérification du chiffrement (différent du message d'origine)
        long_msg = "abcdefghijklmnopqrstuvwxyzAZERTYUIOP\n1234567890 &éçàèùïüö\t,?;.:/!§%*µ£=+})°]@"
        self.assertNotEqual(encrypt(self.keypair1024.public, "a"), "a")
        self.assertNotEqual(encrypt(self.keypair2048.public, "message"), "message")
        self.assertEqual(encrypt(self.keypair1024.public, long_msg), None) # msg too long

    # Tests sur le déchiffrement d'un message

    def test_decryption_message(self):
        # Vérification du format du message à déchiffrer
        self.assertIsNone(decrypt(self.keypair2048.private, "Fake_crypt_msg:CBVscPeuYkXW4/jjhinp"))
        self.assertEqual(decrypt(self.keypair2048.private, ""), "")
        self.assertIsInstance(decrypt(self.keypair2048.private, encrypt(self.keypair2048.public,"A")), str)

    def test_decryption_key(self):
        # Vérification de la clé
        self.assertIsNone(decrypt(self.keypair1024.private, encrypt(self.keypair2048.public, "A")))
        self.assertIsNone(decrypt(self.keypair4096.private, encrypt(self.keypair2048.public, "A")))

    def test_decryption_content(self):
        # Vérification du déchiffrement
        msg = "abcdefghijklmnopqrstuvwxyzAZERTYUIOP\n1234567890 &éçàèùïüö\t,?;.:/!§%*µ£=+})°]@"
        self.assertEqual(decrypt(self.keypair2048.private, encrypt(self.keypair2048.public, "a")), "a")
        self.assertEqual(decrypt(self.keypair2048.private, encrypt(self.keypair2048.public, "")), "")
        self.assertEqual(decrypt(self.keypair2048.private, encrypt(self.keypair2048.public, msg)), msg)

    # Tests sur la signature d'un message

    def test_sign_msg(self):
        # type return verification (to avoid conflicts with bytes)
        self.assertIsInstance(sign(self.keypair2048.private, ""), str)
        self.assertIsInstance(sign(self.keypair2048.private, "a"), str)
        # public VS private key inversion
        self.assertIsNone(sign(self.keypair2048.public, ""))
        self.assertRaises(TypeError, sign(self.keypair2048.public, ""))
        # implementation
        self.assertEqual(verify(self.keypair2048.public, "", sign(self.keypair2048.private, "")), "OK")
        self.assertEqual(verify(self.keypair2048.public, "a", sign(self.keypair2048.private, "a")), "OK")
            # we don't care about message integrity, just check sender integrity
        self.assertEqual(verify(self.keypair2048.public, "BONJOUR !", sign(self.keypair2048.private, "bonjour!")), "OK")

if __name__ == '__main__':
    unittest.main()
