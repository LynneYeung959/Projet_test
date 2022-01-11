import unittest
import sqlite3
from server.database import is_username_valid 

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
'''
	def test_checkUsername(self):
        self.assertFalse(database.check_username("")) # username empty 
        self.assertTrue(database.check_username("log"))

	def test_checkIP(self):
        self.assertFalse(database.check_ip("")) # empty
        self.assertFalse(database.check_ip("1")) # bad IP 
        self.assertTrue(database.check_ip("123.283.288.283"))

    def test_checkPort(self):
        self.assertFalse(database.check_port("")) # empty
        self.assertFalse(database.check_port(80000)) # bad port
        self.assertTrue(database.check_port(8080))

    def test_addUser(self):
        self.assertFalse(database.insert_user_into_db(self.test_database,"","0.0.0.0",80)) # username empty 
        self.assertFalse(database.insert_user_into_db(self.test_database,"log","0.0.0",80)) # bad IP
        self.assertFalse(database.insert_user_into_db(self.test_database,"log","0.0.0.0",70000)) # bad port
        self.assertTrue(database.insert_user_into_db(self.test_database,"log","0.0.0.0",80)) 
        self.assertFalse(database.insert_user_into_db(self.test_database,"log","0.0.0.0",80))  # Cannot add the same user with same address and port
'''
if __name__ == '__main__':
    unittest.main()
