import logging
import sqlite3


def get_db():
	db = sqlite3.connect('users.db')
	db.row_factory = sqlite3.Row
	return db

def init_db():
	db = get_db()
	cursor = db.cursor()
	cursor.execute("DROP TABLE IF EXISTS users")
	cursor.execute('''CREATE TABLE IF NOT EXISTS users
              (username TEXT UNIQUE NOT NULL, IP INT UNSIGNED, PORT INT UNSIGNED)''')
	db.commit()
	db.close()

def dump_db():
	db = get_db()
	cursor = db.cursor()
	cursor.execute("SELECT * FROM users")
	rows = cursor.fetchall()
	dump_result = []
	for row in rows:
		dump_result.append([row['id'], row['valeur']])
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
	if port < 0 or port > 65535 or type(port) is not int:
		logging.error("Port number incorrect (must be integer between 0 and 65535)")
		return False

	command = "INSERT INTO users(username, IP, PORT) VALUES (?, ?, ?)"
	cursor.execute(command, [username, ip_address, port])
	db.commit()
	return True