import unittest
import sqlite3
from hashlib import md5

from server.database import is_username_valid, is_password_valid, \
is_ip_valid, is_port_valid, add_user
from client.crypto import generate_keys, encrypt_message, decrypt_message

class TestDatabase(unittest.TestCase):

    # Test de validation des champs entrés par l'utilisateur :

    def test_is_username_valid(self):
        # Vérification du username
        self.assertTrue(is_username_valid("abcdefghijklmnopqrstuvwxyz1234567890"))
        self.assertTrue(is_username_valid("xXyYzZ"))
        self.assertTrue(is_username_valid("420"))

        self.assertFalse(is_username_valid(""))
        self.assertFalse(is_username_valid("a"))
        self.assertFalse(is_username_valid("_Noobmaster69_"))
        self.assertFalse(is_username_valid("HtmlGoes<br>"))
        self.assertFalse(is_username_valid("\u00C8re"))  # \u00C8 = È

    def test_is_password_valid(self):
        # Vérification du password
        self.assertTrue(is_password_valid("Abcdef#1"))
        self.assertTrue(is_password_valid("SecretPa§w0rδ"))
        self.assertTrue(is_password_valid("\u00C8ÉE{_n00b"))  # \u00C8 = È
        self.assertTrue(is_password_valid("1PassSecretδ"))

        self.assertFalse(is_password_valid("Abc#1"))
        self.assertFalse(is_password_valid("Abc123"))
        self.assertFalse(is_password_valid("Abc-#"))
        self.assertFalse(is_password_valid("HtmlGoes<br>"))
        self.assertFalse(is_password_valid("SPEACSRSEWTO"))

    def test_is_ip_valid(self):
        # Vérification de l'adresse ip
        self.assertTrue(is_ip_valid("192.168.0.0"))
        self.assertTrue(is_ip_valid("0.0.0.0"))
        self.assertTrue(is_ip_valid("127.0.0.100"))
        self.assertTrue(is_ip_valid("255.255.255.255"))

        self.assertFalse(is_ip_valid(""))
        self.assertFalse(is_ip_valid("0"))
        self.assertFalse(is_ip_valid("ceci n'est pas une ip"))
        self.assertFalse(is_ip_valid("9999.9999.9999.9999"))

    def test_is_port_valid(self):
        # Vérification du port
        self.assertTrue(is_port_valid(4242))
        self.assertTrue(is_port_valid(1024))
        self.assertTrue(is_port_valid(65535))
        self.assertTrue(is_port_valid(50000))

        self.assertFalse(is_port_valid(0))
        self.assertFalse(is_port_valid(-10))
        self.assertFalse(is_port_valid(80))
        self.assertFalse(is_port_valid(99999))

    def test_add_user(self):
        self.assertFalse(database.insert_user_into_db(self.test_database,"","0.0.0.0",80)) # username empty 
        self.assertFalse(database.insert_user_into_db(self.test_database,"log","0.0.0",80)) # bad IP
        self.assertFalse(database.insert_user_into_db(self.test_database,"log","0.0.0.0",70000)) # bad port
        self.assertTrue(database.insert_user_into_db(self.test_database,"log","0.0.0.0",80)) 
        self.assertFalse(database.insert_user_into_db(self.test_database,"log","0.0.0.0",80))  # Cannot add the same user with same address and port

if __name__ == '__main__':

    # Création d'une table SQL de test
    conn = sqlite3.connect('test_database.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS `Users`")
    cursor.execute("CREATE TABLE `Users` ( \
        `username` TEXT UNIQUE NOT NULL, \
        `password` VARBINARY(32) NOT NULL, \
        `publickey` TEXT NOT NULL, \
        `privatekey` TEXT NOT NULL, \
        `ip` TEXT NOT NULL, \
        `port` INT UNSIGNED)")

    # Remplir quelques utilisateurs arbitrairement
    users = [("Gerard", "Pa$$w0rd"), ("Noobmaster69", "xXP@ssw0rdXx")]
    for username, password in users:
        md5_pass = md5(password.encode())
        keys = generate_key(2048)
        ip = "127.0.0.1"
        port = 4242
        cursor.execute("INSERT INTO `users` VALUES(?, ?, ?, ?, ?, ?, ?)", [username, md5_pass.digest(), keys[0], keys[1], ip, port])

    unittest.main()

    conn.commit()
    conn.close()