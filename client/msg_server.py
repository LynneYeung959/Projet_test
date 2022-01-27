import json

from flask import Flask, request
from .crypto import decrypt


def run_message_server(private_key: str, local_port: int):
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
        # decrypt msg
        decrypted_msg = decrypt(private_key, data['msg'])
        # print result
        print(f"\r{data['username']} > {decrypted_msg}\n>")
        return "", 200

    app.run(port=local_port)
