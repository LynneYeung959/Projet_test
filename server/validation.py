import re
import socket

import jsonschema

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


def validate_json(data, schema) -> bool:
    try:
        jsonschema.validate(data, schema)
    except jsonschema.exceptions.ValidationError:
        return False
    return True
