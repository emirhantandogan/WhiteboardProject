from tkinter import Tk
from Model.client_model import ClientModel
from View.lobby_view import LobbyView
from Controller.client_controller import ClientController

if __name__ == "__main__":
    root = Tk()

    #localde deniyorsan server ipv4 : 127.0.0.1
    model = ClientModel("127.0.0.1", 12345)  # Sunucu adresini burada ayarlayın
    view = LobbyView(root, None)
    controller = ClientController(model, view)
    view.controller = controller

    root.geometry("800x400")
    root.mainloop()