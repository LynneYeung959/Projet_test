import argparse
import logging

from flask import Flask

from . import database

app = Flask(__name__)


# Check server state
@app.route('/isalive', methods=['GET'])
def is_alive():
    return "", 200


# Add user
@app.route('/users', methods=['POST'])
def add_user():
    cursor = None  # temporary, replace by database cursor
    # temporary placeholders, the values should be get from POST data
    username = "Username"
    password = "1Password"
    ip_address = "128.54.68.1"
    port = 88
    result = database.user_create(cursor, username, password, ip_address, port)
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Launch server at specified port')
    parser.add_argument('--port', default=80, help='specify server port (default : 80)')
    args = parser.parse_args()

    app.run(host='localhost', port=args.port)
