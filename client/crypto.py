import base64
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

def generate_keys(key_size):
	"""
	Genére une paire de clé privée / publique
	de la taille key_size d'au minimum 1024 bits
	Retourne les deux clés au format string sous 
	la forme d'une liste de deux éléments
	"""
	if key_size < 1024:
		return None
	else:
		random_gen = Random.new().read

		# Génération de la paire de clé de taille key_size
		private_key = RSA.generate(key_size, random_gen)
		public_key  = private_key.publickey()

		# Conversion des clés au format texte (type string)
		private_key_str = private_key.exportKey().decode()
		public_key_str  = public_key.exportKey().decode()

		return private_key_str, public_key_str

def encrypt_message(public_key, message):
	"""
	Chiffrement d'un message à partir d'une clé publique
	Retourne le message crypté au format string
	"""
	if message == "":
		return None
	else:
		# Conversion de la clé publique de string vers RSA_key_format
		# lorsque celle-ci est valide
		try:
			key = RSA.importKey(public_key)
		except ValueError:
			return None

		encryptor = PKCS1_OAEP.new(key)
		msg_crypt = base64.b64encode(encryptor.encrypt(message.encode()))
		
		# Conversion au format texte (type string)
		msg_crypt_str = msg_crypt.decode()
		
		return msg_crypt_str

def decrypt_message(private_key, crypt_message):
	pass