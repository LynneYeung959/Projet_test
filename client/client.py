import argparse
import sys
import os
import signal
import time
import requests
from threading import Thread
from multiprocessing import Process

from .msg_server import run_message_server

def signal_handler(signal, frame):
    print("User exit programm with Crtl+c")
    os._exit(1)

class ThreadClient(Thread):

    def run(self):
        client = Client()
        client.run()

class Client():

    def __init__(self):
        # Command line arguments
        parser = argparse.ArgumentParser(description='Launch client connected at specified address and port')
        parser.add_argument('--addr', default='localhost', type=str, help='specify name server address (default : localhost)')
        parser.add_argument('--port', default=80, type=int, help='specify name server port (default : 80)')
        parser.add_argument('--local-port', default=5000, type=int, help='specify your local server port (default : 5000)')
        args = parser.parse_args()

        self.server_addr = args.addr
        self.server_port = args.port
        self.port = args.local_port
        self.server_url = f"http://{self.server_addr}:{self.server_port}"

        self.ip: str
        self.username: str
        self.password: str

    def checkServer(self):
        # Check if server address exists and is alive
        try:
            response = requests.get(self.server_url + '/isalive')
            if response.status_code != 200:
                print(f"Server at {self.server_url} is down !")
        except requests.exceptions.ConnectionError:
            print(f"Failed to connect to {self.server_url} !")
            os._exit(1)

    def run(self):

        self.checkServer()

        print("Your username (at least 3 characters, only letters or digits) : ")
        self.username = input("> ")
        # check if user exists by getting its IP from server
        get_ip_response = requests.get(self.server_url + '/users/' + self.username + '/ip')

        # connect and login user
        if get_ip_response.status_code == 404:
            print(f"Welcome {self.username} !\n"
                  f"Create your account by entering a new password\n"
                  f"(at least 8 characters, at least 1 uppercase, 1 digit and 1 special character)")
            self.password = input("> ")
            data = {'username': self.username, 'password': self.password, 'port': self.port}
            response = requests.post(self.server_url + '/users', json=data)
            while response.status_code != 200:
                print("Bad inputs, please try again :")
                self.username = input("Your username : ")
                self.password = input("Your password : ")
                data = {'username': self.username, 'password': self.password, 'port': self.port}
                response = requests.post(self.server_url + '/users', json=data)

            response = requests.post(self.server_url + '/sessions', json=data)
            print("Account created successfully !")

        else:
            print(f"Welcome back {self.username} !\n"
                  f"Please enter your password to log in :")
            self.password = input("> ")
            data = {'username': self.username, 'password': self.password, 'port': self.port}
            response = requests.post(self.server_url + '/sessions', json=data)
            while response.status_code != 200:
                print("Bad credentials, please try again :")
                self.username = input("Your username : ")
                self.password = input("Your password : ")
                data = {'username': self.username, 'password': self.password, 'port': self.port}
                response = requests.post(self.server_url + '/sessions', json=data)

            get_ip_data = get_ip_response.json()
            if get_ip_data['port'] != self.port:
                requests.put(self.server_url + '/users/' + self.username + '/ip', json={'password': self.password, 'port': self.port})

            print("Logged in successfully !")

        # user logged in, run their message server
        Process(target=run_message_server, kwargs={'port': self.port}).start()
        time.sleep(3)

        # print connected users list
        print("Users online :")
        response = requests.get(self.server_url + '/sessions')
        user_list = response.json()
        for user in user_list:
            if user == self.username:
                print("* " + user + " (You)")
            else:
                print("* " + user)

        print("")

        dest = input("You want to talk with : ")
        response = requests.get(self.server_url + '/sessions/' + dest)

        while response.status_code != 200:
            print(f"{dest} is not connected right now")
            # here : print connected users list again to see if someone just connected
            dest = input("You want to talk with : ")
            response = requests.get(self.server_url + '/sessions/' + dest)

        response = requests.get(self.server_url + '/users/' + dest + '/ip')

        while response.status_code != 200:
            print(f'User {dest} is not connected !')
            dest = input("You want to talk with : ")
            response = requests.get(self.server_url + '/users/' + dest + '/ip')

        data = response.json()
        dest_address = f"http://{data['ip']}:{data['port']}"

        # wait for their input
        while True:
            msg = input("\r> ")

            if (msg == "/exit"):
                requests.delete(self.server_url + "/sessions/" + self.username, json={'password': self.password})
                requests.post(dest_address + '/msg', json={'username': self.username, 'msg': msg})
                os._exit(1)

            elif (msg == "/list"):
                # print connected users list
                print("Users online :")
                response = requests.get(self.server_url + '/sessions')
                user_list = response.json()
                for user in user_list:
                    if user == self.username:
                        print("* " + user + " (You)")
                    else:
                        print("* " + user)
                print("")

            else:
                requests.post(dest_address + '/msg', json={'username': self.username, 'msg': msg})