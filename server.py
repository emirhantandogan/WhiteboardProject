import socket
import threading

# Sunucu Ayarları
HOST = '0.0.0.0'  # Her yerden bağlantı kabul eder
PORT = 12345

lobbies = {}  # {lobi_ismi: [client_socket1, client_socket2, ...]}


def handle_client(client_socket, client_address):
    global lobbies
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            command, data = message.split(':', 1)

            if command == "CREATE":
                lobby_name = data.strip()
                if lobby_name not in lobbies:
                    lobbies[lobby_name] = [client_socket]
                    client_socket.send("LOBBY_CREATED".encode())
                else:
                    client_socket.send("ERROR: Lobby already exists!".encode())

            elif command == "LIST":
                lobby_list = ','.join(lobbies.keys())
                client_socket.send(f"LOBBIES:{lobby_list}".encode())

            elif command == "JOIN":
                lobby_name = data.strip()
                if lobby_name in lobbies:
                    lobbies[lobby_name].append(client_socket)
                    client_socket.send("JOINED_LOBBY".encode())
                else:
                    client_socket.send("ERROR: Lobby not found!".encode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Bağlantıyı temizle
        for lobby_name, clients in lobbies.items():
            if client_socket in clients:
                clients.remove(client_socket)
                if not clients:  # Eğer lobide kimse kalmazsa sil
                    del lobbies[lobby_name]
                break
        client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server started on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection: {client_address}")
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()


if __name__ == "__main__":
    main()
