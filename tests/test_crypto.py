import unittest
from Crypto.PublicKey import RSA
import sys

sys.path.append("../client")
from crypto import *

class TestCrypto(unittest.TestCase):

	# Tests sur la génération des clés privées et publiques

	def test_minimum_key_size(self):
		# Taille minium de 1024 bits
		self.assertEqual(generate_keys(512), None)
		self.assertEqual(generate_keys(0), None)
		self.assertEqual(generate_keys(1023), None)
		self.assertIsInstance(generate_keys(1024)[0], str)
		self.assertIsInstance(generate_keys(1024)[1], str)
		self.assertIsInstance(generate_keys(4096)[0], str)

	def test_key_size(self):
		# Vérification de la taille des clés
		keys_1 = generate_keys(1024)
		self.assertEqual(RSA.importKey(keys_1[0]).n.bit_length(), 1024)
		self.assertEqual(RSA.importKey(keys_1[1]).n.bit_length(), 1024)
		keys_2 = generate_keys(4096)
		self.assertEqual(RSA.importKey(keys_2[0]).n.bit_length(), 4096)
		self.assertEqual(RSA.importKey(keys_2[1]).n.bit_length(), 4096)

	def test_key_unique(self):
		# Unicité des clés privées et publiques
		self.assertNotEqual(generate_keys(2048)[0], generate_keys(2048)[0])
		self.assertNotEqual(generate_keys(1024)[0], generate_keys(1024)[0])
		self.assertNotEqual(generate_keys(2048)[1], generate_keys(2048)[1])
		keys = generate_keys(2048)
		self.assertNotEqual(keys[0], keys[1])
		

if __name__ == '__main__':
	unittest.main()