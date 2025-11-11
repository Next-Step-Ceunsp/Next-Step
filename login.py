import tkinter as tk
from tkinter import messagebox
import json
import os

# Caminho para o banco de dados local
DATA_PATH = os.path.join("data", "usuarios.json")

class TelaLogin(tk.Frame):
    def __init__(self, master, callback_login_sucesso, callback_open_cadastro, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.callback_login_sucesso = callback_login_sucesso
        self.callback_open_cadastro = callback_open_cadastro
        self.config(bg="#18776e")

        # --- Título ---
        tk.Label(self, text="Login - NextStep", font=("Arial", 18, "bold"), bg="#18776e", fg="white").pack(pady=20)

        # --- Campo Usuário ---
        tk.Label(self, text="Usuário:", bg="#18776e", fg="white").pack()
        self.entry_usuario = tk.Entry(self, font=("Arial", 14))
        self.entry_usuario.pack(pady=5)

        # --- Campo Senha ---
        tk.Label(self, text="Senha:", bg="#18776e", fg="white").pack()
        self.entry_senha = tk.Entry(self, show="*", font=("Arial", 14))
        self.entry_senha.pack(pady=5)

        # --- Botões ---
        tk.Button(
            self,
            text="Entrar",
            bg="#3dbb9d",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.fazer_login,
            width=15
        ).pack(pady=10)

        tk.Button(
            self,
            text="Cadastrar",
            bg="white",
            fg="#18776e",
            font=("Arial", 12, "bold"),
            command=self.abrir_cadastro,
            width=15
        ).pack(pady=5)

    # --- Função de login ---
    def fazer_login(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()

        if not usuario or not senha:
            messagebox.showerror("Erro", "Preencha usuário e senha.")
            return

        if not os.path.exists(DATA_PATH):
            messagebox.showerror("Erro", "Nenhum usuário cadastrado ainda.")
            return

        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                usuarios = json.load(f)
        except Exception:
            messagebox.showerror("Erro", "Falha ao ler dados dos usuários.")
            return

        if usuario in usuarios and usuarios[usuario] == senha:
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            self.callback_login_sucesso(usuario)  # ✅ Corrigido: agora envia o nome do usuário
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    # --- Abre a tela de cadastro ---
    def abrir_cadastro(self):
        self.callback_open_cadastro()
