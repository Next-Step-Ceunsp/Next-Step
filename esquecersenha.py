import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json, os

DATA_PATH = os.path.join("data", "usuarios.json")

class TelaEsquecerSenha(tk.Frame):
    def __init__(self, master, callback_voltar, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.callback_voltar = callback_voltar
        self.config(bg="#18776e")

        # --- Container do Card ---
        container = tk.Frame(
            self,
            bg="white",
            bd=3,
            relief="solid",
            highlightbackground="black",
            highlightthickness=2
        )
        container.place(relx=0.5, rely=0.5, anchor="center", width=400, height=420)

        # --- Logo centralizada ---
        try:
            logo_img = Image.open("assets/img/logo.png").resize((120, 120))
            self.logo = ImageTk.PhotoImage(logo_img)
            tk.Label(container, image=self.logo, bg="white").pack(pady=(20, 10))
        except:
            tk.Label(container, text="NextStep",
                     font=("Poppins", 22, "bold"),
                     bg="white", fg="#18776e").pack(pady=20)

        # --- Título ---
        tk.Label(
            container,
            text="Recuperar Senha",
            font=("Poppins", 18, "bold"),
            fg="#18776e",
            bg="white"
        ).pack(pady=(5, 10))

        # --- Texto Informativo ---
        tk.Label(
            container,
            text="Digite seu e-mail para receber o link:",
            bg="white",
            fg="black",
            anchor="w",
            font=("Poppins", 10)
        ).pack(padx=40, fill="x")

        # --- Campo Email ---
        self.entry_email = tk.Entry(
            container,
            font=("Poppins", 12),
            bg="#f9f9f9",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#ccc",
            highlightcolor="#18776e"
        )
        self.entry_email.pack(padx=40, pady=10, fill="x", ipady=8)

        # --- Botão Enviar ---
        tk.Button(
            container,
            text="Enviar link",
            bg="#3dbb9d",
            fg="white",
            font=("Poppins", 12, "bold"),
            bd=0,
            activebackground="#2fa083",
            command=self.enviar_link
        ).pack(pady=10, ipadx=10, ipady=5)

        # --- Botão Voltar ---
        tk.Button(
            container,
            text="Voltar",
            bg="white",
            fg="#18776e",
            font=("Poppins", 11, "bold"),
            bd=0,
            command=self.callback_voltar
        ).pack(pady=5)


    def enviar_link(self):
        email = self.entry_email.get().strip()

        if not email:
            messagebox.showerror("Erro", "Digite o email.")
            return

        if not os.path.exists(DATA_PATH):
            messagebox.showerror("Erro", "Nenhum usuário cadastrado ainda.")
            return

        with open(DATA_PATH, "r", encoding="utf-8") as f:
            usuarios = json.load(f)

        if email not in usuarios:
            messagebox.showerror("Erro", "Email não encontrado.")
            return

        # Aqui seria onde você realmente enviaria o email (simulado)
        messagebox.showinfo(
            "Sucesso",
            f"Um link de recuperação foi enviado para:\n{email}\n\n(Envio simulado)"
        )
