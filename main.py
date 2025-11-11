import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # pip install pillow
import time
import threading
from login import TelaLogin


class SplashScreen(tk.Frame):
    def __init__(self, master, on_finish_callback, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.on_finish_callback = on_finish_callback
        self.config(bg="#18776e")

        # Ocupa toda a tela
        self.pack(fill="both", expand=True)

        # Cria um container centralizado
        container = tk.Frame(self, bg="#18776e")
        container.place(relx=0.5, rely=0.5, anchor="center")

        # --- LOGO ---
               # --- LOGO + NOME DO PROJETO ---
        try:
            # Aumente aqui o tamanho da logo conforme quiser
            self.logo_img = Image.open("assets/img/logo.png")
            self.logo_img = self.logo_img.resize((280, 280))  # tamanho ajustável
            self.logo = ImageTk.PhotoImage(self.logo_img)

            # Frame para logo e nome do projeto
            frame_logo = tk.Frame(container, bg="#18776e")
            frame_logo.pack(pady=(0, 20))

            # Logo centralizada
            tk.Label(frame_logo, image=self.logo, bg="#18776e").pack()

            # Nome do projeto logo abaixo da logo
            tk.Label(frame_logo,
                     text="NextStep",
                     font=("Arial", 28, "bold"),
                     fg="white", bg="#18776e").pack(pady=(10, 0))

        except:
            tk.Label(container, text="NextStep", font=("Arial", 36, "bold"),
                     fg="white", bg="#18776e").pack(pady=(0, 20))


        # --- TEXTO ---
        self.texto = tk.Label(container,
                              text="Sua próxima entrevista começa aqui.",
                              font=("Arial", 18), fg="white", bg="#18776e")
        self.texto.pack(pady=(0, 30))

        # --- PROGRESS BAR ---
        self.progress = ttk.Progressbar(container,
                                        orient="horizontal",
                                        length=400,
                                        mode="indeterminate")
        self.progress.pack(pady=(10, 10))
        self.progress.start(15)

        # Thread para transição automática
        threading.Thread(target=self.aguardar_e_transitar, daemon=True).start()

    def aguardar_e_transitar(self):
        time.sleep(3.5)  # tempo da splash (em segundos)
        self.on_finish_callback()


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("NextStep - Simulador de Entrevistas")
        self.root.attributes('-fullscreen', True)  # Tela cheia
        self.root.config(bg="#18776e")
        self.root.bind("<Escape>", lambda e: self.root.destroy())  # Fecha com ESC

        self.splash = SplashScreen(self.root, self.mostrar_login)
        self.splash.pack(fill="both", expand=True)

    def mostrar_login(self):
        # Remove splash e mostra a tela de login
        self.splash.destroy()
        self.login = TelaLogin(self.root, self.login_sucesso, self.abrir_cadastro)
        self.login.pack(fill="both", expand=True)

    def login_sucesso(self, usuario):
        # Aqui futuramente vai abrir o simulador
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text=f"Bem-vindo, {usuario}!", font=("Arial", 28, "bold"),
                 fg="#18776e", bg="white").pack(expand=True, fill="both")

    def abrir_cadastro(self):
        # Aqui você pode adicionar sua tela de cadastro
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Tela de Cadastro (em construção)",
                 font=("Arial", 22, "bold"), fg="white", bg="#18776e").pack(expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
