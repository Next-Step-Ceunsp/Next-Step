# main.py (Versão Corrigida para incluir TelaHome)
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time
import threading

from login import TelaLogin
from Simulador import SimuladorEntrevista
from cadastro import TelaCadastro
from esquecersenha import TelaEsquecerSenha
from TelaHome import TelaHome # NOVO: Importa a TelaHome


# --- CÓDIGO DA SPLASHSCREEN (MANTIDO INALTERADO) ---
class SplashScreen(tk.Frame):
    def __init__(self, master, on_finish_callback, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.on_finish_callback = on_finish_callback
        self.config(bg="#18776e")

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
                     fg="white").pack()
        except:
             tk.Label(container, text="NextStep", font=("Arial", 28, "bold"),
                     fg="white", bg="#18776e").pack(pady=40)

        self.pb = ttk.Progressbar(container, orient="horizontal", length=200, mode="determinate")
        self.pb.pack(pady=20)
        self.pb.start(10)

        # Inicia a thread para a transição
        threading.Thread(target=self._simular_carregamento, daemon=True).start()

    def _simular_carregamento(self):
        # Simula um tempo de carregamento
        time.sleep(2) 
        self.master.after(0, self.on_finish_callback)
        

class NextStepApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NextStep - Simulador de Entrevista")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        self.root.config(bg="#18776e")
        self.root.protocol("WM_DELETE_WINDOW", self.on_fechar)
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        self.user_data = None # Armazena os dados do usuário logado

        self.splash = SplashScreen(self.root, self.mostrar_login)
        self.splash.pack(fill="both", expand=True)

    # --- LIMPAR TELA ---
    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- LOGIN ---
    def mostrar_login(self):
        self.limpar_tela()
        self.login = TelaLogin(
            self.root,
            self.login_sucesso,
            self.mostrar_cadastro,
            self.mostrar_esquecersenha
        )
        self.login.pack(fill="both", expand=True)

    # --- HOME (NOVO PONTO DE ENTRADA PÓS-LOGIN) ---
    def login_sucesso(self, dados_usuario):
        self.user_data = dados_usuario
        self.limpar_tela()
        self.home = TelaHome(
            self.root,
            self.user_data,
            callback_iniciar_simulador=self.iniciar_simulador, # Novo callback
            callback_sair=self.mostrar_login # Volta para o Login
        )
        self.home.pack(fill="both", expand=True)

    # --- INICIAR SIMULADOR (NOVA FUNÇÃO DE TRANSIÇÃO) ---
    def iniciar_simulador(self, vaga_empresa):
        self.limpar_tela()
        self.simulador = SimuladorEntrevista(
            self.root,
            self.user_data,
            vaga_empresa, # Passa a vaga/empresa
            callback_sair=lambda: self.login_sucesso(self.user_data) # Volta para a Home/Menu Principal
        )
        self.simulador.pack(fill="both", expand=True)


    # --- CADASTRO ---
    def mostrar_cadastro(self):
        self.limpar_tela()
        self.cadastro = TelaCadastro(self.root, self.mostrar_login)
        self.cadastro.pack(expand=True, fill="both")

    # --- ESQUECER SENHA ---
    def mostrar_esquecersenha(self):
        self.limpar_tela()
        self.esquecer = TelaEsquecerSenha(self.root, self.mostrar_login)
        self.esquecer.pack(expand=True, fill="both")

    # --- FECHAR ---
    def on_fechar(self):
        if messagebox.askokcancel("Sair", "Tem certeza que deseja fechar o aplicativo?"):
            self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = NextStepApp()
    app.run()