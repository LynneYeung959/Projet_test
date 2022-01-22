import argparse
import json

from flask import Flask, request, jsonify

from . import database


__DEFAULT_DB = 'database.db'


def create_app(name: str = __name__, *, db: str) -> Flask:
    app = Flask(name)
    app.client_sessions = []

    # Check server state
    @app.route('/isalive', methods=['GET'])
    def is_alive():
        return "", 200

    # Add user
    @app.route('/users', methods=['POST'])
    @database.connect(db)
    def add_user():
        if not request.data:
            return "", 400

        data = json.loads(request.data.decode('utf-8'))
        username = data['username']
        password = data['password']
        ip_address = request.remote_addr
        port = request.environ.get('REMOTE_PORT')
        result = database.DB.user_create(username, password, ip_address, port)

        if not result:
            return "", 400
        return "", 200

    # Get IP with username
    @app.route('/users/<string:username>/ip', methods=['GET'])
    @database.connect(db)
    def get_user_ip(username):
        if not database.DB.user_exists(username):
            return "", 404
        ip, port = database.DB.get_user_address(username)
        return jsonify({'ip': ip, 'port': port}), 200

    # Delete user with username
    @app.route('/users/<string:username>', methods=['DELETE'])
    @database.connect(db)
    def delete_user(username):
        if not request.data:
            return "", 400

        data = json.loads(request.data.decode('utf-8'))

        if 'password' not in data:
            return "", 400

        if not database.DB.user_login(username, data['password']):
            return "", 403

        cursor = database.DB.conn.cursor()
        cursor.execute("DELETE FROM `Users` WHERE username=?", [username])

        return "", 200

    # Login user
    @app.route('/sessions', methods=['POST'])
    @database.connect(db)
    def create_session():
        if not request.data:
            return "", 400

        data = json.loads(request.data.decode('utf-8'))

        if 'username' not in data or 'password' not in data:
            return "", 400

        if not database.DB.user_login(data['username'], data['password']):
            return "", 403

        app.client_sessions.append(data['username'])

        return "", 200

    # Logout user
    @app.route('/sessions/<string:username>', methods=['DELETE'])
    @database.connect(db)
    def destroy_session(username):
        if not request.data:
            return "", 400

        data = json.loads(request.data.decode('utf-8'))

        if 'password' not in data:
            return "", 400

        if not database.DB.user_login(username, data['password']):
            return "", 403

        app.client_sessions.remove(username)

        return "", 200

    # Check if user logged in
    @app.route('/sessions/<string:username>', methods=['GET'])
    def get_session(username):
        if username in app.client_sessions:
            return "", 200
        return "", 404

    return app


def create_db(name: str, reset=False):
    @database.connect(name)
    def init_db():
        if reset:
            database.DB.drop_tables()
        database.DB.create_tables()
    init_db()


def run(host=None, port=None, *, db_name=__DEFAULT_DB, db_reset=False):
    print(f"Running server at {host}:{port}")
    print(f"Using database {db_name} (reset={db_reset})")
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
