import json

from flask import Flask, request, jsonify

from . import database
from .validation import validate_json


USER_PASS_PORT_SCHEMA = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
        "port": {"type": "number"},
    },
    "required": ["username", "password", "port"],
    "additionalProperties": False
}

USER_PASS_SCHEMA = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["username", "password"],
    "additionalProperties": False
}

PASS_PORT_SCHEMA = {
    "type": "object",
    "properties": {
        "password": {"type": "string"},
        "port": {"type": "number"},
    },
    "required": ["password", "port"],
    "additionalProperties": False
}

PASS_SCHEMA = {
    "type": "object",
    "properties": {
        "password": {"type": "string"},
    },
    "required": ["password"],
    "additionalProperties": False
}


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

        if not validate_json(data, USER_PASS_PORT_SCHEMA):
            return "", 400

        username = data['username']
        password = data['password']
        ip_address = request.remote_addr
        port = data['port']
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

    # Update port with username and password
    @app.route('/users/<string:username>/ip', methods=['PUT'])
    @database.connect(db)
    def update_user_ip(username):
        if not database.DB.user_exists(username):
            return "", 404

        data = json.loads(request.data.decode('utf-8'))

        if not validate_json(data, PASS_PORT_SCHEMA):
            return "", 400

        if not database.DB.user_login(username, data['password']):
            return "", 403

        database.DB.update_user_port(username, data['port'])
        return "", 200

    # Get public key with username
    @app.route('/users/<string:username>/keys/public', methods=['GET'])
    @database.connect(db)
    def get_user_public_key(username):
        if not database.DB.user_exists(username):
            return "", 404

        key = database.DB.get_public_key(username)

        return jsonify({'key': key}), 200

    # Get private key with username and password
    @app.route('/users/<string:username>/keys/private', methods=['GET'])
    @database.connect(db)
    def get_user_private_key(username):
        password = request.args.get('secret')

        if not database.DB.user_exists(username):
            return "", 404

        if not password or not database.DB.user_login(username, password):
            return "", 403

        key = database.DB.get_private_key(username)

        return jsonify({'key': key}), 200

    # Delete user with username and password
    @app.route('/users/<string:username>', methods=['DELETE'])
    @database.connect(db)
    def delete_user(username):
        if not request.data:
            return "", 400

        data = json.loads(request.data.decode('utf-8'))

        if not validate_json(data, PASS_SCHEMA):
            return "", 400

        if not database.DB.user_login(username, data['password']):
            return "", 403

        cursor = database.DB.conn.cursor()
        cursor.execute("DELETE FROM `Users` WHERE username=?", [username])

        return "", 200

    # List users online
    @app.route('/sessions', methods=['GET'])
    def get_sessions():
        return jsonify(app.client_sessions), 200

    # Login user
    @app.route('/sessions', methods=['POST'])
    @database.connect(db)
    def create_session():
        if not request.data:
            return "", 400

        data = json.loads(request.data.decode('utf-8'))

        if not validate_json(data, USER_PASS_SCHEMA):
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

        if not validate_json(data, PASS_SCHEMA):
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


def run(host=None, port=None, *, db_name, db_reset=False):
    print(f"Running server at {host}:{port}")
    print(f"Using database file '{db_name}' (reset={db_reset})")
    create_db(db_name, db_reset)
    app = create_app(db=db_name)
    app.run(host=host, port=port)
