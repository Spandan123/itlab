import socket
import threading


class KeyValueStore:
    def __init__(self):
        self.users = {}
        self.clients = {}  # to store client information and data
        self.client_data = {}  # in-memory client data

    def handle_client(self, client_socket, client_address):
        while True:
            command = client_socket.recv(1024).decode("utf-8")
            if not command:
                break

            if command.startswith("signup"):
                _, username, password = command.split()
                self.handle_signup(client_socket, client_address, username, password)
            elif command == "logout":
                self.handle_logout(client_socket)
                break
            elif command.startswith("logout"):
                _, username = command.split()
                self.handle_logout(client_socket, username)
                break
            elif command.startswith("put"):
                _, key, value = command.split()
                self.handle_put(client_socket, key, value)
            elif command.startswith("get"):
                _, key = command.split()
                self.handle_get(client_socket, key)
            elif command.startswith("upgrade"):
                _, password = command.split()
                self.handle_upgrade(client_socket, password)
            elif command.startswith("superput"):
                _, target_user, key, value = command.split()
                self.handle_superput(client_socket, target_user, key, value)
            elif command.startswith("superget"):
                _, target_user, key = command.split()
                self.handle_superget(client_socket, target_user, key)
            elif command.startswith("view_all_users"):
                self.handle_view_all_users(client_socket)


    def handle_signup(self, client_socket, client_address, username, password):
        if username in self.users:
            client_socket.send(
                "\nUsername already exists. Please login.".encode("utf-8")
            )
        else:
            self.users[username] = {"password": password}
            self.clients[username] = {
                "socket": client_socket,
                "address": client_address,
                "role": "guest",
            }
            client_socket.send(
                "\nSignup successful. You are now logged in as GUEST.".encode("utf-8")
            )
            print(f"{username} signed up and logged in as GUEST.")

    def handle_logout(self, client_socket, username=""):
        try:
            if username in self.clients:
                role = self.clients[username].get("role")
                print(f"User {username} logged out as {role.upper()}.")
                self.users.pop(username)
                self.clients.pop(username)
                self.client_data.pop(username)
            client_socket.close()
        except:
            print()

    def handle_put(self, client_socket, key, value):
        username = self.get_username_by_socket(client_socket)
        if username in self.client_data:
            self.client_data[username][key] = value
        else:
            self.client_data[username] = {}
            self.client_data[username][key] = value
        client_socket.send(f'\nKey "{key}" set to "{value}".'.encode("utf-8"))
        print(f"{username} performed PUT operation.")

    def handle_get(self, client_socket, key):
        username = self.get_username_by_socket(client_socket)
        if username in self.client_data and key in self.client_data[username]:
            client_socket.send(
                f'\nValue for the key "{key}": {self.client_data[username][key]}.'.encode(
                    "utf-8"
                )
            )
        else:
            client_socket.send(
                f'\nValue for the key "{key}" doesn\'t exist.'.encode("utf-8")
            )
        print(f"{username} performed GET operation.")

    def handle_upgrade(self, client_socket, password):
        username = self.get_username_by_socket(client_socket)
        if password == "Kfc_KingKohli":
            self.clients[username]["role"] = "manager"
            client_socket.send(
                "\nUpgrade successful! You are now a MANAGER.".encode("utf-8")
            )
            print(f"{username} upgraded to MANAGER.")
        else:
            client_socket.send(
                "\nIncorrect upgrade password. Please try again.".encode("utf-8")
            )

    def handle_superput(self, client_socket, target_user, key, value):
        username = self.get_username_by_socket(client_socket)
        if target_user in self.client_data:
            self.client_data[target_user][key] = value
            client_socket.send(
                f'\nKey "{key}" set to "{value}" for user "{target_user}".'.encode(
                    "utf-8"
                )
            )
            print(f"User {username} performed PUT operation on {target_user}.")
        elif target_user not in self.users:
            client_socket.send(
                f'\nInvalid target user "{target_user}".'.encode("utf-8")
            )
        else:
            self.client_data[target_user] = {}
            self.client_data[target_user][key] = value
            client_socket.send(
                f'\nKey "{key}" set to "{value}" for user "{target_user}".'.encode(
                    "utf-8"
                )
            )
            print(f"(MANAGER) {username} performed PUT operation on {target_user}.")

    def handle_superget(self, client_socket, target_user, key):
        username = self.get_username_by_socket(client_socket)
        if target_user in self.client_data and key in self.client_data[target_user]:
            client_socket.send(
                f'\nValue for the key "{key}" for user "{target_user}": {self.client_data[target_user][key]}'.encode(
                    "utf-8"
                )
            )
            print(f"(MANAGER) {username} performed GET operation on {target_user}.")
        elif target_user not in self.users:
            client_socket.send(f'\nInvalid target user "{target_user}"'.encode("utf-8"))
        else:
            client_socket.send(
                f'\nValue for the key "{key}" for user "{target_user}" doesn\'t exist'.encode(
                    "utf-8"
                )
            )
            print(f"(MANAGER) {username} performed GET operation on {target_user}.")

    def handle_view_all_users(self, client_socket):
        username = self.get_username_by_socket(client_socket)
        usernames = list(self.users.keys())
        if usernames:
            user_list = "\n".join(
                [f"{i + 1}. {username}" for i, username in enumerate(usernames)]
            )
            response = f"\nThe users registered in the server are:\n{user_list}"
        else:
            response = "\nNo users registered in the server."

        client_socket.send(response.encode("utf-8"))
        print(f"(MANAGER) {username} viewed all users registered in the server.")

    def get_username_by_socket(self, client_socket):
        for username, client_info in self.clients.items():
            if client_info["socket"] == client_socket:
                return username

    def start_server(self, host):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, 0))  # Use 0 to let the OS choose an available port
        server_port = server_socket.getsockname()[1]  # Get the chosen port
        server_socket.listen(5)

        print(f"\nServer listening on {host} : {server_port}...\n")

        try:
            while True:
                client_socket, client_address = server_socket.accept()
                client_handler = threading.Thread(
                    target=self.handle_client, args=(client_socket, client_address)
                )
                client_handler.start()
        except KeyboardInterrupt:
            print("\nServer shutting down.")
        finally:
            server_socket.close()


if __name__ == "__main__":
    host = input("Enter the IP address of the network: ")

    kv_store = KeyValueStore()
    kv_store.start_server(host)