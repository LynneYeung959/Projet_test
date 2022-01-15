import argparse
import logging

from flask import Flask
from flask import Response

from . import database

app = Flask(__name__)


# Check server state
@app.route('/isalive', methods=['GET'])
def is_alive():
    return Response(status=200)


# Add user
@app.route('/users', methods=['POST'])
def add_user(username, ip_address, port):
    cursor = None  # temporary, replace by database cursor
    password = "1Password"  # temporary, replace by POST value from client
    result = database.user_create(cursor, username, password, ip_address, port)
    if not result:
        logging.warning("Failed to register user")
        return Response(status=404)
    return Response(status=200)


# Get IP with username
@app.route('/users/<string:username>/ip', methods=['GET'])
def get_ip(username):  # pylint: disable=unused-argument
    pass


# Delete user with username
@app.route('/users/<string:username>', methods=['DELETE'])
def delete_user(username):  # pylint: disable=unused-argument
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Launch server at specified port')
    parser.add_argument('--port', default=80, help='specify server port (default : 80)')
    args = parser.parse_args()

    app.run(host='localhost', port=args.port)
