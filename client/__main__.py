import argparse
import sys
import time

from multiprocessing import Process

import requests

from .msg_server import run_message_server

parser = argparse.ArgumentParser(description='Launch client connected at specified address and port')
parser.add_argument('--addr', default='localhost', type=str, help='specify name server address (default : localhost)')
parser.add_argument('--port', default=80, type=int, help='specify name server port (default : 80)')
parser.add_argument('--local-port', default=5000, type=int, help='specify your local server port (default : 5000)')
args = parser.parse_args()

server_url = f"http://{args.addr}:{args.port}"

# check if server address exists and is alive
try:
    response = requests.get(server_url + '/isalive')
    if response.status_code != 200:
        print(f"Server at {server_url} is down !")
except requests.exceptions.ConnectionError:
    print(f"Failed to connect to {server_url} !")
    sys.exit(1)

print("Your username (at least 3 characters, only letters or digits) : ")
username = input("> ")

# check if user exists by getting its IP from server
response = requests.get(server_url + '/users/' + username + '/ip')

# connect and login user
if response.status_code == 404:
    print(f"Welcome {username} !\n"
          f"Create your account by entering a new password\n"
          f"(at least 8 characters, at least 1 uppercase, 1 digit and 1 special character)")
    password = input("> ")
    data = {'username': username, 'password': password}
    response = requests.post(server_url + '/users', json=data)
    while response.status_code != 200:
        print("Bad inputs, please try again :")
        username = input("Your username : ")
        password = input("Your password : ")
        data = {'username': username, 'password': password}
        response = requests.post(server_url + '/users', json=data)

    print("Account created successfully !")

else:
    print(f"Welcome back {username} !\n"
          f"Please enter your password to log in :")
    password = input("> ")
    data = {'username': username, 'password': password}
    response = requests.post(server_url + '/sessions', json=data)
    while response.status_code != 200:
        print("Bad credentials, please try again :")
        username = input("Your username : ")
        password = input("Your password : ")
        data = {'username': username, 'password': password}
        response = requests.post(server_url + '/sessions', json=data)

    print("Logged in successfully !")

# user logged in, run their message server
Process(target=run_message_server, kwargs={'port': args.local_port}).start()
time.sleep(3)

# here : print connected users list
dest = input("You want to talk with : ")
response = requests.get(server_url + '/sessions/' + dest)

while response.status_code != 200:
    print(f"{dest} is not connected right now")
    # here : print connected users list again to see if someone just connected
    dest = input("You want to talk with : ")
    response = requests.get(server_url + '/sessions/' + dest)

response = requests.get(server_url + '/users/' + dest + '/ip')

while response.status_code != 200:
    print(f'User {dest} is not connected !')
    dest = input("You want to talk with : ")
    response = requests.get(server_url + '/users/' + dest + '/ip')

data = response.json()
dest_address = f"http://{data['ip']}:{data['port']}"

# wait for their input
while True:
    msg = input("> ")
    requests.post(dest_address + '/msg', data=msg)
