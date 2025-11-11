# simulador.py
import tkinter as tk
from tkinter import messagebox

class FrameConfigEntrevista(tk.Frame):
    def __init__(self, master, continuar_callback, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.config(bg="#18776e")

        self.continuar_callback = continuar_callback

        self.area_selecionada = None
        self.nivel_selecionado = None

        self.botoes_area = {}
        self.botoes_nivel = {}

        titulo = tk.Label(self, text="Agora vamos configurar sua entrevista de emprego!",
                          font=("Arial", 16, "bold"), fg="white", bg="#18776e")
        titulo.pack(pady=(20,10))

        label_area = tk.Label(self, text="Escolha sua área de interesse:",
                              font=("Arial", 12), fg="white", bg="#18776e")
        label_area.pack(pady=(10,10))

        frame_area = tk.Frame(self, bg="#18776e")
        frame_area.pack(pady=(0,20))

        areas = [
            ("Tecnologia", "<>", "#a64ca6"),
            ("Saúde", "+", "#d93838"),
            ("Administração", "👤", "#2d82c9"),
            ("Marketing", "📞", "#e3a52f")
        ]

        for nome, icone, cor in areas:
            btn = tk.Button(frame_area, text=f"{icone}\n{nome}",
                            font=("Arial", 10),
                            width=10, height=5,
                            relief="flat",
                            bg="white",
                            fg="black",
                            command=lambda n=nome: self.selecionar_area(n))
            btn.pack(side="left", padx=8)
            self.botoes_area[nome] = btn

        label_nivel = tk.Label(self, text="Escolha o seu nível de experiência:",
                              font=("Arial", 12), fg="white", bg="#18776e")
        label_nivel.pack(pady=(10,10))

        frame_nivel = tk.Frame(self, bg="#18776e")
        frame_nivel.pack(pady=(0,20))

        niveis = [
            ("Junior", "0-2 anos de experiência"),
            ("Pleno", "2-5 anos de experiência"),
            ("Senior", "+5 anos de experiência"),
        ]

        for nome, desc in niveis:
            btn = tk.Button(frame_nivel, text=f"{nome}\n{desc}",
                            font=("Arial", 10),
                            width=16, height=3,
                            relief="flat",
                            bg="white",
                            fg="black",
                            justify="center",
                            command=lambda n=nome: self.selecionar_nivel(n))
            btn.pack(side="left", padx=8)
            self.botoes_nivel[nome] = btn

        self.btn_continuar = tk.Button(self, text="Continuar",
                                       font=("Arial", 14),
                                       bg="#3dbb9d",
                                       fg="white",
                                       relief="flat",
                                       width=20,
                                       command=self.continuar)
        self.btn_continuar.pack(pady=(20,30))

    def selecionar_area(self, nome):
        for btn in self.botoes_area.values():
            btn.config(bg="white", fg="black", relief="flat", bd=0)
        btn_sel = self.botoes_area[nome]
        btn_sel.config(bg="#3dbb9d", fg="white", relief="solid", bd=2)
        self.area_selecionada = nome

    def selecionar_nivel(self, nome):
        for btn in self.botoes_nivel.values():
            btn.config(bg="white", fg="black", relief="flat", bd=0)
        btn_sel = self.botoes_nivel[nome]
        btn_sel.config(bg="#3dbb9d", fg="white", relief="solid", bd=2)
        self.nivel_selecionado = nome

    def continuar(self):
        if not self.area_selecionada or not self.nivel_selecionado:
            messagebox.showerror("Erro", "Por favor, selecione a área e o nível de experiência.")
            return
        self.continuar_callback(self.area_selecionada, self.nivel_selecionado)


class SimuladorEntrevista:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Entrevista de Emprego")
        # restringe tamanho mínimo e inicial
        self.root.geometry("600x450")
        self.root.minsize(520, 420)

        self.frame1 = tk.Frame(self.root)
        self.frame2 = FrameConfigEntrevista(self.root, continuar_callback=self.iniciar_entrevista)
        self.frame_entrevista = tk.Frame(self.root)

        self.frame1.pack(fill="both", expand=True)
        self.mostrar_pagina1()

        # perguntas de fallback (se a integração com Gemini não estiver configurada)
        self.perguntas_simuladas = {
            "Tecnologia": {
                "Junior": ["Você conhece os conceitos básicos de programação?"],
                "Pleno": ["Explique o que é orientação a objetos."],
                "Senior": ["Como você realiza a arquitetura de sistemas escaláveis?"]
            },
            "Saúde": {
                "Junior": ["O que você sabe sobre ética profissional na saúde?"],
                "Pleno": ["Descreva sua experiência com prontuários eletrônicos."],
                "Senior": ["Como liderar equipes multidisciplinares na saúde?"]
            },
            "Administração": {
                "Junior": ["Você tem experiência com rotinas administrativas básicas?"],
                "Pleno": ["Como você organiza seu tempo e tarefas?"],
                "Senior": ["Fale sobre sua habilidade em gerenciar conflitos."]
            },
            "Marketing": {
                "Junior": ["Você conhece técnicas básicas de marketing digital?"],
                "Pleno": ["Como foi sua experiência com campanhas em redes sociais?"],
                "Senior": ["Como definir a estratégia de marketing para um novo produto?"]
            }
        }
        self.indice_pergunta = 0

    def mostrar_pagina1(self):
        self.frame2.pack_forget()
        self.frame_entrevista.pack_forget()
        self.frame1.pack(fill="both", expand=True)

        for widget in self.frame1.winfo_children():
            widget.destroy()

        label_frase = tk.Label(self.frame1, text="Dê o seu primeiro passo para o futuro da sua carreira!",
                               font=("Arial", 16))
        label_frase.pack(pady=100)

        btn_comecar = tk.Button(self.frame1, text="Começar", font=("Arial", 14),
                               command=self.mostrar_pagina2)
        btn_comecar.pack(pady=20)

    def mostrar_pagina2(self):
        self.frame1.pack_forget()
        self.frame_entrevista.pack_forget()
        self.frame2.pack(fill="both", expand=True)

    def iniciar_entrevista(self, area, nivel):
        self.area = area
        self.nivel = nivel
        self.frame2.pack_forget()
        self.frame_entrevista.pack(fill="both", expand=True)
        self.criar_interface_entrevista()
        self.indice_pergunta = 0
        self.exibir_proxima_pergunta()

    def criar_interface_entrevista(self):
        for widget in self.frame_entrevista.winfo_children():
            widget.destroy()

        self.label_titulo = tk.Label(self.frame_entrevista, text="Simulador de Entrevista",
                                     font=("Arial", 16))
        self.label_titulo.pack(pady=10)

        self.label_pergunta = tk.Label(self.frame_entrevista, text="", wraplength=550, font=("Arial", 12))
        self.label_pergunta.pack(pady=20)

        self.entry_resposta = tk.Entry(self.frame_entrevista, width=70)
        self.entry_resposta.pack(pady=10)

        self.btn_enviar_resposta = tk.Button(self.frame_entrevista, text="Enviar Resposta",
                                            command=self.avaliar_resposta)
        self.btn_enviar_resposta.pack(pady=15)

    def exibir_proxima_pergunta(self):
        # tenta gerar pergunta via gemini_api (se estiver disponível), caso contrário usa fallback local
        try:
            from gemini_api import gerar_pergunta
            pergunta = gerar_pergunta(area=self.area, nivel=self.nivel)
            # garantir que sempre teremos texto
            if not pergunta or not pergunta.strip():
                raise Exception("Resposta vazia da API")
            self.pergunta_atual = pergunta
            self.label_pergunta.config(text=f"Pergunta: {self.pergunta_atual}")
        except Exception:
            perguntas = self.perguntas_simuladas.get(self.area, {}).get(self.nivel, [])
            if self.indice_pergunta < len(perguntas):
                self.pergunta_atual = perguntas[self.indice_pergunta]
                self.label_pergunta.config(text=f"Pergunta: {self.pergunta_atual}")
            else:
                self.label_pergunta.config(text="Parabéns! Você completou a simulação.")
                self.entry_resposta.pack_forget()
                self.btn_enviar_resposta.pack_forget()

    def avaliar_resposta(self):
        resposta = self.entry_resposta.get()
        if not resposta.strip():
            messagebox.showerror("Erro", "Por favor, escreva uma resposta para continuar.")
            return

        # Tenta usar feedback do gemini_api (se disponível)
        try:
            from gemini_api import gerar_feedback
            feedback = gerar_feedback(pergunta=self.pergunta_atual, resposta=resposta)
            if not feedback:
                raise Exception("Feedback vazio")
        except Exception:
            feedback = f"Resposta recebida: {resposta}\nContinue para a próxima pergunta."

        messagebox.showinfo("Feedback", feedback)

        # se estivermos usando fallback local, avançamos índice; caso contrário, também avançamos
        self.indice_pergunta += 1
        self.entry_resposta.delete(0, tk.END)
        self.exibir_proxima_pergunta()
