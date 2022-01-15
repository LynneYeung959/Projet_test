import sqlite3
import re
import socket
from hashlib import md5

from client.crypto import KeyPair

# Regular expression
username_regex = re.compile("([A-Za-z0-9]){3,}")
password_regex = re.compile("(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^A-Za-z0-9]).{8,}")
ip_regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"


def is_username_valid(username: str) -> bool:
    """ Check username format validity (at least 3 characters, only letters and digits allowed) """
    match = username_regex.match(username)
    return match is not None and match.group() == username


def is_password_valid(password: str) -> bool:
    """ Check password format validity (at least 8 characters with 1 digit, 1 special character and 1 uppercase) """
    match = password_regex.match(password)
    return match is not None and match.group() == password


def is_ip_valid(ip_address: str) -> bool:
    """ Check IPv4 format validity """
    try:
        socket.inet_aton(ip_address)
        if re.search(ip_regex, ip_address):
            return True
    except OSError:
        ...
    return False


def is_port_valid(port_nb: int) -> bool:
    """ Check port value validity (should be a number between 1024 and 65535 """
    return 1024 <= port_nb <= 65535


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
