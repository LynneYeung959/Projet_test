import sqlite3

from functools import wraps
from hashlib import md5
from typing import Callable, Optional

from client.crypto import KeyPair

from .validation import is_username_valid, is_password_valid, is_ip_valid, is_port_valid


class Database:
    def __init__(self, file_name: str):
        self.name = file_name
        self.conn = sqlite3.connect(self.name)
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def reset(self):
        self.drop_tables()
        self.create_tables()

    def create_tables(self):
        self.conn.cursor().execute("""CREATE TABLE IF NOT EXISTS `Users` (
            username TEXT UNIQUE NOT NULL,
            password VARBINARY(32) NOT NULL,
            privatekey TEXT NOT NULL,
            publickey TEXT NOT NULL,
            ip TEXT NOT NULL,
            port INT UNSIGNED
        )""")

    def drop_tables(self):
        self.conn.cursor().execute("DROP TABLE IF EXISTS `Users`")

    def user_exists(self, username: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("SELECT username FROM `Users` WHERE username=?", [username])
        return len(cursor.fetchall()) > 0

    def user_create(self, username: str, password: str, ip_address: str, port: int) -> bool:
        """ Create a new user with the given arguments and insert it in the database
            Returns True if successful, False otherwise
        """
        # Test de validité des arguments (optionnel, doivent être vérifiés avant l'appel de cette fonction
        if is_username_valid(username) and is_password_valid(password) and is_ip_valid(ip_address) and is_port_valid(port):
            if not self.user_exists(username):
                # Création du nouvel utilisateur
                md5_pass = md5(password.encode())
                keys = KeyPair.generate(2048)
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO `Users` VALUES(?, ?, ?, ?, ?, ?)",
                               [username, md5_pass.digest(), keys.public, keys.private, ip_address, port])
                return True
        return False

    def user_login(self, username: str, password: str):
        """ Try to log in user using username and password
            Returns True if successful, False otherwise
        """
        md5_pass = md5(password.encode())
        cursor = self.conn.cursor()
        cursor.execute("SELECT username FROM `Users` WHERE username=? AND password=?", [username, md5_pass.digest()])
        return len(cursor.fetchall()) > 0


DB:  Optional[Database] = None


def connect(db_name: str) -> Callable:
    """ Decorator that opens a database connection in user function scope.
        Connection is stored in DB global variable.
    """
    def decorator(function: Callable):
        @wraps(function)
        def wrapper(*args, **kwargs):
            global DB
            DB = Database(db_name)
            ret = function(*args, **kwargs)
            DB = None
            return ret
        return wrapper

    return decorator
