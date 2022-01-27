import argparse

from .client import Client

# Command line arguments
parser = argparse.ArgumentParser(description='Launch client connected at specified address and port')
parser.add_argument('--addr', default='localhost', type=str, help='specify name server address (default : localhost)')
parser.add_argument('--port', default=80, type=int, help='specify name server port (default : 80)')
parser.add_argument('--local-port', default=5000, type=int, help='specify your local server port (default : 5000)')
args = parser.parse_args()

# Start client
client = Client(args.addr, args.port, args.local_port)
client.run()
