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

        # --- Container central ---
        container = tk.Frame(
            self,
            bg="white",
            bd=3,
            relief="solid",
            highlightbackground="black",
            highlightthickness=2
        )
        container.place(relx=0.5, rely=0.5, anchor="center", width=400, height=650)

        # --- Logo ---
        try:
            logo_img = Image.open("assets/img/logo.png").resize((120, 120))
            self.logo = ImageTk.PhotoImage(logo_img)
            tk.Label(container, image=self.logo, bg="white").pack(pady=(20, 10))
        except:
            tk.Label(container, text="NextStep",
                     font=("Poppins", 22, "bold"),
                     bg="white", fg="#18776e").pack(pady=(20, 10))

        # --- Título ---
        tk.Label(container, text="Faça Cadastro",
                 font=("Poppins", 20, "bold"),
                 bg="white", fg="#18776e").pack(pady=(5, 15))

        # --- Função para criar input sem sombra ---
        def criar_campo(parent, show=None):
            entry = tk.Entry(
                parent,
                font=("Poppins", 12),
                bg="#f9f9f9",
                relief="flat",
                highlightthickness=1,
                highlightbackground="#ccc",
                highlightcolor="#18776e",
                show=show
            )
            return entry

        # --- Nome Completo ---
        tk.Label(container, text="Nome Completo", bg="white", fg="black",
                 font=("Poppins", 10), anchor="w").pack(padx=40, fill="x")
        self.entry_nome = criar_campo(container)
        self.entry_nome.pack(padx=40, pady=(5, 15), fill="x", ipady=8)

        # --- Email ---
        tk.Label(container, text="Email", bg="white", fg="black",
                 font=("Poppins", 10), anchor="w").pack(padx=40, fill="x")
        self.entry_email = criar_campo(container)
        self.entry_email.pack(padx=40, pady=(5, 15), fill="x", ipady=8)

        # --- Senha ---
        tk.Label(container, text="Senha", bg="white", fg="black",
                 font=("Poppins", 10), anchor="w").pack(padx=40, fill="x")
        frame_senha = tk.Frame(container, bg="white")
        frame_senha.pack(padx=40, pady=(5, 15), fill="x")
        self.entry_senha = criar_campo(frame_senha, show="*")
        self.entry_senha.pack(side="left", fill="x", expand=True, ipady=8)

        # Olhinho senha
        self.btn_olho = tk.Button(frame_senha, text="👁", bg="white", bd=0,
                                  command=self.toggle_senha)
        self.btn_olho.pack(side="right")

        # --- Confirmar Senha ---
        tk.Label(container, text="Confirmar Senha", bg="white", fg="black",
                 font=("Poppins", 10), anchor="w").pack(padx=40, fill="x")
        self.entry_confirmar = criar_campo(container, show="*")
        self.entry_confirmar.pack(padx=40, pady=(5, 15), fill="x", ipady=8)

        # Estado do olho
        self.senha_visivel = False

        # --- Botão Cadastrar ---
        tk.Button(
            container,
            text="Cadastrar",
            bg="#3dbb9d",
            fg="white",
            font=("Poppins", 12, "bold"),
            bd=0,
            activebackground="#2fa083",
            activeforeground="white",
            command=self.cadastrar_usuario
        ).pack(pady=10, ipadx=10, ipady=5)

        # --- Botão Voltar ---
        tk.Button(
            container,
            text="Voltar",
            bg="white",
            fg="#18776e",
            font=("Poppins", 12, "bold"),
            bd=0,
            activeforeground="#18776e",
            command=self.callback_voltar
        ).pack(pady=5)

    # --- Mostrar/Ocultar senha ---
    def toggle_senha(self):
        self.senha_visivel = not self.senha_visivel
        show = "" if self.senha_visivel else "*"
        self.entry_senha.config(show=show)
        self.entry_confirmar.config(show=show)

    # --- Cadastro ---
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

        # Carrega JSON
        usuarios = {}
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                usuarios = json.load(f)

        if email in usuarios:
            messagebox.showerror("Erro", "Este email já está cadastrado.")
            return

        # Salvar
        usuarios[email] = {
            "nome": nome,
            "senha": senha
        }

        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(usuarios, f, indent=4, ensure_ascii=False)

        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        self.callback_voltar()
