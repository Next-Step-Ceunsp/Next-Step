import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json, os

DATA_PATH = os.path.join("data", "usuarios.json")

class TelaCadastro(tk.Frame):
    def __init__(self, master, callback_voltar, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.callback_voltar = callback_voltar
        self.config(bg="#18776e")

        # Container central com borda preta
        container = tk.Frame(self, bg="white", bd=3, relief="solid",
                             highlightbackground="black", highlightthickness=2)
        container.place(relx=0.5, rely=0.5, anchor="center", width=400, height=600)

        # --- Logo ---
        try:
            logo_img = Image.open("assets/img/logo.png").resize((120, 120))
            self.logo = ImageTk.PhotoImage(logo_img)
            tk.Label(container, image=self.logo, bg="white").pack(pady=(20, 10))
        except:
            tk.Label(container, text="NextStep", font=("Arial", 22, "bold"),
                     bg="white", fg="#18776e").pack(pady=20)

        tk.Label(container, text="Cadastro", font=("Arial", 20, "bold"),
                 bg="white", fg="#18776e").pack(pady=(5, 15))

        # --- Nome Completo ---
        tk.Label(container, text="Nome Completo", bg="white", fg="black", anchor="w").pack(padx=40, fill="x")
        self.entry_nome = self._create_entry(container)
        self.entry_nome.pack(padx=40, pady=(5, 15), fill="x")

        # --- Email ---
        tk.Label(container, text="Email", bg="white", fg="black", anchor="w").pack(padx=40, fill="x")
        self.entry_email = self._create_entry(container)
        self.entry_email.pack(padx=40, pady=(5, 15), fill="x")

        # --- Senha ---
        tk.Label(container, text="Senha", bg="white", fg="black", anchor="w").pack(padx=40, fill="x")
        senha_frame = tk.Frame(container, bg="white")
        senha_frame.pack(padx=40, pady=(5, 15), fill="x")
        self.entry_senha = self._create_entry(senha_frame, show="*")
        self.entry_senha.pack(side="left", fill="x", expand=True)
        self.btn_ver_senha = tk.Button(senha_frame, text="👁", bg="white", bd=0, command=self.toggle_senha)
        self.btn_ver_senha.pack(side="right")

        # --- Confirmar Senha ---
        tk.Label(container, text="Confirmar Senha", bg="white", fg="black", anchor="w").pack(padx=40, fill="x")
        self.entry_confirmar = self._create_entry(container, show="*")
        self.entry_confirmar.pack(padx=40, pady=(5, 15), fill="x")

        # --- Botões ---
        tk.Button(container, text="Cadastrar", bg="#3dbb9d", fg="white", font=("Arial", 12, "bold"),
                  command=self.cadastrar_usuario).pack(pady=10, ipadx=10, ipady=5)

        tk.Button(container, text="Voltar", bg="white", fg="#18776e", font=("Arial", 12, "bold"),
                  command=self.callback_voltar).pack(pady=5)

        self.senha_visivel = False

    def _create_entry(self, parent, show=None):
        """Cria campo com leve sombra."""
        sombra = tk.Frame(parent, bg="#d9d9d9")
        sombra.pack(fill="x", pady=2)
        entry = tk.Entry(sombra, font=("Arial", 12), relief="flat", show=show)
        entry.pack(fill="x", padx=2, pady=2)
        return entry

    def toggle_senha(self):
        self.senha_visivel = not self.senha_visivel
        show = "" if self.senha_visivel else "*"
        self.entry_senha.config(show=show)
        self.entry_confirmar.config(show=show)

    def cadastrar_usuario(self):
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        senha = self.entry_senha.get().strip()
        confirmar = self.entry_confirmar.get().strip()

        if not nome or not email or not senha or not confirmar:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        if senha != confirmar:
            messagebox.showerror("Erro", "As senhas não conferem.")
            return

        usuarios = {}
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                usuarios = json.load(f)

        if email in usuarios:
            messagebox.showerror("Erro", "Email já cadastrado.")
            return

        usuarios[email] = {"nome": nome, "senha": senha}
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(usuarios, f, indent=4, ensure_ascii=False)

        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        self.callback_voltar()
