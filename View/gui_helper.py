from tkinter import Tk, Label, Button, Entry, Listbox, Frame, END

class GUIHelper:
    def __init__(self):
        return

    def create_button(parent, text):
        def on_enter(event):
            button.configure(bg="#0056b3")  # Koyu mavi renk

        def on_leave(event):
            button.configure(bg="#007BFF")  # Orijinal mavi renk

        def on_press(event):
            button.configure(bg="#003f7f")  # Daha koyu mavi

        def on_release(event):
            button.configure(bg="#0056b3")  # Tıklama sonrası rengi hafif koyulaştır

        button = Button(
            parent,
            text=text,
            bg="#007BFF",
            fg="white",
            font=("Arial", 14, "bold"),
            relief="flat",
            bd=0,
            highlightthickness=0,
            padx=10,
            pady=5,
            cursor="hand2",
            activebackground="#003f7f",  # Tıklanırken arka plan rengi
            activeforeground="white"  # Tıklanırken yazı rengi
        )

        # Etkileşim olayları
        button.bind("<Enter>", on_enter)  # Fare üzerine geldiğinde
        button.bind("<Leave>", on_leave)  # Fare ayrıldığında
        button.bind("<ButtonPress-1>", on_press)  # Tıklama anında
        button.bind("<ButtonRelease-1>", on_release)  # Tıklama bırakıldığında

        return button

    def create_entry(parent, placeholder=""):
        entry = Entry(
            parent,
            font=("Arial", 14),  # Daha büyük yazı boyutu
            relief="flat",  # Düz kenarlık
            bd=2,  # Kenar genişliği
            fg="grey"  # Placeholder için gri metin rengi
        )
        entry.configure(highlightbackground="#007BFF", highlightthickness=1)  # Modern mavi kenarlık

        # Placeholder'ı gösterme
        entry.insert(0, placeholder)

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.config(fg="black")  # Normal metin rengine geç

        def on_focus_out(event):
            if not entry.get():  # Eğer giriş boşsa tekrar placeholder'ı göster
                entry.insert(0, placeholder)
                entry.config(fg="grey")

        def get_actual_value():
            # Placeholder göründüğü durumda None döner, aksi halde kullanıcı girdisini döner
            return None if entry.get() == placeholder else entry.get()

        # Olayları bağlama
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        # Yeni bir metot ekleyerek giriş değerini doğru şekilde kontrol edebiliriz
        entry.get_actual_value = get_actual_value

        return entry

    def create_label(parent, text, bg_color = "white" ,color="black"):
        """Modern etiket oluşturur."""
        return Label(
            parent,
            text=text,
            fg=color,
            bg=bg_color,
            font=("Arial", 20, "bold"),
            anchor="w",
        )
