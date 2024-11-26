from Model.client_model import ClientModel
from View.lobby_view import LobbyView
from View.whiteboard_view import WhiteboardView
from tkinter import Toplevel, Label, Entry, Button

class ClientController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.create_button.config(command=self.create_lobby)
        self.view.refresh_button.config(command=self.refresh_lobbies)

    def create_lobby(self):
        lobby_name = self.view.lobby_name_entry.get()
        password = self.view.get_lobby_password()
        if lobby_name:
            response = self.model.create_lobby(lobby_name, password)
            self.view.set_output_message(response)
        if password is None:
            self.join_lobby(lobby_name)
        else:
            self.join_lobby_with_password(lobby_name, password)

    def refresh_lobbies(self):
        """Lobi listesini yeniler."""
        lobbies = self.model.list_lobbies()
        self.view.update_lobby_list(lobbies, self.join_lobby)

    def join_lobby(self, lobby_name):
        username = self.view.get_username()
        response = self.model.join_lobby(lobby_name, username)
        if response == "PASSWORD_REQUIRED":
            self.show_password_prompt(lobby_name, username)
        else:
            users = self.model.get_users_in_lobby(lobby_name)
            self.open_whiteboard_view(lobby_name, users)

    def join_lobby_with_password(self, lobby_name, password):
        '''
        This method for joining to lobby instantly after creating that lobby
        '''
        username = self.view.get_username()
        response = self.model.join_lobby_with_password(lobby_name, password, username)
        self.view.set_output_message(response)
        if response == "JOINED_LOBBY":
            users = self.model.get_users_in_lobby(lobby_name)
            self.open_whiteboard_view(lobby_name, users)


    def show_password_prompt(self, lobby_name, username):
        password_window = Toplevel(self.view.root)
        password_window.title("Enter Password")

        Label(password_window, text="Password:").grid(row=0, column=0, padx=10, pady=10)
        password_entry = Entry(password_window, show="*")
        password_entry.grid(row=0, column=1, padx=10, pady=10)

        def submit_password():
            password = password_entry.get()
            response = self.model.join_lobby_with_password(lobby_name, password, username)
            self.view.set_output_message(response)
            if response == "JOINED_LOBBY":
                users = self.model.get_users_in_lobby(lobby_name)
                self.view.set_output_message(response)
                self.open_whiteboard_view(lobby_name, users)
            password_window.destroy()

        Button(password_window, text="Submit", command=submit_password).grid(row=1, column=0, columnspan=2, pady=10)

    def open_whiteboard_view(self, lobby_name, users):
        """Whiteboard View'ı aç ve çizim güncellemelerini dinle."""
        self.view.root.withdraw()
        whiteboard_view = WhiteboardView(self.view.root, lobby_name, users, self)

        # Sunucudan çizim verilerini düzenli olarak al ve canvas'ı güncelle
        # self.model.listen_for_draw_updates(lobby_name, whiteboard_view.update_canvas)


