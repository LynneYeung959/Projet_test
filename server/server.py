import argparse
import json
import logging

from flask import Flask, request

from . import database


__DEFAULT_DB = 'database.db'


def create_app(name: str = __name__, *, db: str) -> Flask:
    app = Flask(name)

    # Check server state
    @app.route('/isalive', methods=['GET'])
    def is_alive():
        return "", 200

    # Add user
    @app.route('/users', methods=['POST'])
    @database.connect(db)
    def add_user():
        data = json.loads(request.data.decode('utf-8'))
        username = data['username']
        password = data['password']
        ip_address = data['ip']
        port = data['port']
        result = database.DB.user_create(username, password, ip_address, port)

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


def create_db(name: str, reset=False):
    @database.connect(name)
    def init_db():
        if reset:
            database.DB.drop_tables()
        database.DB.create_tables()
    init_db()


def run(host=None, port=None, *, db_name=__DEFAULT_DB, db_reset=False):
    create_db(db_name, db_reset)
    app = create_app(db=db_name)
    app.run(host=host, port=port)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Launch server at specified port')
    parser.add_argument('--port', default=80, type=int, help='specify server port (default : 80)')
    parser.add_argument('--db', default=__DEFAULT_DB, type=str, help=f'specify database file (default : {__DEFAULT_DB})')
    parser.add_argument('--reset', default=False, type=bool, help='flag to reset database on launch')
    args = parser.parse_args()

    run("localhost", args.port, db_name=args.db, db_reset=args.reset)
