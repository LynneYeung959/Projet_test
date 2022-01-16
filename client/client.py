import requests


if __name__ == '__main__':
    print("Please enter server address : ")
    server_address = input("> ")

    print("Please enter server port : ")
    server_port = input("> ")

    server_url = f"http://{server_address}:{server_port}"

    print("Your username (at least 3 characters, only letters or digits) : ")
    username = input("> ")

    # check if user exists by getting its IP from server
    response = requests.get(server_url + '/users/' + username + '/ip')

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
              f"Please enter your password to log in")
        password = input("> ")
