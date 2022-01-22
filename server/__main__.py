import argparse

from . import server


__DEFAULT_DB = 'database.db'

parser = argparse.ArgumentParser(description='Launch server at specified port')
parser.add_argument('--port', default=80, type=int, help='specify server port (default : 80)')
parser.add_argument('--db', default=__DEFAULT_DB, type=str, help=f'specify database file (default : {__DEFAULT_DB})')
parser.add_argument('--reset', default=False, type=bool, help='flag to reset database on launch')
args = parser.parse_args()

server.run("localhost", args.port, db_name=args.db, db_reset=args.reset)
