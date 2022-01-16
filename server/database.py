import sqlite3

from functools import wraps
from hashlib import md5
from typing import Callable, List, Optional

from client.crypto import KeyPair

from .validation import is_username_valid, is_password_valid, is_ip_valid, is_port_valid


connection: Optional[sqlite3.Connection] = None


def is_user_registered(cursor: sqlite3.Cursor, username: str) -> bool:
    """ Check if username already exists in database """
    cursor.execute("SELECT username FROM `Users` WHERE username=?", [username])
    return len(cursor.fetchall()) > 0  # La liste est vide si username n'est pas trouvé


def user_login(cursor: sqlite3.Cursor, username: str, password: str) -> bool:
    """ Try to log in user using username and password
        Returns True if successful, False otherwise
    """
    md5_pass = md5(password.encode())
    cursor.execute("SELECT username FROM `Users` WHERE username=? AND password=?", [username, md5_pass.digest()])
    return len(cursor.fetchall()) > 0


def user_create(cursor: sqlite3.Cursor, username: str, password: str, ip_address: str, port: int) -> bool:
    """ Create a new user with the given arguments and insert it in the database
        Returns True if successful, False otherwise
    """
    # Test de validité des arguments (optionnel, doivent être vérifiés avant l'appel de cette fonction
    if is_username_valid(username) and is_password_valid(password) and is_ip_valid(ip_address) and is_port_valid(port):
        if not is_user_registered(cursor, username):
            # Création du nouvel utilisateur
            md5_pass = md5(password.encode())
            keys = KeyPair.generate(2048)
            cursor.execute("INSERT INTO `Users` VALUES(?, ?, ?, ?, ?, ?)",
                           [username, md5_pass.digest(), keys.public, keys.private, ip_address, port])
            return True
    return False


def init_db():
    """ Initialize the database. Should be called only once at server startup """
    data_base = sqlite3.connect('users.db')
    data_base.row_factory = sqlite3.Row
    cursor = data_base.cursor()

    cursor.execute("DROP TABLE IF EXISTS `Users`")
    cursor.execute("""CREATE TABLE IF NOT EXISTS `Users` (
        username TEXT UNIQUE NOT NULL,
        password VARBINARY(32) NOT NULL,
        privatekey TEXT NOT NULL,
        publickey TEXT NOT NULL,
        ip TEXT NOT NULL,
        port INT UNSIGNED
    )""")

    data_base.commit()
    data_base.close()


def connect(db_name: str):

    def decorator(function: Callable):
        @wraps(function)
        def wrapper(*args, **kwargs):
            global connection
            connection = sqlite3.connect('users.db')
            connection.row_factory = sqlite3.Row
            ret = function(*args, **kwargs)
            connection.commit()
            connection.close()
            connection = None
            return ret
        return wrapper

    return decorator
