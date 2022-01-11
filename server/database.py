import logging
import sqlite3
import re

# Regular expression
username_regex = re.compile("([A-Za-z0-9]){3,}")
password_regex = re.compile("(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^A-Za-z0-9]).{8,}")

def is_username_valid(username):
	"""
	Vérifie si le username est au bon format :
	au moins 3 caractères, uniquement des lettres et des chiffres
	Retourne un booléen selon la validité
	"""
	match = username_regex.match(username)
	return match is not None and match.group() == username

def get_db():
	db = sqlite3.connect('users.db')
	db.row_factory = sqlite3.Row
	return db

def init_db():
	db = get_db()
	cursor = db.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS users( \
    username TEXT UNIQUE NOT NULL, \
    password VARBINARY(32) NOT NULL, \
    ip TEXT NOT NULL, \
    port INT UNSIGNED, \
    privatekey TEXT NOT NULL, \
    publickey TEXT NOT NULL)")
	db.commit()
	db.close()

def dump_db():
	db = get_db()
	cursor = db.cursor()
	cursor.execute("SELECT * FROM users")
	rows = cursor.fetchall()
	dump_result = []
	for row in rows:
		dump_result.append([row['username'], row['IP'], row['PORT']])
	db.commit()
	db.close()
	print(dump_result)

def insert_user_into_db(username, ip_address, port):
	db = get_db()
	cursor = db.cursor()

	if not username or type(username) is not str:
		logging.error("Username incorrect (must be string not empty)")
		return False


	if not ip_address or type(ip_address) is not str:
		logging.error("IP address incorrect (must be string not empty)")
		return False
		
	addr = ip_address.strip().split('.')
	if len(addr) != 4:
    	logging.error("IP address incorrect (bas size)")
    	return False
	for num in addr:
    	try:
        	num=int(num)
    	except:
        	logging.error("IP address incorrect (not int)")
        	return False
    	if num < 0 or num > 255: 
        	logging.error("IP address incorrect (there is at least one part of IP address not between 0 and 255)")
        	return False
	
	if port < 0 or port > 65535 or type(port) is not int:
		logging.error("Port number incorrect (must be integer between 0 and 65535)")
		return False

	command = "INSERT INTO users(username, IP, PORT) VALUES (?, ?, ?)"
	cursor.execute(command, [username, ip_address, port])
	db.commit()
	return True