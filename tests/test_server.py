import time
import unittest

from multiprocessing import Process

import requests

from server import server


class TestServer(unittest.TestCase):
    server_subprocess: Process
    server_address = "127.0.0.1"
    server_port = "1234"
    server_url = "http://" + server_address + ":" + server_port

    @classmethod
    def setUpClass(cls):
        cls.server_subprocess = Process(target=server.run, args=(cls.server_address, cls.server_port))
        cls.server_subprocess.start()
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        cls.server_subprocess.kill()

    def test_launch_server(self):
        response = requests.get(self.server_url + "/isalive")
        self.assertEqual(response.status_code, 200)

    def test_add_user_request(self):
        # test correct user insertion
        payload = {'username': 'alice', 'IP': '0.0.0.14', 'port': '1236'}
        response = requests.post(self.server_url + "/users", data=payload)
        self.assertEqual(response.status_code, 200)

        # test multiple users insertion with same username (should fail)
        payload = {'username': 'albert', 'IP': '0.0.0.0', 'port': '1234'}
        response = requests.post(self.server_url + "/users", data=payload)
        payload = {'username': 'albert', 'IP': '0.0.0.1', 'port': '1235'}
        response = requests.post(self.server_url + "/users", data=payload)
        self.assertEqual(response.status_code, 404)

        # test unsupported request type
        response = requests.get(self.server_url + "/users")
        self.assertEqual(response.status_code, 405)

        # wrong URL
        response = requests.get(self.server_url + "/user")
        self.assertEqual(response.status_code, 404)

    def test_get_ip(self):
        # correct request
        response = requests.get(self.server_url + "/users/paul/ip")
        self.assertEqual(response.status_code, 200)

        # correct request (should fail later)
        response = requests.get(self.server_url + "/users/12$/ip")
        self.assertEqual(response.status_code, 200)

        # incorrect request (URL shall contain username)
        response = requests.get(self.server_url + "/users/ip")
        self.assertEqual(response.status_code, 404)

    def test_delete_user(self):
        # correct request
        response = requests.delete(self.server_url + "/users/paul")
        self.assertEqual(response.status_code, 200)

        # unsupported request
        response = requests.get(self.server_url + "/users/paul")
        self.assertEqual(response.status_code, 405)

        # try to delete all users (not allowed)
        response = requests.delete(self.server_url + "/users")
        self.assertEqual(response.status_code, 405)


if __name__ == '__main__':
    unittest.main()
