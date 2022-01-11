import sqlite3
import re
import socket
from hashlib import md5

from client.crypto import generate_keys

# Regular expression
username_regex = re.compile("([A-Za-z0-9]){3,}")
password_regex = re.compile("(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^A-Za-z0-9]).{8,}")
ip_regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"

def is_username_valid(username):
    """
    Vérifie si le username est au bon format :
    au moins 3 caractères, uniquement des lettres et des chiffres
    Retourne un booléen selon la validité
    """
    match = username_regex.match(username)
    return match is not None and match.group() == username

def is_password_valid(password):
    """
    Vérifie si le password est au bon format :
    au moins 8 caractères, avec au moins
    1 chiffre et 1 caractère spécial
    Retourne un booléen selon la validité
    """
    match = password_regex.match(password)
    return match is not None and match.group() == password

def is_ip_valid(ip_address):
    """
    Vérifie si l'ip est au bon format :
    On utilise la fonction inet_aton:
    si elle peut s'exécuter, l'ip est valide
    Ainsi qu'une comparaison avec les expressions régulières
    Retourne un booléen selon la validité
    """
    ip_format = re.search(ip_regex, ip_address)

    try:
        socket.inet_aton(ip_address)
        legal_ip = True
    except OSError:
        legal_ip = False

    return ip_format and legal_ip

def is_port_valid(port_nb):
    """
    Vérifie si le est au bon format :
    Le numéro de port doit être compris
    entre 1024 et 65535
    Retourne un booléen selon la validité
    """
    port_validity = 1024 <= port_nb <= 65535
    return port_validity

def is_user_registered(cursor, username):
    """
    Vérifie si username est déjà enregistré :
    Retourne un booléen selon la validité
    """
    cursor.execute("SELECT username FROM `users` WHERE username=?", [username])
    return len(cursor.fetchall()) > 0 # La liste est vide si username n'est pas trouvé

def user_login(cursor, username, password):
    """
    Vérifie si le username correspond au bon password enregistré
    Retourne un booléen selon la validité
    """
    md5_pass = md5(password.encode())
    cursor.execute("SELECT username FROM `Users` WHERE username=? AND password=?", [username, md5_pass.digest()])
    return len(cursor.fetchall()) > 0

def user_create(cursor, username, password, ip_adress, port):
    """
    Ajoute un nouvel utilisateur à la base de donnée avec:
    username, password, ip, port et la paire de clé (publique, privée)
    Retourne un booléen selon la réussite de l'opération
    """
    # Test de validité des arguments
    if not is_username_valid(username):
        return False
    if is_user_registered(cursor, username):
        return False
    if not is_password_valid(password):
        return False
    if not is_ip_valid(ip_adress):
        return False
    if not is_port_valid(port):
        return False

    # Création du nouvel utilisateur
    md5_pass = md5(password.encode())
    keys = generate_keys(2048)
    cursor.execute("INSERT INTO `Users` VALUES(?, ?, ?, ?, ?, ?)", \
    [username, md5_pass.digest(), keys[0], keys[1], ip_adress, port])

    return True

def init_db():
    """
    Créé la base de donnée
    """
    data_base = sqlite3.connect('users.db')
    data_base.row_factory = sqlite3.Row
    cursor = data_base.cursor()

    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("CREATE TABLE IF users( \
    username TEXT UNIQUE NOT NULL, \
    password VARBINARY(32) NOT NULL, \
    privatekey TEXT NOT NULL, \
    publickey TEXT NOT NULL), \
    ip TEXT NOT NULL, \
    port INT UNSIGNED)")

    data_base.commit()
    data_base.close()
