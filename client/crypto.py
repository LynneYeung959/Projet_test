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
	pass