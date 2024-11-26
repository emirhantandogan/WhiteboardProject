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

        # Çizim işlevlerini bağlama
        self.canvas.bind("<B1-Motion>", self.draw)

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

        # Sunucuya düzenli aralıklarla çizim verilerini gönderen bir thread başlat
        self.start_draw_update_thread()

        self.refresh_button = GUIHelper.create_button(left_frame, "Refresh Lobbies")
        self.refresh_button.grid(row=5, column=0, padx=10, pady=5, sticky="new")
        self.refresh_button.config(command=self.call_data)

    def update_user_list(self, users):
        """Kullanıcı listesini günceller."""
        self.user_listbox.delete(0, END)
        for user in users:
            self.user_listbox.insert(END, user)

    def draw(self, event):
        """Canvas üzerine çizim yapar ve koordinatları listeye ekler."""
        x, y = event.x, event.y
        self.canvas.create_oval(x, y, x + 2, y + 2, fill="black", outline="black")
        self.draw_data.append((x, y))  # Koordinatları listeye ekle

    def start_draw_update_thread(self):
        """Sunucuya düzenli olarak çizim verilerini göndermek için bir thread çalıştırır."""
        def update_server():
            while True:
                if self.draw_data:
                    # Sunucuya çizim verilerini gönder
                    self.controller.model.send_draw_data_batch(self.lobby_name, self.draw_data)
                    self.draw_data.clear()  # Listeyi temizle
                time.sleep(5)  # 5 saniyede bir gönderim yap

        threading.Thread(target=update_server, daemon=True).start()

    def update_canvas(self, draw_data):
        """Sunucudan gelen çizim verilerini Canvas'a çizer."""
        for x, y in draw_data:
            self.canvas.create_oval(x, y, x + 2, y + 2, fill="black", outline="black")


    def call_data(self):
        self.controller.model.call_data(self.lobby_name, self.update_canvas)
