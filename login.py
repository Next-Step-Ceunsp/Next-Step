# login.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
import webbrowser  # opcional, caso queira usar redefinir_senha que abre link

DATA_PATH = os.path.join("data", "usuarios.json")


class TelaLogin(tk.Frame):
    def __init__(self, master, callback_login_sucesso, callback_open_cadastro, callback_open_esquecer, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.callback_login_sucesso = callback_login_sucesso
        self.callback_open_cadastro = callback_open_cadastro
        self.callback_open_esquecer = callback_open_esquecer

        self.config(bg="#18776e")

        # --- Container do card ---
        container = tk.Frame(
            self,
            bg="white",
            bd=2,
            relief="solid",
            highlightbackground="#18776e",
            highlightthickness=2
        )
        container.place(relx=0.5, rely=0.5, anchor="center", width=400, height=580)

        # --- Logo ---
        try:
            logo_img = Image.open("assets/img/logo.png").resize((120, 120))
            self.logo = ImageTk.PhotoImage(logo_img)
            tk.Label(container, image=self.logo, bg="white").pack(pady=(20, 10))
        except Exception:
            tk.Label(container, text="NextStep",
                     font=("Poppins", 22, "bold"),
                     bg="white", fg="#18776e").pack(pady=20)

        # --- “Bem-vindo” ---
        tk.Label(container, text="Bem-vindo de volta!",
                 font=("Poppins", 22, "bold"),
                 bg="white", fg="#18776e").pack()

        # --- Título ---
        tk.Label(container, text="Faça Login",
                 font=("Poppins", 18, "bold"),
                 bg="white", fg="#18776e").pack(pady=(0, 12))

        # --- Email ---
        tk.Label(container, text="Email", bg="white", fg="black",
                 anchor="w", font=("Poppins", 10)).pack(padx=40, fill="x")

        self.entry_email = tk.Entry(
            container,
            font=("Poppins", 12),
            bg="#f9f9f9",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#ccc",
            highlightcolor="#18776e"
        )
        self.entry_email.pack(padx=40, pady=(5, 12), fill="x", ipady=8)

        # --- Senha ---
        tk.Label(container, text="Senha", bg="white", fg="black",
                 anchor="w", font=("Poppins", 10)).pack(padx=40, fill="x")

        senha_frame = tk.Frame(container, bg="white")
        senha_frame.pack(padx=40, pady=(5, 12), fill="x")

        self.entry_senha = tk.Entry(
            senha_frame,
            show="*",
            font=("Poppins", 12),
            bg="#f9f9f9",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#ccc",
            highlightcolor="#18776e"
        )
        self.entry_senha.pack(side="left", fill="x", expand=True, ipady=8)

        # Botão de mostrar senha
        self.senha_visivel = False
        tk.Button(
            senha_frame,
            text="👁",
            bg="white",
            bd=0,
            font=("Poppins", 10),
            command=self.toggle_senha
        ).pack(side="right")

        # --- Esqueci a senha ---
        lbl_esqueci = tk.Label(
            container,
            text="Esqueci minha senha",
            fg="#18776e",
            bg="white",
            cursor="hand2",
            font=("Poppins", 9, "underline")
        )
        lbl_esqueci.pack(pady=(0, 8))
        lbl_esqueci.bind("<Button-1>", lambda e: self.callback_open_esquecer())

        # --- Botão Entrar ---
        tk.Button(
            container,
            text="Entrar",
            bg="#3dbb9d",
            fg="white",
            font=("Poppins", 12, "bold"),
            bd=0,
            command=self.fazer_login
        ).pack(pady=10, ipadx=10, ipady=5)

        # --- Cadastre-se ---
        lbl_cadastro = tk.Label(
            container,
            text="Não possui conta? Cadastre-se",
            fg="#18776e",
            bg="white",
            cursor="hand2",
            font=("Poppins", 10, "underline")
        )
        lbl_cadastro.pack(pady=10)
        lbl_cadastro.bind("<Button-1>", lambda e: self.callback_open_cadastro())

    # --- Mostrar/Ocultar senha ---
    def toggle_senha(self):
        self.senha_visivel = not self.senha_visivel
        self.entry_senha.config(show="" if self.senha_visivel else "*")

    # --- Fazer login ---
    def fazer_login(self):
        email = self.entry_email.get().strip()
        senha = self.entry_senha.get().strip()

        if not email or not senha:
            messagebox.showerror("Erro", "Preencha email e senha.")
            return

        if not os.path.exists(DATA_PATH):
            messagebox.showerror("Erro", "Nenhum usuário cadastrado ainda.")
            return

        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                usuarios = json.load(f)
        except Exception:
            messagebox.showerror("Erro", "Erro ao ler o arquivo de usuários.")
            return

        # espera-se que usuarios seja um dict: { "email@ex.com": {"nome": "...", "senha": "..."} }
        if email in usuarios and usuarios[email].get("senha") == senha:
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            # envia o objeto do usuário (com nome, senha...) para o callback
            self.callback_login_sucesso(usuarios[email])
        else:
            messagebox.showerror("Erro", "Email ou senha incorretos.")

    # --- (opcional) função para abrir link de redefinição ---
    def redefinir_senha(self):
        email = self.entry_email.get().strip()
        if not email:
            messagebox.showwarning("Atenção", "Digite seu email para redefinir a senha.")
            return
        # implementar envio real ou abrir página externa
        webbrowser.open("https://nextstep.com/redefinir-senha")
        messagebox.showinfo("Recuperação", f"Se esse email existir, você receberá instruções em: {email}")
