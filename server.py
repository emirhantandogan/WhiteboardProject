import socket
import threading

# Sunucu Ayarları
HOST = '0.0.0.0'  # Her yerden bağlantı kabul eder
PORT = 12345

import hashlib

def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

lobbies = {}  # {lobi_ismi: {"password": şifre, "clients": {client_socket: "username"}}}

lobbies_draw_data = {}

def handle_client(client_socket, client_address):
    global lobbies
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            if len(message) > 1024:
                print("Message too large, ignoring...")
                return

            command, data = message.split(':', 1)

            if command == "CREATE":
                lobby_name, *password = data.strip().split('|')
                if lobby_name not in lobbies:
                    lobbies[lobby_name] = {
                        "password": password[0] if password else None,
                        "clients": {},  # Sözlük olarak başlatılıyor
                    }
                    client_socket.send("LOBBY_CREATED".encode())
                else:
                    client_socket.send("ERROR: Lobby already exists!".encode())

            elif command == "LIST":
                lobby_list = ','.join(lobbies.keys())
                client_socket.send(f"LOBBIES:{lobby_list}".encode())

            elif command == "JOIN":
                lobby_name, username = data.strip().split('|')
                if lobby_name in lobbies and not lobbies[lobby_name]["password"]:
                    lobbies[lobby_name]["clients"][client_socket] = username
                    client_socket.send("JOINED_LOBBY".encode())

                    # Güncellenmiş kullanıcı listesini yayınla
                    users = list(lobbies[lobby_name]["clients"].values())
                    broadcast_to_lobby(lobby_name, f"USERS:{','.join(users)}")
                else:
                    client_socket.send("PASSWORD_REQUIRED".encode())

            elif command == "JOIN_WITH_PASSWORD":
                lobby_name, password, username = data.strip().split('|')
                print(lobbies[lobby_name]["password"])
                print(password)
                if lobby_name in lobbies and lobbies[lobby_name]["password"] == password:
                    lobbies[lobby_name]["clients"][client_socket] = username
                    client_socket.send("JOINED_LOBBY".encode())

                    # Güncellenmiş kullanıcı listesini yayınla
                    users = list(lobbies[lobby_name]["clients"].values())
                    broadcast_to_lobby(lobby_name, f"USERS:{','.join(users)}")
                else:
                    client_socket.send("ERROR: Incorrect password!".encode())

            elif command == "GET_USERS":
                lobby_name = data.strip()
                if lobby_name in lobbies:
                    users = list(lobbies[lobby_name]["clients"].values())  # Kullanıcı adlarını al
                    client_socket.send(f"USERS:{','.join(users)}".encode())
                else:
                    client_socket.send("ERROR: Lobby not found!".encode())


    except ConnectionResetError:
        print(f"Connection reset by client: {client_address}")
    except socket.timeout:
        print("Client connection timed out.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        for lobby_name, lobby_data in lobbies.items():
            if client_socket in lobby_data["clients"]:
                del lobby_data["clients"][client_socket]
                if not lobby_data["clients"]:
                    del lobbies[lobby_name]
                else:
                    # Güncellenmiş kullanıcı listesini yayınla
                    users = list(lobby_data["clients"].values())
                    broadcast_to_lobby(lobby_name, f"USERS:{','.join(users)}")
                break
        print(f"Closing connection for client: {client_address}")
        client_socket.close()

def broadcast_to_lobby(lobby_name, message):
    """Belirtilen lobiye bağlı tüm istemcilere mesaj gönder."""
    if lobby_name in lobbies:
        for client_socket in lobbies[lobby_name]["clients"].keys():
            try:
                client_socket.send(message.encode())
            except Exception as e:
                print(f"Error broadcasting to client: {e}")

# UDP Sunucu İşleme
def handle_udp():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((HOST, UDP_PORT))
    print(f"UDP Server started on {HOST}:{UDP_PORT}")

    while True:
        try:
            data, addr = udp_socket.recvfrom(4096)
            if addr not in udp_clients:
                udp_clients.append(addr)

            # Gelen veriyi çözümle ve aynı lobiye bağlı tüm istemcilere gönder
            serialized_data = data.decode()
            for client in udp_clients:
                if client != addr:  # Gönderen hariç
                    udp_socket.sendto(serialized_data.encode(), client)
        except Exception as e:
            print(f"Error in UDP server: {e}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(20)
    print(f"Server started on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection: {client_address}")
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()


if __name__ == "__main__":
    main()
