import json

from flask import Flask, request


def run_message_server(port: int):
    app = Flask(__name__)

    import logging  # pylint: disable=import-outside-toplevel
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    @app.route('/msg', methods=['POST'])
    def on_msg():
        data = json.loads(request.data.decode('utf-8'))
        if 'username' not in data or 'msg' not in data:
            return "", 400

        if data['msg'] == "/exit":
            print(f"{data['username']} left the chat.")
        else:
            print(f"\r{data['username']} > {data['msg']}\n>")

        return "", 200

    app.run(port=port)
