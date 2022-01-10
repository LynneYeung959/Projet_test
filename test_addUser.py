import unittest
import string
import sqlite3

import db

class TestUserSrv(unittest.TestCase):

    test_db = "test_db.db"

    def test_checkUsername(self):
        self.assertFalse(db.checkUsername("")) # username empty
        self.assertTrue(db.checkUsername("log"))
    
    def test_checkIP(self):
        self.assertFalse(db.checkIP("")) # empty
        self.assertFalse(db.checkIP("1")) # bad IP
        self.assertTrue(db.checkIP("123.283.288.283"))

    def test_checkPort(self):
        self.assertFalse(db.checkPort("")) # empty
        self.assertFalse(db.checkPort(80000)) # bad port
        self.assertTrue(db.checkPort(8080))

    def test_addUser(self):
        self.assertFalse(db.addUser(self.test_db,"","0.0.0.0",80)) # username empty 
        self.assertFalse(db.addUser(self.test_db,"log","0.0.0",80)) # bad IP
        self.assertFalse(db.addUser(self.test_db,"log","0.0.0.0",70000)) # bad port
        self.assertTrue(db.addUser(self.test_db,"log","0.0.0.0",80))
        self.assertFalse(db.addUser(self.test_db,"log","0.0.0.0",80))  # Cannot add the same user with same address and port

if __name__ == '__main__' :
    unittest.main()