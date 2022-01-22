import argparse
import sys

import requests


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Launch client connected at specified address and port')
    parser.add_argument('--addr', default='localhost', type=str, help='specify server address (default : localhost)')
    parser.add_argument('--port', default=80, type=int, help='specify server port (default : 80)')
    args = parser.parse_args()

    server_url = f"http://{args.addr}:{args.port}"

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
        while response.status_code == 400:
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
        while response.status_code == 400:
            print("Bad credentials, please try again :")
            username = input("Your username : ")
            password = input("Your password : ")
            data = {'username': username, 'password': password}
            response = requests.post(server_url + '/sessions', json=data)

        print("Logged in successfully !")

    # user logged in
    ...
