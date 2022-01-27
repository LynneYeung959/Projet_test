import sys
import os
import signal as sig
import time

import json
from multiprocessing import Process
import threading
import requests
from flask import Flask, request


class Client():

    def __init__(self, addr, port, local_port):

        self.server_addr = addr
        self.server_port = port
        self.port = local_port
        self.server_url = f"http://{self.server_addr}:{self.server_port}"

        self.ip: str
        self.username: str
        self.password: str
        self.dest_address: str

        self.connected = False

    def checkServer(self):
        # Check if server address exists and is alive
        try:
            response = requests.get(self.server_url + '/isalive')
            if response.status_code != 200:
                print(f"Server at {self.server_url} is down !")
        except requests.exceptions.ConnectionError:
            print(f"Failed to connect to {self.server_url} !")
            sys.exit(0)

    def displayBanner(self):
        print("")
        print("=======================================================================================")
        print("")
        print("$$\\       $$$$$$$$\\       $$$$$$$\\ $$\\     $$\\  $$$$$$\\  $$$$$$$$\\  $$$$$$\\  $$\\   $$\\ ")
        print("$$ |      $$  _____|      $$  __$$\\\\$$\\   $$  |$$  __$$\\ $$  _____|$$  __$$\\ $$$\\  $$ |")
        print("$$ |      $$ |            $$ |  $$ |\\$$\\ $$  / $$ /  \\__|$$ |      $$ /  $$ |$$$$\\ $$ |")
        print("$$ |      $$$$$\\          $$$$$$$  | \\$$$$  /  $$ |$$$$\\ $$$$$\\    $$ |  $$ |$$ $$\\$$ |")
        print("$$ |      $$  __|         $$  ____/   \\$$  /   $$ |\\_$$ |$$  __|   $$ |  $$ |$$ \\$$$$ |")
        print("$$ |      $$ |            $$ |         $$ |    $$ |  $$ |$$ |      $$ |  $$ |$$ |\\$$$ |")
        print("$$$$$$$$\\ $$$$$$$$\\       $$ |         $$ |    \\$$$$$$  |$$$$$$$$\\  $$$$$$  |$$ | \\$$ |")
        print("\\________|\\________|      \\__|         \\__|     \\______/ \\________| \\______/ \\__|  \\__|")
        print("                                                                                       ")
        print("                                                                                       ")
        print("                                                                                       ")
        print("$$\\    $$\\  $$$$$$\\ $$\\     $$\\  $$$$$$\\   $$$$$$\\  $$$$$$$$\\ $$\\   $$\\ $$$$$$$\\       ")
        print("$$ |   $$ |$$  __$$\\\\$$\\   $$  |$$  __$$\\ $$  __$$\\ $$  _____|$$ |  $$ |$$  __$$\\      ")
        print("$$ |   $$ |$$ /  $$ |\\$$\\ $$  / $$ /  $$ |$$ /  \\__|$$ |      $$ |  $$ |$$ |  $$ |     ")
        print("\\$$\\  $$  |$$ |  $$ | \\$$$$  /  $$$$$$$$ |$$ |$$$$\\ $$$$$\\    $$ |  $$ |$$$$$$$  |     ")
        print(" \\$$\\$$  / $$ |  $$ |  \\$$  /   $$  __$$ |$$ |\\_$$ |$$  __|   $$ |  $$ |$$  __$$<      ")
        print("  \\$$$  /  $$ |  $$ |   $$ |    $$ |  $$ |$$ |  $$ |$$ |      $$ |  $$ |$$ |  $$ |     ")
        print("   \\$  /    $$$$$$  |   $$ |    $$ |  $$ |\\$$$$$$  |$$$$$$$$\\ \\$$$$$$  |$$ |  $$ |     ")
        print("    \\_/     \\______/    \\__|    \\__|  \\__| \\______/ \\________| \\______/ \\__|  \\__|     ")
        print("")
        print("===========================================================================================")
        print("\n\n")
        print("Welcome to this very, very secure chat app!\n")
        print(f"Server adress : {self.server_url}")
        print(f"Local port : {self.port}")

    def displaySessions(self):

        print("Users online :")
        response = requests.get(self.server_url + '/sessions')
        user_list = response.json()
        for user in user_list:
            if user == self.username:
                print("* " + user + " (You)")
            else:
                print("* " + user)
        print("")

    def loginMenu(self):

        print("Username :")
        self.username = input("> ")
        # check if user exists by getting its IP from server
        get_ip_response = requests.get(self.server_url + '/users/' + self.username + '/ip')

        # New username : Account creation
        if get_ip_response.status_code == 404:
            print("New user detected.\n")
            print(f"Welcome {self.username} !\n"
                  f"Create your account by entering a new password\n"
                  f"(at least 8 characters, 1 uppercase, 1 digit and 1 special character)")

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

        # Known usename : sign in
        else:
            print(f"Welcome back {self.username} !\n"
                  f"Password :")
            self.password = input("> ")
            data = {'username': self.username, 'password': self.password}
            response = requests.post(self.server_url + '/sessions', json=data)
            while response.status_code != 200:
                print("Bad credentials, please try again :")
                self.username = input("Your username : ")
                self.password = input("Your password : ")
                data = {'username': self.username, 'password': self.password}
                response = requests.post(self.server_url + '/sessions', json=data)

            get_ip_data = get_ip_response.json()
            if get_ip_data['port'] != self.port:
                requests.put(self.server_url + '/users/' + self.username + '/ip',
                            json={'password': self.password, 'port': self.port})

            print("Logged in successfully !")

    def sessionsMenu(self):

        print("")
        self.displaySessions()
        print("Who do you want to talk with ?")
        dest = input("> ")

        response = requests.get(self.server_url + '/sessions/' + dest)
        while response.status_code != 200:
            print(f"Sorry, {dest} is not connected right now")
            self.displaySessions()
            print("Who do you want to talk with ?")
            dest = input("> ")
            response = requests.get(self.server_url + '/sessions/' + dest)

        response = requests.get(self.server_url + '/users/' + dest + '/ip')
        data = response.json()
        self.dest_address = f"http://{data['ip']}:{data['port']}"
        self.connected = True

        print(f"\nStarting chat with {dest} !\n")

    def messageServer(self):
        app = Flask(__name__)

        import logging  # pylint: disable=import-outside-toplevel
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

        @app.route('/msg', methods=['POST'])
        def on_msg():
            data = json.loads(request.data.decode('utf-8'))
            if 'username' not in data or 'msg' not in data:
                return "", 400

            if data['msg'] == "/exit":
                print(f"{data['username']} left the chat.")
            else:
                print(f"\r{data['username']} > {data['msg']}\n>", end=" ")

            return "", 200

        app.run(port=self.port)

    def chatLoop(self):
        # wait for their input
        while True:
            msg = input("\r> ")

            if msg == "/exit":
                self.exitChat()
                os._exit(1)
            elif msg == "/list":
                self.displaySessions()
            else:
                requests.post(self.dest_address + '/msg', json={'username': self.username, 'msg': msg})

    def signal_handler(self, signal, frame):
        print("\nUser exit programm with Crtl+c")
        if self.connected:
            self.exitChat()
        os._exit(1)

    def exitChat(self, msg="/exit"):
        requests.delete(self.server_url + "/sessions/" + self.username, json={'password': self.password})
        requests.post(self.dest_address + '/msg', json={'username': self.username, 'msg': msg})
        self.msgServProc.kill()

    def run(self):

        # Signal to catch Crtl+C from client
        sig.signal(sig.SIGINT, self.signal_handler)
        signal_thread = threading.Event()

        self.checkServer()
        self.displayBanner()
        self.loginMenu()

        # Run message server
        self.msgServProc = Process(target=self.messageServer)
        self.msgServProc.start()
        time.sleep(1)

        self.sessionsMenu()
        self.chatLoop()
