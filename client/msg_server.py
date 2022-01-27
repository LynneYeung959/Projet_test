import json

from flask import Flask, request
from .crypto import decrypt, verify

import requests

def run_message_server(server_url: str, local_port: int, private_key: str):
    app = Flask(__name__)

    import logging  # pylint: disable=import-outside-toplevel
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    @app.route('/msg', methods=['POST'])
    def on_msg():
        data = json.loads(request.data.decode('utf-8'))
        if 'username' not in data or 'msg' not in data or 'signature' not in data:
            return "", 400
            
        sender = data['username']
        message = data['msg']
        signature = data['signature']
        
        # CHECK SENDER INTERGRITY
        # get sender public key
        response = requests.get(server_url + '/users/' + sender + '/keys/public')
        if response.status_code == 200:
            sender_public_key_data = response.json()
        elif response.status_code == 404:
            print(f"\rCAUTION ! Sender \'{sender}\' does not exist in database, they might not be who they seem to be !\n")
        sender_public_key = sender_public_key_data['key']
        assert verify(sender_public_key, message, signature) == "OK"

        # DECRYPT HERE
        # decrypt msg
        decrypted_msg = decrypt(private_key, message)

        # print result
        print(f"\r{data['username']} > {decrypted_msg}\n>")
        return "", 200

    app.run(port=local_port)
