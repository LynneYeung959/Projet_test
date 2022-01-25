from flask import Flask, request


def run_message_server(port: int):
    app = Flask(__name__)

    import logging  # pylint: disable=import-outside-toplevel
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    @app.route('/msg', methods=['POST'])
    def on_msg():
        msg = str(request.data).encode()
        print("> received :", msg)
        return "", 200

    app.run(port=port)
