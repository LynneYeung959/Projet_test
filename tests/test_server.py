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
    database_name = "tests/test_database.db"

    @classmethod
    def setUpClass(cls):
        server_args = (cls.server_address, cls.server_port)
        server_kwargs = {'db_name': cls.database_name, 'db_reset': True}
        cls.server_subprocess = Process(target=server.run, args=server_args, kwargs=server_kwargs)
        cls.server_subprocess.start()
        time.sleep(3)

        @server.database.connect(cls.database_name)
        def create_test_users():
            server.database.DB.user_create("leon", "0P@ssword", "127.0.0.19", 1998)
            server.database.DB.user_create("paul", "1P@ssword", "127.0.0.13", 1999)
            server.database.DB.user_create("jean", "2P@ssword", "127.0.0.99", 2000)

        create_test_users()

    @classmethod
    def tearDownClass(cls):
        cls.server_subprocess.kill()

    def test_launch_server(self):
        response = requests.get(self.server_url + "/isalive")
        self.assertEqual(response.status_code, 200)

    def test_add_user_request(self):
        # test correct user insertion
        payload = {'username': 'albert', 'password': '1MdpV@lide', 'ip': '0.0.0.1', 'port': 1235}
        response = requests.post(self.server_url + "/users", json=payload)
        self.assertEqual(response.status_code, 200)

        # correct request, but non valid password
        payload = {'username': 'alice', 'password': 'eau pet idée mer veille', 'ip': '0.0.0.14', 'port': 1236}
        response = requests.post(self.server_url + "/users", json=payload)
        self.assertEqual(response.status_code, 400)

        # incorrect request, missing data
        response = requests.post(self.server_url + "/users")
        self.assertEqual(response.status_code, 400)

        # test unsupported request type
        response = requests.get(self.server_url + "/users")
        self.assertEqual(response.status_code, 405)

        # wrong URL
        response = requests.get(self.server_url + "/user")
        self.assertEqual(response.status_code, 404)

    def test_get_ip(self):
        # correct request
        response = requests.get(self.server_url + "/users/jean/ip")
        self.assertEqual(response.status_code, 200)

        # check returned json data
        data = response.json()
        self.assertTrue('ip' in data)
        self.assertTrue('port' in data)

        # correct request, but nonexistent user
        response = requests.get(self.server_url + "/users/12$/ip")
        self.assertEqual(response.status_code, 404)

        # incorrect request (URL shall contain username)
        response = requests.get(self.server_url + "/users/ip")
        self.assertEqual(response.status_code, 405)

    def test_delete_user(self):
        # correct request
        payload = {'password': '1P@ssword'}
        response = requests.delete(self.server_url + "/users/paul", json=payload)
        self.assertEqual(response.status_code, 200)

        # incomplete request (missing data)
        response = requests.delete(self.server_url + "/users/paul")
        self.assertEqual(response.status_code, 400)

        # incorrect parameters
        payload = {'pass': '1P@ssword'}
        response = requests.delete(self.server_url + "/users/paul", json=payload)
        self.assertEqual(response.status_code, 400)

        # correct request, but incorrect credentials
        payload = {'password': 'P@ssword'}
        response = requests.delete(self.server_url + "/users/paul", json=payload)
        self.assertEqual(response.status_code, 403)

        # unsupported request
        response = requests.get(self.server_url + "/users/paul")
        self.assertEqual(response.status_code, 405)

        # try to delete all users (not allowed)
        response = requests.delete(self.server_url + "/users")
        self.assertEqual(response.status_code, 405)

    def test_create_session(self):
        # correct request
        payload = {'username': 'jean', 'password': '2P@ssword'}
        response = requests.post(self.server_url + "/sessions", json=payload)
        self.assertEqual(response.status_code, 200)

        # incomplete request (missing data)
        response = requests.post(self.server_url + "/sessions")
        self.assertEqual(response.status_code, 400)

        # incorrect parameters
        payload = {'username': 'paul'}
        response = requests.post(self.server_url + "/sessions", json=payload)
        self.assertEqual(response.status_code, 400)

        # correct request, but incorrect credentials
        payload = {'username': 'paul', 'password': 'P@ssword'}
        response = requests.post(self.server_url + "/sessions", json=payload)
        self.assertEqual(response.status_code, 403)

    def test_destroy_session(self):
        # correct request
        payload = {'password': '2P@ssword'}
        response = requests.delete(self.server_url + "/sessions/jean", json=payload)
        self.assertEqual(response.status_code, 200)

        # incomplete request (missing data)
        response = requests.delete(self.server_url + "/sessions/jean")
        self.assertEqual(response.status_code, 400)

        # incorrect parameters
        payload = {'username': 'jean'}
        response = requests.delete(self.server_url + "/sessions/jean", json=payload)
        self.assertEqual(response.status_code, 400)

        # correct request, but incorrect credentials
        payload = {'password': 'P@ssword'}
        response = requests.delete(self.server_url + "/sessions/jean", json=payload)
        self.assertEqual(response.status_code, 403)

    def test_get_session(self):
        payload = {'username': 'jean', 'password': '2P@ssword'}
        response = requests.post(self.server_url + "/sessions", json=payload)

        # correct request
        response = requests.get(self.server_url + "/sessions/jean")
        self.assertEqual(response.status_code, 200)

        # correct request, but unexistant user
        response = requests.get(self.server_url + "/sessions/da_void")
        self.assertEqual(response.status_code, 404)

        # unsupported request
        response = requests.post(self.server_url + "/sessions/jean")
        self.assertEqual(response.status_code, 405)

    def test_get_public_key(self):
        # correct request
        response = requests.get(self.server_url + "/users/leon/keys/public")
        self.assertEqual(response.status_code, 200)

        # check returned json data
        data = response.json()
        self.assertTrue('key' in data)

        # correct request, but unexistant user
        response = requests.get(self.server_url + "/users/da_void/keys/public")
        self.assertEqual(response.status_code, 404)

        # unsupported request
        response = requests.post(self.server_url + "/users/leon/keys/public")
        self.assertEqual(response.status_code, 405)

    def test_get_private_key(self):
        # correct request
        response = requests.get(self.server_url + "/users/leon/keys/private?secret=0P@ssword")
        self.assertEqual(response.status_code, 200)

        # check returned json data
        data = response.json()
        self.assertTrue('key' in data)

        # correct request, but unexistant user
        response = requests.get(self.server_url + "/users/da_void/keys/private?secret=da_p@ssw0rdo")
        self.assertEqual(response.status_code, 404)

        # correct request, but missing 'secret' argument
        response = requests.get(self.server_url + "/users/leon/keys/private")
        self.assertEqual(response.status_code, 403)

        # correct request, but wrong 'secret' argument
        response = requests.get(self.server_url + "/users/leon/keys/private?secret=wrong_password")
        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()
