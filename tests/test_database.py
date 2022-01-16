import unittest
from hashlib import md5

from server import database
from server.validation import is_username_valid, is_password_valid, is_ip_valid, is_port_valid
from client.crypto import KeyPair


class TestDatabase(unittest.TestCase):
    test_db: database.Database
    test_db_name = "test_database.db"

    @classmethod
    def setUpClass(cls):
        # Création d'une table SQL de test
        cls.test_db = database.Database(cls.test_db_name)
        cls.test_db.reset()

        # Remplir quelques utilisateurs arbitrairement
        users = [("Gerard", "Pa$$w0rd"), ("Noobmaster69", "xXP@ssw0rdXx")]
        for username, password in users:
            md5_pass = md5(password.encode()).digest()
            keys = KeyPair.generate(2048)
            ip_addr = "127.0.0.1"
            port = 4242
            cls.test_db.conn.cursor().execute("INSERT INTO `users` VALUES(?, ?, ?, ?, ?, ?)",
                                              [username, md5_pass, keys.public, keys.private, ip_addr, port])

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

    def test_db_connect(self):
        self.assertIsNone(database.DB)

        @database.connect('dummy.db')
        def user_function():
            self.assertIsNotNone(database.DB)
            self.assertEqual(database.DB.name, 'dummy.db')

        self.assertIsNone(database.DB)

    def test_user_exists(self):
        # Vérification de la recherche d'un utilisateur dans la base de données
        self.assertTrue(self.test_db.user_exists("Gerard"))
        self.assertTrue(self.test_db.user_exists("Noobmaster69"))

        self.assertFalse(self.test_db.user_exists("anonymous"))
        self.assertFalse(self.test_db.user_exists("gerard"))
        self.assertFalse(self.test_db.user_exists("Noobmaster"))

    def test_user_login(self):
        # Vérification du login d'un utilisateur
        self.assertTrue(self.test_db.user_login("Gerard", "Pa$$w0rd"))
        self.assertTrue(self.test_db.user_login("Noobmaster69", "xXP@ssw0rdXx"))

        self.assertFalse(self.test_db.user_login("Gerard", ""))
        self.assertFalse(self.test_db.user_login("Gerard", "wrong_password"))
        self.assertFalse(self.test_db.user_login("Gerard", "pa$$w0rd"))
        self.assertFalse(self.test_db.user_login("wrong_user", "Pa$$w0rd"))
        self.assertFalse(self.test_db.user_login("gerard", "Pa$$w0rd"))

    def test_user_create(self):
        # Tests sur la base de données après avoir créé un nouveau user
        self.assertTrue(self.test_db.user_create("NewUser1", "Pa$$w0rd1", "127.0.0.1", 4242))
        self.assertTrue(self.test_db.user_create("NewUser2", "Pa$$w0rd2", "127.0.0.1", 4242))

        # Mauvais username
        self.assertFalse(self.test_db.user_create("n3", "Pa$$w0rd3", "127.0.0.1", 4242))
        self.assertFalse(self.test_db.user_create("new_user3", "Pa$$w0rd3", "127.0.0.1", 4242))
        # Mauvais password
        self.assertFalse(self.test_db.user_create("NewUser3", "mdp", "127.0.0.1", 4242))
        # Mauvaise IP
        self.assertFalse(self.test_db.user_create("NewUser3", "Pa$$w0rd3", "fakeIP", 4242))
        # Mauvais port
        self.assertFalse(self.test_db.user_create("NewUser3", "Pa$$w0rd3", "127.0.0.1", 99999))

        # Utilisateur déjà existant
        self.assertFalse(self.test_db.user_create("Gerard", "xXP@ssw0rdXx", "127.0.0.1", 4242))
        self.assertFalse(self.test_db.user_create("NewUser2", "xXP@ssw0rdXx", "127.0.0.1", 4242))

        # Vérification de l'ajout des nouveaux utilisateurs
        cursor = self.test_db.conn.cursor()
        cursor.execute('SELECT username FROM `Users` WHERE username="NewUser1"')
        self.assertEqual(len(cursor.fetchall()), 1)

        cursor.execute('SELECT username FROM `Users` WHERE username="NewUser2"')
        self.assertEqual(len(cursor.fetchall()), 1)


if __name__ == '__main__':
    unittest.main()
