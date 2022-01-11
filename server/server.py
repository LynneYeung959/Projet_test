"""server
Usage:
	server.py --port=<int>
Options:
	-h --help     Show this screen.
	--port=<int>  port used
"""
import logging
from docopt import docopt
from flask import Flask
from flask import Response
from flask import request

import database as db


APP = Flask(__name__)

# Check server state
@APP.route('/isalive', methods=['GET'])
def is_alive():
	return Response(status=200)



# Add user
@APP.route('/users', methods=['POST'])
def add_user():
	data = request.form
	result = db.insert_user_into_db(data['username'], data['IP'], int(data['port']))
	if not result:
		logging.warning("Failed to register user")
		return Response(status=404)
	return Response(status=200)

# Get IP with username
@APP.route('/users/<string:username>/ip', methods=['GET'])
def get_IP(username):
	pass

# Delete user with username
@APP.route('/users/<string:username>', methods=['DELETE'])
def delete_user(username):
	pass



if __name__ == '__main__':
	db.init_db()
	db.dump_db()
	APP.run()
	# ARGS = docopt(__doc__)
	# if ARGS['--port']:
	# 	APP.run(host='0.0.0.0', port=ARGS['--port'])
	# else:
	# 	logging.error("Wrong command line arguments")