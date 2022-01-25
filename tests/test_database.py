import unittest
from hashlib import md5
from typing import Callable, Optional, Tuple

from server import database
from client.crypto import KeyPair


class TestDatabase(unittest.TestCase):
    test_db: database.Database
    test_db_name = "tests/test_database.db"

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

    @classmethod
    def tearDownClass(cls):
        del cls.test_db

    def test_db_connect(self):
        self.assertIsNone(database.DB)
        dummy_db = 'tests/dumy.db'

        @database.connect(dummy_db)
        def user_function():
            self.assertIsNotNone(database.DB)
            self.assertEqual(database.DB.name, dummy_db)

        user_function()

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

    def test_getter_functions(self):
        # Tests de get_user_address
        self.assertIsInstance(self.test_db.get_user_address("Gerard"), tuple)
        self.assertIsInstance(self.test_db.get_user_address("Gerard")[0], str)
        self.assertIsInstance(self.test_db.get_user_address("Gerard")[1], int)
        self.assertIsInstance(self.test_db.get_user_address("Noobmaster69"), tuple)

        # Tests de get_private_key

        # Tests de get_public_key

if __name__ == '__main__':
    unittest.main()
