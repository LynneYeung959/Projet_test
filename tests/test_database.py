import unittest
<<<<<<< Updated upstream
import sqlite3
from server.database import *
=======
>>>>>>> Stashed changes

class TestDatabase(unittest.TestCase):

	def test_checkUsername(self):
        self.assertFalse(database.check_username("")) # username empty 
        self.assertTrue(database.check_username("log"))
<<<<<<< Updated upstream

=======
  
>>>>>>> Stashed changes
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

if __name__ == '__main__':
    unittest.main()
