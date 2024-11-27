from tkinter import Toplevel, Frame, Label, Listbox, END, Canvas, Button
from View.gui_helper import GUIHelper

import threading
import time

class WhiteboardView:
    def __init__(self, parent, lobby_name, users, controller):
        self.controller = controller
        self.lobby_name = lobby_name

        self.draw_data = []  # Çizim verilerini tutan liste

        # Ana pencere yerine yeni bir Toplevel penceresi oluştur
        self.root = Toplevel(parent)
        self.root.title("Whiteboard")
        self.root.geometry("800x600")

        # Ana pencerenin boyutlandırılmasını sağla
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=12)

        # Sol taraf: Lobi adı ve kullanıcı listesi
        left_frame = Frame(self.root, bg="#007BFF")
        left_frame.grid(row=0, column=0, sticky="nsew")
        left_frame.rowconfigure(1, weight=1)
        left_frame.columnconfigure(0, weight=1)

        # Sağ taraf: Whiteboard alanı (Boş bırakılabilir, genişletilebilir)
        right_frame = Frame(self.root, bg="#F0F0F0")
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)

        # Sağ taraf: Çizim yapılabilir bir Canvas alanı
        self.canvas = Canvas(right_frame, bg="white", cursor="cross")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<B1-Motion>", self.draw_on_canvas)

        # Lobi adı
        Label(left_frame, text=f"Lobby: {lobby_name}", bg="white", font=("Arial", 16)).grid(
            row=0, column=0, padx=10, pady=10, sticky="new"
        )

        # Kullanıcı listesi
        Label(left_frame, text="Users in Lobby:", bg="white", font=("Arial", 12)).grid(
            row=1, column=0, padx=10, pady=5, sticky="new"
        )
        self.user_listbox = Listbox(left_frame)
        self.user_listbox.grid(row=2, column=0, padx=10, pady=5, sticky="new")

        # Kullanıcı listesini doldur
        self.update_user_list(users)

        # "Send Draw Data" butonu
        send_button = Button(right_frame, text="Send Draw Data", command=self.send_draw_data)
        send_button.grid(row=1, column=0, padx=10, pady=10, sticky="new")

        self.send_draw_data_periodically()

    def update_user_list(self, users):
        """Kullanıcı listesini günceller."""
        self.user_listbox.delete(0, END)
        for user in users:
            self.user_listbox.insert(END, user)

    def draw_on_canvas(self, event):
        """Canvas üzerinde çizim yapılmasını sağlar."""
        x, y = event.x, event.y
        r = 2
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="black", outline="black")
        self.draw_data.append((x, y))

    def send_draw_data(self):
        self.controller.send_draw_data(self.lobby_name, self.draw_data)
        self.draw_data = []

    def send_draw_data_periodically(self):
        if len(self.draw_data) > 5:
            self.send_draw_data()

        self.root.after(500, self.send_draw_data_periodically)

    def get_draw_data(self, list):
        return list

    def draw_data_getted_from_server(self, list):
        print("drawing this:", list)
        #get_draw_data metodu yerine listeyi aldığında bu listedeki koordinatlara göre canvasa çizimi gerçekleştiren bir metod yaz.
        for x, y in list:
            self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black", outline="black")

