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

        self.lock = threading.Lock()

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
            with self.lock:
                try:
                    self.client_socket.settimeout(0.1)
                    try:
                        message = self.client_socket.recv(1024).decode()
                        if not message:
                            return
                        if message.startswith("USERS:"):
                            users = message.split(":", 1)[1].split(",")
                            callback(users)
                    except socket.timeout:
                        pass
                except Exception as e:
                    print(f"Error receiving updates: {e}")
                finally:
                    self.client_socket.settimeout(None)

            threading.Timer(5, listen).start()

        listen()

    def listen_for_draw_updates(self, callback):
        buffer = ""  # Tampon, eksik kalan verileri saklamak için

        def listen():
            nonlocal buffer  # Tamponu fonksiyonlar arasında paylaşmak için

            with self.lock:
                try:
                    self.client_socket.settimeout(5)
                    try:
                        # Yeni veriyi oku ve tampona ekle
                        data = self.client_socket.recv(1024).decode()
                        if not data:
                            return
                        buffer += data  # Gelen veriyi tampona ekle

                        # Eğer "DRAW_DATA:" öncesinde eksik \n varsa tamamla
                        while "DRAW_DATA:" in buffer:
                            # İlk "DRAW_DATA:" mesajını bul
                            start = buffer.find("DRAW_DATA:")
                            if start > 0 and buffer[start - 1] != "\n":
                                # Eğer "DRAW_DATA:" öncesinde \n yoksa ekle
                                buffer = buffer[:start] + "\n" + buffer[start:]

                            # İlk tam mesajı al ve tamponu güncelle
                            if "\n" in buffer:
                                message, buffer = buffer.split("\n", 1)
                            else:
                                # Eğer sonlandırıcı yoksa döngüyü kır ve bekle
                                break

                            if message.startswith("DRAW_DATA:"):
                                try:
                                    # DRAW_DATA'yı parse et ve (x, y) tuple'larına dönüştür
                                    raw_data = message.split(":", 1)[1].split(";")
                                    draw_data = [tuple(map(int, point.split(","))) for point in raw_data if point]
                                    callback(draw_data)
                                except ValueError:
                                    print(f"Invalid data format in message: {message}")
                    except socket.timeout:
                        pass
                except Exception as e:
                    print(f"Error receiving draw updates: {e}")
                finally:
                    self.client_socket.settimeout(None)

            # 5 saniye sonra tekrar çağır
            threading.Timer(5, listen).start()

        listen()

    def send_ping(self):
        self.clear_socket_buffer(self.client_socket)
        print("sent ping")
        response = self.send_message("PING")
        print("Server response:", response)

    def send_draw_data(self, lobby_name, draw_data):
        with self.lock:
            serialized_data = ";".join(f"{x},{y}" for x, y in draw_data)
            message = f"SEND_DRAW:{lobby_name}|{serialized_data}"
            self.send_message(message)

    def clear_socket_buffer(self, sock):
        """Tampon bellekte kalan verileri temizler."""
        sock.setblocking(False)
        try:
            while sock.recv(1024):
                pass
        except BlockingIOError:
            pass
        finally:
            sock.setblocking(True)





