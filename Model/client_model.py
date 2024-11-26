import socket
from hashlib import sha256
import threading
import time

def encrypt_password(password):
    return sha256(password.encode()).hexdigest()

class ClientModel:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_host, self.server_port))

    def send_message(self, message):
        self.client_socket.send(message.encode())
        return self.client_socket.recv(1024).decode()

    def create_lobby(self, lobby_name, password=None):
        if password:
            return self.send_message(f"CREATE:{lobby_name}|{encrypt_password(password)}")
        return self.send_message(f"CREATE:{lobby_name}")

    def join_lobby(self, lobby_name, username):
        return self.send_message(f"JOIN:{lobby_name}|{username}")

    def join_lobby_with_password(self, lobby_name, password, username):
        encrypted_password = encrypt_password(password)
        return self.send_message(f"JOIN_WITH_PASSWORD:{lobby_name}|{encrypted_password}|{username}")

    def list_lobbies(self):
        response = self.send_message("LIST:")
        if response.startswith("LOBBIES:"):
            return response.split(":", 1)[1].split(",")
        return []

    def get_users_in_lobby(self, lobby_name):
        response = self.send_message(f"GET_USERS:{lobby_name}")
        if response.startswith("USERS:"):
            return response.split(":", 1)[1].split(",")
        return []

    def listen_for_user_updates(self, callback):
        def listen():
            while True:
                try:
                    message = self.client_socket.recv(1024).decode()
                    if message.startswith("USERS:"):
                        users = message.split(":", 1)[1].split(",")
                        callback(users)
                except Exception as e:
                    print(f"Error receiving updates: {e}")
                    break

        threading.Thread(target=listen, daemon=True).start()








