import socket


def connect_to_server():
    host = input("Enter the IP address of the server: ")
    port = int(input("Enter the port number of the server: "))

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print(f"Connected to server at ({host}, {port})")
    return client_socket


def display_menu():
    print("\n===========================================================================================")
    print("_________________________ Welcome to our Store_______________________________________________")
    print("1. Login")
    print("2. Exit")
    print("===========================================================================================\n")


def display_guest_menu():
    print("\n===========================================================================================")
    print("__________________________Logged In as GUEST_________________________________________________")
    print("1. To PUT KEY")
    print("2. To GET KEY")
    print("3. To UPGRADE TO MANAGER")
    print("4. Exit")
    print("===========================================================================================\n")


def display_manager_menu():
    print("\n===========================================================================================")
    print("__________________________Logged In as MANAGER_______________________________________________")
    print("1. To PUT KEY")
    print("2. To GET KEY")
    print("3. To View all active users")
    print("4. To MANAGER PUT KEY")
    print("5. To MANAGER GET KEY")
    print("6. Exit")
    print("===========================================================================================\n")



def login(client_socket):
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    command = f"signup {username} {password}"
    client_socket.send(command.encode("utf-8"))

    response = client_socket.recv(1024).decode("utf-8")
    print(response)

    proceed = False
    if response.startswith("\nSignup successful"):
        proceed = True

    return username, proceed


def logout(client_socket, username_entered, username=""):
    if username_entered:
        command = f"logout {username}"
    else:
        command = "logout"
    client_socket.send(command.encode("utf-8"))


def put(client_socket):
    key = input("Enter the key: ")
    value = input("Enter the value: ")

    command = f"put {key} {value}"
    client_socket.send(command.encode("utf-8"))

    response = client_socket.recv(1024).decode("utf-8")
    print(response)


def get(client_socket):
    key = input("Enter the key: ")

    command = f"get {key}"
    client_socket.send(command.encode("utf-8"))

    response = client_socket.recv(1024).decode("utf-8")
    print(response)


def upgrade(client_socket):
    upgrade_password = input("Enter the upgrade password: ")

    command = f"upgrade {upgrade_password}"
    client_socket.send(command.encode("utf-8"))

    response = client_socket.recv(1024).decode("utf-8")
    print(response)

    proceed_upgrade = False
    if response.startswith("\nUpgrade successful"):
        proceed_upgrade = True

    return proceed_upgrade


def superput(client_socket, username):
    while True:
        target_user = input("Enter the username of the target user: ")

        if target_user.lower() == username.lower():
            print("You cannot perform SUPERPUT on yourself. Please use PUT operation.")
        else:
            break

    key = input("Enter the key: ")
    value = input("Enter the value: ")

    command = f"superput {target_user} {key} {value}"
    client_socket.send(command.encode("utf-8"))

    response = client_socket.recv(1024).decode("utf-8")
    print(response)


def superget(client_socket, username):
    while True:
        target_user = input("Enter the username of the user: ")

        if target_user.lower() == username.lower():
            print("You cannot perform SUPERGET on yourself. Please use GET operation.")
        else:
            break

    key = input("Enter the key: ")

    command = f"superget {target_user} {key}"
    client_socket.send(command.encode("utf-8"))

    response = client_socket.recv(1024).decode("utf-8")
    print(response)


def view_all_users(client_socket):
    command = "view_all_users"
    client_socket.send(command.encode("utf-8"))

    response = client_socket.recv(1024).decode("utf-8")
    print(response)


def main():
    client_socket = connect_to_server()
    username_entered = False

    try:
        while True:
            display_menu()
            choice = input("Enter your choice: ")

            
            if choice == "1":
                username, proceed = login(client_socket)
                username_entered = proceed
                if proceed:
                    whole_exit = False
                    while True:
                        if whole_exit:
                            break
                        display_guest_menu()
                        choice_guest = input("Enter your choice: ")

                        if choice_guest == "1":
                            put(client_socket)
                        elif choice_guest == "2":
                            get(client_socket)
                        elif choice_guest == "3":
                            proceed_upgrade = upgrade(client_socket)
                            if proceed_upgrade:
                                while True:
                                    display_manager_menu()
                                    choice_manager = input("Enter your choice: ")

                                    if choice_manager == "1":
                                        put(client_socket)
                                    elif choice_manager == "2":
                                        get(client_socket)
                                    elif choice_manager == "3":
                                        view_all_users(client_socket)
                                    elif choice_manager == "4":
                                        superput(client_socket, username)
                                    elif choice_manager == "5":
                                        superget(client_socket, username)
                                    elif choice_manager == "6":
                                        logout(
                                            client_socket, username_entered, username
                                        )
                                        whole_exit = True
                                        break
                                    else:
                                        print("Invalid choice.")
                        elif choice_guest == "4":
                            logout(client_socket, username_entered, username)
                            break
                        else:
                            print("Invalid choice.")
                    break
            elif choice == "2":
                logout(client_socket, username_entered)
                break
            else:
                print("Invalid choice.")
    except KeyboardInterrupt:
        print("\nClient program terminated.")
    finally:
        
        client_socket.close()


if __name__ == "__main__":
    main()
