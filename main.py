import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
import threading
from login import TelaLogin
from simulador import SimuladorEntrevista
from cadastro import TelaCadastro  # ✅ importante: importa a tela de cadastro


class SplashScreen(tk.Frame):
    def __init__(self, master, on_finish_callback, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.on_finish_callback = on_finish_callback
        self.config(bg="#18776e")

        # Tela cheia
        self.pack(fill="both", expand=True)
        container = tk.Frame(self, bg="#18776e")
        container.place(relx=0.5, rely=0.5, anchor="center")

        try:
            self.logo_img = Image.open("assets/img/logo.png")
            self.logo_img = self.logo_img.resize((280, 280))
            self.logo = ImageTk.PhotoImage(self.logo_img)

            frame_logo = tk.Frame(container, bg="#18776e")
            frame_logo.pack(pady=(0, 20))
            tk.Label(frame_logo, image=self.logo, bg="#18776e").pack()
            tk.Label(frame_logo, text="NextStep", font=("Arial", 28, "bold"),
                     fg="white", bg="#18776e").pack(pady=(10, 0))
        except:
            tk.Label(container, text="NextStep", font=("Arial", 36, "bold"),
                     fg="white", bg="#18776e").pack(pady=(0, 20))

        self.texto = tk.Label(container,
                              text="Sua próxima entrevista começa aqui.",
                              font=("Arial", 18), fg="white", bg="#18776e")
        self.texto.pack(pady=(0, 30))

        self.progress = ttk.Progressbar(container,
                                        orient="horizontal",
                                        length=400,
                                        mode="indeterminate")
        self.progress.pack(pady=(10, 10))
        self.progress.start(15)

        threading.Thread(target=self.aguardar_e_transitar, daemon=True).start()

    def aguardar_e_transitar(self):
        time.sleep(3.5)
        self.on_finish_callback()


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("NextStep - Simulador de Entrevistas")
        self.root.attributes('-fullscreen', True)
        self.root.config(bg="#18776e")
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        self.splash = SplashScreen(self.root, self.mostrar_login)
        self.splash.pack(fill="both", expand=True)

    # --- Limpa widgets anteriores ---
    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- LOGIN ---
    def mostrar_login(self):
        self.limpar_tela()
        self.login = TelaLogin(self.root, self.login_sucesso, self.mostrar_cadastro)
        self.login.pack(fill="both", expand=True)

    # --- LOGIN SUCESSO ---
    def login_sucesso(self, usuario):
        self.limpar_tela()
        self.simulador = SimuladorEntrevista(self.root, usuario, callback_sair=self.mostrar_login)
        self.simulador.pack(fill="both", expand=True)

    # --- CADASTRO ---
    def mostrar_cadastro(self):
        self.limpar_tela()
        self.cadastro = TelaCadastro(self.root, self.mostrar_login)
        self.cadastro.pack(expand=True, fill="both")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
