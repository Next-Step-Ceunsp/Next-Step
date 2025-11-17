# TelaHome.py (Versão com Dupla Seleção de Botões)
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import webbrowser

class TelaHome(tk.Frame):
    def __init__(self, master, dados_usuario, callback_iniciar_simulador, callback_sair, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.dados_usuario = dados_usuario
        self.callback_iniciar_simulador = callback_iniciar_simulador
        self.callback_sair = callback_sair
        self.config(bg="#18776e")
        
        self.nome_usuario = dados_usuario.get("nome", "Candidato")
        
        # --- Definição das Opções ---
        self.AREAS = {
            "Frontend": "Desenvolvedor Frontend",
            "Backend": "Desenvolvedor Backend",
            "UX/UI Design": "UX/UI Designer",
            "Data Science": "Cientista de Dados",
        }
        self.NIVEIS = ["Júnior", "Pleno", "Sênior"]
        
        # Variáveis de controle para as seleções
        self.area_selecionada = tk.StringVar(value="") 
        self.nivel_selecionado = tk.StringVar(value="")

        # --- Container Central do Card ---
        container = tk.Frame(
            self,
            bg="white",
            bd=3,
            relief="solid",
            highlightbackground="black",
            highlightthickness=2
        )
        container.place(relx=0.5, rely=0.5, anchor="center", width=550, height=680)

        # --- Logo e Boas-vindas (Mantidas) ---
        try:
            logo_img = Image.open("assets/img/logo.png").resize((120, 120))
            self.logo = ImageTk.PhotoImage(logo_img)
            tk.Label(container, image=self.logo, bg="white").pack(pady=(20, 10))
        except:
            tk.Label(container, text="NextStep",
                     font=("Poppins", 22, "bold"),
                     bg="white", fg="#18776e").pack(pady=(20, 10))

        tk.Label(
            container,
            text=f"Olá, {self.nome_usuario}!",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#18776e"
        ).pack(pady=(0, 20))


        # ====================================
        #   1. SELEÇÃO DE ÁREA
        # ====================================
        tk.Label(
            container,
            text="1. Escolha sua **Área de Atuação**:",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#333"
        ).pack(pady=(10, 5))
        
        self.botoes_area_frame = tk.Frame(container, bg="white")
        self.botoes_area_frame.pack(padx=20, pady=5, fill="x")

        # Criação dos botões de Área (4 opções em 2 colunas)
        self.criar_botoes_selecao(self.botoes_area_frame, self.AREAS.keys(), self.area_selecionada, colunas=2)

        # ====================================
        #   2. SELEÇÃO DE NÍVEL
        # ====================================
        tk.Label(
            container,
            text="2. Escolha seu **Nível de Experiência**:",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#333"
        ).pack(pady=(20, 5))
        
        self.botoes_nivel_frame = tk.Frame(container, bg="white")
        self.botoes_nivel_frame.pack(padx=40, pady=5)

        # Criação dos botões de Nível (3 opções em 3 colunas)
        self.criar_botoes_selecao(self.botoes_nivel_frame, self.NIVEIS, self.nivel_selecionado, colunas=3)

        # --- Botão Iniciar Simulação ---
        self.btn_iniciar = tk.Button(
            container,
            text="🚀 Iniciar Simulação",
            bg="#A7E6D1", 
            fg="#666",
            font=("Arial", 14, "bold"),
            bd=0,
            state=tk.DISABLED, 
            activebackground="#2fa083",
            activeforeground="white",
            command=self.iniciar_simulacao
        )
        self.btn_iniciar.pack(pady=30, ipadx=20, ipady=10)

        # --- Botão Sair ---
        tk.Button(
            container,
            text="Voltar ao Login",
            bg="white",
            fg="#18776e",
            font=("Arial", 10, "underline"),
            bd=0,
            command=self.callback_sair
        ).pack(pady=5)
        
        # Chama a função para garantir o estado inicial dos botões
        self.atualizar_estilo()


    def criar_botoes_selecao(self, parent_frame, opcoes, var_controle, colunas):
        """Função utilitária para criar botões de seleção e configurar o layout em grid."""
        
        radio_style = {
            "bg": "white",
            "fg": "#333",
            "font": ("Arial", 11, "bold"),
            "selectcolor": "white",
            "activebackground": "white",
            "activeforeground": "#18776e",
            "indicatoron": 0, 
            "padx": 15,
            "pady": 10,
            "relief": "groove",
            "bd": 1,
        }
        
        for i, item in enumerate(opcoes):
            btn = tk.Radiobutton(
                parent_frame,
                text=item,
                variable=var_controle,
                value=item,
                command=self.atualizar_estilo, 
                **radio_style
            )
            row = i // colunas
            col = i % colunas
            # O sticky="ew" garante que os botões se expandam para preencher a célula
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

        # Configura as colunas do frame para se expandirem uniformemente
        for col in range(colunas):
            parent_frame.grid_columnconfigure(col, weight=1)


    def atualizar_estilo(self):
        """Atualiza a aparência de todos os botões de área e nível, e o botão Iniciar."""
        
        selecao_area = self.area_selecionada.get()
        selecao_nivel = self.nivel_selecionado.get()

        # --- Atualizar estilo dos botões de ÁREA ---
        for btn in self.botoes_area_frame.winfo_children():
            if isinstance(btn, tk.Radiobutton):
                if btn.cget("text") == selecao_area:
                    btn.config(bg="#18776e", fg="white", relief="raised")
                else:
                    btn.config(bg="white", fg="#333", relief="groove")
        
        # --- Atualizar estilo dos botões de NÍVEL ---
        for btn in self.botoes_nivel_frame.winfo_children():
            if isinstance(btn, tk.Radiobutton):
                if btn.cget("text") == selecao_nivel:
                    btn.config(bg="#18776e", fg="white", relief="raised")
                else:
                    btn.config(bg="white", fg="#333", relief="groove")

        # --- Habilitar/Desabilitar botão Iniciar ---
        if selecao_area and selecao_nivel:
            self.btn_iniciar.config(state=tk.NORMAL, bg="#3dbb9d", fg="white")
        else:
            self.btn_iniciar.config(state=tk.DISABLED, bg="#A7E6D1", fg="#666")


    def iniciar_simulacao(self):
        area = self.area_selecionada.get()
        nivel = self.nivel_selecionado.get()
        
        if not area or not nivel:
            messagebox.showwarning("Atenção", "Por favor, selecione uma área e um nível para iniciar a entrevista.")
            return
            
        # Constrói a descrição detalhada da vaga para a IA
        # Exemplo: "Desenvolvedor Backend Pleno na empresa fictícia NextStep"
        cargo_base = self.AREAS.get(area, "Vaga Genérica")
        vaga_empresa = f"{cargo_base} {nivel} na empresa fictícia NextStep"
        
        # Chama o callback no main.py, passando os dados da vaga
        self.callback_iniciar_simulador(vaga_empresa)