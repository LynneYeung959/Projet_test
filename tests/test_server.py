import unittest
import requests
import shlex
import subprocess
import time

import sys
sys.path.append('../server')

import server

class TestServer(unittest.TestCase):

	server_subprocess = None

	test_port = "5000"
	server_address = "127.0.0.1"
	server_url = "http://" + server_address + ":" + test_port

	def set_up(self):
		cmd = "python3 ../server/server.py --port="+self.test_port
		print("wesh")
		args = shlex.split(cmd)
		self.server_subprocess  = subprocess.Popen(args) # launch command as a subprocess
		time.sleep(3)

	def tear_down(self):
		print("killing subprocess server")
		self.server_subprocess.kill()
		self.server_subprocess.wait()

	def test_launch_server(self):
		response = requests.get(self.server_url+"/isalive")
		self.assertEqual(response.status_code,200)

if __name__ == '__main__':
	unittest.main()