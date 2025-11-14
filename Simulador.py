import tkinter as tk
from tkinter import Menu
import webbrowser
from PIL import Image, ImageTk


class SimuladorEntrevista(tk.Frame):
    def __init__(self, master, dados_usuario, callback_sair, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.callback_sair = callback_sair
        self.config(bg="white")

        # ================================
        #   TOP BAR (User + NextStep + Sobre nós)
        # ================================
        topbar = tk.Frame(self, bg="#18776e", height=60)
        topbar.pack(fill="x", side="top")

        # Texto NextStep
        titulo = tk.Label(
            topbar,
            text="NextStep",
            fg="white",
            bg="#18776e",
            font=("Arial", 18, "bold")
        )
        titulo.pack(side="left", padx=20)

        # Botão Sobre Nós
        sobre = tk.Label(
            topbar,
            text="Sobre nós",
            fg="#A7E6D1",
            bg="#18776e",
            cursor="hand2",
            font=("Arial", 14, "italic"),
        )
        sobre.pack(side="left", padx=15)
        sobre.bind("<Button-1>", lambda e: webbrowser.open("https://nextstep3.netlify.app/"))

        # Ícone usuário
        try:
            user_img = Image.open("assets/img/user.png").resize((35, 35))
            self.user_icon = ImageTk.PhotoImage(user_img)
        except:
            self.user_icon = None

        user_button = tk.Button(
            topbar,
            image=self.user_icon,
            bg="#18776e",
            activebackground="#18776e",
            bd=0,
            highlightthickness=0,
            command=self.menu_usuario
        )
        user_button.pack(side="right", padx=20, pady=10)

        # ================================
        #        SIDEBAR
        # ================================
        self.sidebar = tk.Frame(self, bg="#145d54", width=240)
        self.sidebar.pack(side="left", fill="y")

        try:
            logo_img = Image.open("assets/img/logo.png").resize((110, 110))
            self.logo = ImageTk.PhotoImage(logo_img)
            tk.Label(self.sidebar, image=self.logo, bg="#145d54").pack(pady=25)
        except:
            tk.Label(self.sidebar, text="NextStep",
                     font=("Arial", 20, "bold"),
                     fg="white", bg="#145d54").pack(pady=25)

        nova_item = tk.Label(
            self.sidebar,
            text="➕  Nova Entrevista",
            fg="white",
            bg="#145d54",
            font=("Arial", 15, "bold"),
            cursor="hand2",
            pady=15
        )
        nova_item.pack(fill="x")
        nova_item.bind("<Button-1>", lambda e: self.limpar_chat())

        historico_item = tk.Label(
            self.sidebar,
            text="📂  Histórico de Entrevistas",
            fg="white",
            bg="#145d54",
            font=("Arial", 15, "bold"),
            cursor="hand2",
            pady=15
        )
        historico_item.pack(fill="x")
        historico_item.bind("<Button-1>", lambda e: self.abrir_historico())

        # ================================
        #        CHAT + SCROLL
        # ================================
        self.chat_container = tk.Frame(self, bg="white")
        self.chat_container.pack(side="right", fill="both", expand=True)

        self.canvas = tk.Canvas(self.chat_container, bg="white", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scroll = tk.Scrollbar(self.chat_container, command=self.canvas.yview)
        self.scroll.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scroll.set)

        self.chat_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")

        self.chat_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        ))

        # ================================
        #  BARRA DE DIGITAÇÃO COMPLETA (CORRIGIDA)
        # ================================
        input_area = tk.Frame(self, bg="#e9e9e9")
        input_area.pack(fill="x", side="bottom")

        input_area.update_idletasks()
        input_area.configure(height=100)

        self.entry = tk.Entry(
            input_area,
            font=("Arial", 16),
        )
        self.entry.pack(
            fill="both",
            expand=True,
            side="left",
            padx=20,
            pady=20,
            ipady=20  # aumenta a altura do campo de digitação
        )
        self.entry.bind("<Return>", self.enviar_mensagem)

        try:
            send_img = Image.open("assets/img/send.png").resize((35, 35))
            self.send_icon = ImageTk.PhotoImage(send_img)
        except:
            self.send_icon = None

        send_button = tk.Button(
            input_area,
            image=self.send_icon,
            bg="#e9e9e9",
            activebackground="#e9e9e9",
            bd=0,
            command=self.enviar_mensagem
        )
        send_button.pack(side="right", padx=20, pady=10)

    # ================================
    #   MENU DO USUÁRIO
    # ================================
    def menu_usuario(self):
        menu = Menu(self.master, tearoff=0)
        menu.add_command(label="Sair", command=self.callback_sair)
        try:
            menu.tk_popup(self.winfo_rootx() + self.winfo_width() - 100,
                          self.winfo_rooty() + 50)
        finally:
            menu.grab_release()

    # ================================
    #   MENSAGEM DO USER → DIREITA
    # ================================
    def adicionar_mensagem_usuario(self, texto):
        frame = tk.Frame(self.chat_frame, bg="white")
        frame.pack(anchor="e", pady=5, padx=10, fill="x")

        bubble = tk.Label(
            frame,
            text=texto,
            bg="#dff7f3",
            fg="black",
            font=("Arial", 13),
            padx=12,
            pady=8,
            wraplength=700,
            justify="left"
        )
        bubble.pack(anchor="e")

    # ================================
    #   MENSAGEM DA IA → ESQUERDA
    # ================================
    def adicionar_mensagem_ia(self, texto):
        frame = tk.Frame(self.chat_frame, bg="white")
        frame.pack(anchor="w", pady=5, padx=10, fill="x")

        bubble = tk.Label(
            frame,
            text=texto,
            bg="#18776e",
            fg="white",
            font=("Arial", 13),
            padx=12,
            pady=8,
            wraplength=700,
            justify="left"
        )
        bubble.pack(anchor="w")

    # ================================
    #   ENVIAR
    # ================================
    def enviar_mensagem(self, event=None):
        texto = self.entry.get().strip()
        if texto == "":
            return

        self.entry.delete(0, tk.END)
        self.adicionar_mensagem_usuario(texto)

        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1)

    # ================================
    #   LIMPAR CHAT
    # ================================
    def limpar_chat(self):
        for widget in self.chat_frame.winfo_children():
            widget.destroy()

    # ================================
    #   HISTÓRICO
    # ================================
    def abrir_historico(self):
        self.limpar_chat()
        self.adicionar_mensagem_ia("📂 Aqui aparecerá o histórico de entrevistas (em desenvolvimento).")
