# cadastro.py
import tkinter as tk
from tkinter import messagebox
import json
import os

DATA_DIR = "data"
DATA_PATH = os.path.join(DATA_DIR, "usuarios.json")

class TelaCadastro(tk.Frame):
    def __init__(self, master, callback_voltar, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.callback_voltar = callback_voltar
        self.config(bg="#18776e")

        tk.Label(self, text="Cadastro - NextStep", font=("Arial", 18, "bold"), bg="#18776e", fg="white").pack(pady=20)

        tk.Label(self, text="Novo usuário:", bg="#18776e", fg="white").pack()
        self.entry_usuario = tk.Entry(self)
        self.entry_usuario.pack(pady=5)

        tk.Label(self, text="Senha:", bg="#18776e", fg="white").pack()
        self.entry_senha = tk.Entry(self, show="*")
        self.entry_senha.pack(pady=5)

        tk.Button(self, text="Cadastrar", bg="#3dbb9d", fg="white", command=self.cadastrar).pack(pady=10)
        tk.Button(self, text="Voltar", bg="white", fg="#18776e", command=self.voltar).pack(pady=5)

    def cadastrar(self):
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()

        if not usuario or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

        if os.path.exists(DATA_PATH):
            try:
                with open(DATA_PATH, "r", encoding="utf-8") as f:
                    usuarios = json.load(f)
            except Exception:
                usuarios = {}
        else:
            usuarios = {}

        if usuario in usuarios:
            messagebox.showerror("Erro", "Usuário já cadastrado.")
            return

        usuarios[usuario] = senha

        try:
            with open(DATA_PATH, "w", encoding="utf-8") as f:
                json.dump(usuarios, f, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar usuário: {e}")
            return

        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        self.callback_voltar()

    def voltar(self):
        self.callback_voltar()
