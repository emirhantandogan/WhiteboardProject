import socket
import threading
from tkinter import Tk, Label, Button, Entry, Listbox, END

# İstemci Ayarları
SERVER_HOST = '127.0.0.1'  # Yerel sunucu için
SERVER_PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

def send_message(message):
    client_socket.send(message.encode())
    return client_socket.recv(1024).decode()

def create_lobby():
    lobby_name = lobby_name_entry.get()
    response = send_message(f"CREATE:{lobby_name}")
    output_label.config(text=response)

def refresh_lobbies():
    response = send_message("LIST:")
    if response.startswith("LOBBIES:"):
        lobbies = response.split(":", 1)[1].split(",")
        lobby_listbox.delete(0, END)  # Listeyi temizle
        for lobby in lobbies:
            lobby_listbox.insert(END, lobby)

def join_lobby():
    selected_lobby = lobby_listbox.get(lobby_listbox.curselection())
    response = send_message(f"JOIN:{selected_lobby}")
    output_label.config(text=response)

# GUI Oluşturma
root = Tk()
root.title("Online Whiteboard")

Label(root, text="Lobi İsmi:").pack()
lobby_name_entry = Entry(root)
lobby_name_entry.pack()

Button(root, text="Lobi Oluştur", command=create_lobby).pack()

Label(root, text="Mevcut Lobiler:").pack()
lobby_listbox = Listbox(root, height=10, width=50)
lobby_listbox.pack()

Button(root, text="Lobileri Yenile", command=refresh_lobbies).pack()
Button(root, text="Seçili Lobiye Katıl", command=join_lobby).pack()

output_label = Label(root, text="", fg="blue")
output_label.pack()

root.mainloop()
