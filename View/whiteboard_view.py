from tkinter import Toplevel, Frame, Label, Listbox, END, Canvas
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

    def update_user_list(self, users):
        """Kullanıcı listesini günceller."""
        self.user_listbox.delete(0, END)
        for user in users:
            self.user_listbox.insert(END, user)
