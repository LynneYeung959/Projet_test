import unittest
import string
import sqlite3

import db

class TestUserSrv(unittest.TestCase):

    test_db = "test_db.db"
    
    def test_AddUser(self):
        self.assertFalse(db.AddUser(self.test_db,"",0.0.0.0,80)) # username empty 
        self.assertFalse(db.AddUser(self.test_db,"log",0.0.0,80)) # bad IP
        self.assertFalse(db.AddUser(self.test_db,"log",0.0.0.0,70000)) # bad port
        self.assertTrue(db.AddUser(self.test_db,"log",0.0.0.0,80)) 
        self.assertFalse(db.AddUser(self.test_db,"log",0.0.0.0,80))  # Cannot add the same user with same address and port

if __name__ == '__main__' :
    unittest.main()