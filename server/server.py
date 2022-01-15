import argparse
import json
import logging
import sqlite3

from flask import Flask, request

from . import database


def create_app(name: str = __name__) -> Flask:
    app = Flask(name)

    # Check server state
    @app.route('/isalive', methods=['GET'])
    def is_alive():
        return "", 200

    # Add user
    @app.route('/users', methods=['POST'])
    def add_user():
        # TODO : database decorator
        data_base = sqlite3.connect('users.db')
        data_base.row_factory = sqlite3.Row
        cursor = data_base.cursor()

        data = json.loads(request.data.decode('utf-8'))
        username = data['username']
        password = data['password']
        ip_address = data['ip']
        port = data['port']
        result = database.user_create(cursor, username, password, ip_address, port)

        data_base.commit()
        data_base.close()
        if not result:
            logging.warning("Failed to register user")
            return "", 404
        return "", 200

    # Get IP with username
    @app.route('/users/<string:username>/ip', methods=['GET'])
    def get_ip(username):  # pylint: disable=unused-argument
        return "", 405

    # Delete user with username
    @app.route('/users/<string:username>', methods=['DELETE'])
    def delete_user(username):  # pylint: disable=unused-argument
        return "", 405

    return app


def run(host=None, port=None):
    database.init_db()
    app = create_app()
    app.run(host=host, port=port)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Launch server at specified port')
    parser.add_argument('--port', default=80, help='specify server port (default : 80)')
    args = parser.parse_args()

    run("localhost", args.port)
