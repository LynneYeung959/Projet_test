import json
from threading import local

from flask import Flask, request
import requests
from .crypto import *


def run_message_server(server_url: str, my_username: str, my_pwd: str, local_port: int):
    app = Flask(__name__)

    import logging  # pylint: disable=import-outside-toplevel
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    @app.route('/msg', methods=['POST'])
    def on_msg():
        data = json.loads(request.data.decode('utf-8'))
        if 'username' not in data or 'msg' not in data:
            return "", 400
        # DECRYPT HERE
        # get my private key
        response = requests.get(server_url + '/users/' + my_username + '/keys/private?secret=' + my_pwd)
        while response.status_code != 200:
            response = requests.get(server_url + '/users/' + my_username + '/keys/private?secret=' + my_pwd)
        private_key_data = response.json()
        my_private_key = private_key_data['key']
        # decrypt msg
        decrypted_msg = decrypt(my_private_key, data['msg'])
        # print result
        print(f"\r{data['username']} > {decrypted_msg}\n>")
        return "", 200

    app.run(port=local_port)
