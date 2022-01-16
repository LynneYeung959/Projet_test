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
    database_name = "test_database.db"

    @classmethod
    def setUpClass(cls):
        server_args = (cls.server_address, cls.server_port)
        server_kwargs = {'db_name': cls.database_name, 'db_reset': True}
        cls.server_subprocess = Process(target=server.run, args=server_args, kwargs=server_kwargs)
        cls.server_subprocess.start()
        time.sleep(3)

        @server.database.connect(cls.database_name)
        def create_test_users():
            server.database.DB.user_create("paul", "1P@ssword", "127.0.0.13", 1999)

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
        response = requests.get(self.server_url + "/users/paul/ip")
        self.assertEqual(response.status_code, 200)

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
        payload = {'user': 'paul', 'password': '1P@ssword'}
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

        # unsupported request
        response = requests.get(self.server_url + "/sessions")
        self.assertEqual(response.status_code, 405)


if __name__ == '__main__':
    unittest.main()
