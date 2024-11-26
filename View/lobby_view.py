from tkinter import Tk, Label, Button, Entry, Frame, Canvas, Scrollbar, VERTICAL, HORIZONTAL
from View.gui_helper import GUIHelper

class LobbyView:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Whiteboard")

        # Ana pencerenin büyütülebilir olmasını sağla
        self.root.rowconfigure(0, weight=1)  # Ana satır büyüyebilir
        self.root.columnconfigure(0, weight=1)  # Sol sütun büyüyebilir
        self.root.columnconfigure(1, weight=8)  # Sağ sütun büyüyebilir

        # Sol alan: Lobi oluşturma ve butonlar
        left_frame = Frame(self.root, bg="white")
        left_frame.grid(row=0, column=0, sticky="nsew")  # Sol sütun
        left_frame.columnconfigure(0, weight=1)

        # Sağ alan: Lobi listesi
        right_frame = Frame(self.root, bg="#007BFF")
        right_frame.grid(row=0, column=1, sticky="nsew")  # Sağ sütun
        right_frame.rowconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=50)
        right_frame.columnconfigure(0, weight=1)

        # --- Sol Taraf: Lobi oluşturma ve butonlar ---
        GUIHelper.create_label(left_frame, "Online Whiteboard", "white", "#007BFF").grid(row=0, column=0, padx=10, pady=5, sticky="nw")

        self.username_entry = GUIHelper.create_entry(left_frame, "Enter a username.")
        self.username_entry.grid(row=1, column=0, padx=10, pady=5, sticky="new")

        self.lobby_name_entry = GUIHelper.create_entry(left_frame, "Enter a lobby name to create.")
        self.lobby_name_entry.grid(row=2, column=0, padx=10, pady=5, sticky="new")

        # Şifre giriş alanı
        self.password_entry = GUIHelper.create_entry(left_frame, "Enter a password (optional)")
        self.password_entry.grid(row=3, column=0, padx=10, pady=5, sticky="new")

        self.create_button = GUIHelper.create_button(left_frame, "Create Lobby")
        self.create_button.grid(row=4, column=0, padx=10, pady=5, sticky="new")

        self.refresh_button = GUIHelper.create_button(left_frame, "Refresh Lobbies")
        self.refresh_button.grid(row=5, column=0, padx=10, pady=5, sticky="new")

        self.output_label = GUIHelper.create_label(left_frame, "", "#007BFF")
        self.output_label.grid(row=6, column=0, padx=10, pady=5, sticky="new")

        # --- Sağ Taraf: Lobi Listesi ---
        GUIHelper.create_label(right_frame, "Available Lobbies:", "#007BFF", "white").grid(row=0, column=0, padx=10, pady=5, sticky="nw")
        # Lobi listesi için kaydırılabilir bir alan oluştur
        self.canvas = Canvas(right_frame, bg="white")
        self.scrollbar = Scrollbar(right_frame, orient=VERTICAL, command=self.canvas.yview)
        self.lobby_frame = Frame(self.canvas, bg="white")

        self.lobby_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.lobby_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=1, column=0, sticky="nsew", padx=(10, 0), pady=5)
        self.scrollbar.grid(row=1, column=1, sticky="ns", padx=(0, 10), pady=5)

    def update_lobby_list(self, lobbies, join_callback):
        # Mevcut lobileri temizle
        for widget in self.lobby_frame.winfo_children():
            widget.destroy()

        # Her lobi için bir satır oluştur
        for lobby in lobbies:
            row_frame = Frame(self.lobby_frame, bg="white", pady=2)
            row_frame.pack(fill="x", expand=True)

            # Lobi ismi (Sola dayalı)
            Label(row_frame, text=lobby, bg="white", font=("Arial", 14), anchor="w").grid(
                row=0, column=0, sticky="w", padx=5, pady=2
            )

            # Join butonu (Sağa dayalı)
            Button(row_frame, text="Join", bg="#007BFF", fg="white", command=lambda l=lobby: join_callback(l)).grid(
                row=0, column=1, sticky="e", padx=5, pady=2
            )

            # Satır çerçevesinin sütunlarını büyütmek için yapılandır
            row_frame.grid_columnconfigure(0, weight=1)  # Lobi ismi genişler
            row_frame.grid_columnconfigure(1, weight=1)  # Buton sabit kalır

    def set_output_message(self, message):
        self.output_label.config(text=message)

    def get_lobby_password(self):
        return self.password_entry.get_actual_value()

    def get_username(self):
        return self.username_entry.get_actual_value()

