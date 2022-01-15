import unittest
from Crypto.PublicKey import RSA

from client.crypto import generate_keys, encrypt_message, decrypt_message


class TestCrypto(unittest.TestCase):

    # Tests sur la génération des clés privées et publiques

    def test_minimum_key_size(self):
        # Taille minium de 1024 bits
        self.assertEqual(generate_keys(512), None)
        self.assertEqual(generate_keys(0), None)
        self.assertEqual(generate_keys(1023), None)
        self.assertIsInstance(generate_keys(1024)[0], str)
        self.assertIsInstance(generate_keys(1024)[1], str)
        self.assertIsInstance(generate_keys(4096)[0], str)

    def test_key_size(self):
        # Vérification de la taille des clés
        keys_1 = generate_keys(1024)
        self.assertEqual(RSA.importKey(keys_1[0]).n.bit_length(), 1024)
        self.assertEqual(RSA.importKey(keys_1[1]).n.bit_length(), 1024)
        keys_2 = generate_keys(4096)
        self.assertEqual(RSA.importKey(keys_2[0]).n.bit_length(), 4096)
        self.assertEqual(RSA.importKey(keys_2[1]).n.bit_length(), 4096)

    def test_key_unique(self):
        # Unicité des clés privées et publiques
        self.assertNotEqual(generate_keys(2048)[0], generate_keys(2048)[0])
        self.assertNotEqual(generate_keys(1024)[0], generate_keys(1024)[0])
        self.assertNotEqual(generate_keys(2048)[1], generate_keys(2048)[1])
        keys = generate_keys(2048)
        self.assertNotEqual(keys[0], keys[1])

    # Tests sur le chiffrement d'un message

    def test_encryption_message(self):
        # Vérification du format du message à chiffrer
        keys = generate_keys(2048)
        msg = "abcdefghijklmnopqrstuvwxyzAZERTYUIOP\n1234567890 &éçàèùïüö\t,?;.:/!§%*µ£=+})°]@"
        self.assertEqual(encrypt_message(keys[1], ""), None)
        self.assertIsInstance(encrypt_message(keys[1], "A"), str)
        self.assertIsInstance(encrypt_message(keys[1], msg), str)

    def test_encryption_key(self):
        # Vérification de la clé
        self.assertEqual(encrypt_message("Fake key:CBVscPeuYkXW4/jjhinp", "message"), None)
        self.assertIsInstance(encrypt_message(generate_keys(2048)[1], "message"), str)

    def test_encryption_content(self):
        # Vérification du chiffrement (différent du message d'origine)
        long_msg = "abcdefghijklmnopqrstuvwxyzAZERTYUIOP\n1234567890 &éçàèùïüö\t,?;.:/!§%*µ£=+})°]@"
        self.assertNotEqual(encrypt_message(generate_keys(1024)[1], "a"), "a")
        self.assertNotEqual(encrypt_message(generate_keys(2048)[1], "message"), "message")
        self.assertNotEqual(encrypt_message(generate_keys(2048)[1], long_msg), long_msg)

    # Tests sur le déchiffrement d'un message

    def test_decryption_message(self):
        # Vérification du format du message à déchiffrer
        keys = generate_keys(2048)
        self.assertEqual(decrypt_message(keys[0], ""), None)
        self.assertEqual(decrypt_message(keys[0], "Fake_crypt_msg:CBVscPeuYkXW4/jjhinp"), None)
        self.assertIsInstance(decrypt_message(keys[0], encrypt_message(keys[1], "A")), str)

    def test_decryption_key(self):
        # Vérification de la clé
        keys = generate_keys(2048)
        self.assertEqual(decrypt_message("Fake key:CBVscPeuYkXW4/jjhinp", encrypt_message(keys[1], "A")), None)
        self.assertIsInstance(decrypt_message(keys[0], encrypt_message(keys[1], "A")), str)

    def test_decryption_content(self):
        # Vérification du déchiffrement
        keys = generate_keys(2048)
        self.assertEqual(decrypt_message(keys[0], encrypt_message(keys[1], "a")), "a")
        self.assertEqual(decrypt_message(keys[0], encrypt_message(keys[1], "Hello world !")), "Hello world !")

        msg = "abcdefghijklmnopqrstuvwxyzAZERTYUIOP\n1234567890 &éçàèùïüö\t,?;.:/!§%*µ£=+})°]@"
        encrypted_msg = encrypt_message(keys[1], msg)
        self.assertEqual(decrypt_message(keys[0], encrypted_msg), msg)


if __name__ == '__main__':
    unittest.main()
