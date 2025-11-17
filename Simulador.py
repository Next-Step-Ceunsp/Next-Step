# Simulador.py (Versão Corrigida para o novo fluxo)
import tkinter as tk
from tkinter import Menu, messagebox
import webbrowser
from PIL import Image, ImageTk
import threading
import os
import time

# --- Configuração da API Gemini ---
try:
    import google.generativeai as genai
    
    # 🔑 LOCAL ONDE VOCÊ COLOCA SUA CHAVE 🔑
    genai.configure(api_key="AIzaSyDyTEq7pHvf5icToNet8vCIbYKvvsCPIsc") 
    
    API_DISPONIVEL = True
except Exception:
    API_DISPONIVEL = False


class SimuladorEntrevista(tk.Frame):
    # ADICIONADO: vaga_empresa
    def __init__(self, master, dados_usuario, vaga_empresa, callback_sair, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.callback_sair = callback_sair
        self.config(bg="white")
        
        self.nome_usuario = dados_usuario.get("nome", "Usuário")
        
        # NOVO: Recebe a vaga/empresa na inicialização
        self.vaga_empresa = vaga_empresa
        
        # --- Variáveis de Estado do Simulador ---
        self.entrevista_ativa = False
        self.ia_respondendo = False
        
        # Variáveis da API
        self.api_disponivel = API_DISPONIVEL
        self.model_chat = None # O objeto de chat será criado em iniciar_entrevista

        # (O resto do __init__ continua igual, definindo UI)
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
            tk.Label(self.sidebar, image=self.logo, bg="#145d54").pack(pady=(25, 10))
        except:
            tk.Label(self.sidebar, text="NextStep",
                     font=("Arial", 20, "bold"),
                     fg="white", bg="#145d54").pack(pady=(25, 10))

        # Nome do usuário na sidebar
        tk.Label(self.sidebar, text=f"Bem-vindo(a), {self.nome_usuario}!",
                 font=("Arial", 11, "italic"),
                 fg="#A7E6D1", bg="#145d54").pack(pady=(0, 15))


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
        # Deve voltar para a home para iniciar nova vaga
        nova_item.bind("<Button-1>", lambda e: self.callback_sair())

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
        #  BARRA DE DIGITAÇÃO COMPLETA
        # ================================
        self.input_area = tk.Frame(self, bg="#e9e9e9")
        self.input_area.pack(fill="x", side="bottom")

        self.entry = tk.Entry(
            self.input_area,
            font=("Arial", 16),
        )
        self.entry.pack(
            fill="both",
            expand=True,
            side="left",
            padx=20,
            pady=20,
            ipady=20
        )
        self.entry.bind("<Return>", self.enviar_mensagem)

        try:
            send_img = Image.open("assets/img/send.png").resize((35, 35))
            self.send_icon = ImageTk.PhotoImage(send_img)
        except:
            self.send_icon = None

        self.send_button = tk.Button(
            self.input_area,
            image=self.send_icon,
            bg="#e9e9e9",
            activebackground="#e9e9e9",
            bd=0,
            command=self.enviar_mensagem
        )
        self.send_button.pack(side="right", padx=20, pady=10)
        
        # Inicia o fluxo
        self.iniciar_entrevista()


    # ================================
    #   FLUXO PRINCIPAL
    # ================================
    def iniciar_entrevista(self):
        self.entrevista_ativa = True
        self.limpar_chat() # Limpa o chat, pois está iniciando uma nova entrevista

        if not self.api_disponivel:
            self.adicionar_mensagem_ia(
                "⚠️ **Alerta:** A API Gemini não está configurada. O simulador funcionará em modo 'simulação' básico."
            )
        
        # BLOCO DE INICIALIZAÇÃO AGORA ESTÁ AQUI
        if self.api_disponivel:
            # Instrução do Sistema para definir o papel da IA
            system_instruction = (
                f"Você é um entrevistador de RH altamente profissional e experiente. "
                f"Você está conduzindo uma simulação de entrevista para a vaga de '{self.vaga_empresa}'. "
                f"Faça perguntas realistas e siga o fluxo de uma entrevista, reagindo às respostas do candidato. "
                f"Mantenha o tom formal. Sua primeira pergunta será de 'Quebra-Gelo'."
            )
            
            # 1. Inicia o chat
            self.model_chat = genai.GenerativeModel('gemini-2.5-flash').start_chat()
            
            # 2. Envia a instrução de sistema (Contexto/Regras)
            self.model_chat.send_message(system_instruction)
            
            # 3. Envia a primeira pergunta (e obtém a resposta)
            threading.Thread(target=self._obter_primeira_pergunta, daemon=True).start()
        
        else:
            # Modo Simulação
            resposta_inicial = (
                f"Entendido! Você está se preparando para **{self.vaga_empresa}**.\n\n"
                "Iniciaremos agora o modo de simulação. A primeira pergunta é:\n\n"
                "**'Fale um pouco sobre você e sua experiência profissional.'**"
            )
            self.adicionar_mensagem_ia(resposta_inicial)
            self.entry.focus_set()


    # Função auxiliar para thread para a primeira pergunta
    def _obter_primeira_pergunta(self):
        self.ia_respondendo = True
        try:
            # Mensagem de IA que o usuário vê:
            resposta_ia = self.model_chat.send_message(
                "Pode começar a entrevista com a primeira pergunta para o candidato."
            ).text
        except Exception as e:
            resposta_ia = f"Desculpe, houve um erro ao processar a resposta da IA: {e}"
        finally:
            self.master.after(0, lambda: self.atualizar_interface_apos_ia(resposta_ia))


    def reiniciar_entrevista(self):
        # Este método não é mais necessário, pois a nova entrevista volta para a Home
        pass

    # ================================
    #   ENVIAR E PROCESSAR MENSAGEM
    # ================================
    def enviar_mensagem(self, event=None):
        if self.ia_respondendo:
            messagebox.showwarning("Aguarde", "O entrevistador ainda está processando sua resposta. Por favor, aguarde.")
            return

        texto = self.entry.get().strip()
        if not texto:
            return

        self.entry.delete(0, tk.END)
        self.adicionar_mensagem_usuario(texto)

        # Bloqueia a entrada enquanto a IA responde
        self.ia_respondendo = True
        self.entry.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)

        # Inicia o processamento da IA em uma thread separada
        threading.Thread(target=self.processar_mensagem_ia, args=(texto,), daemon=True).start()


    def processar_mensagem_ia(self, mensagem_usuario):
        resposta_ia = ""
        
        try:
            # Mensagens seguintes: Continua a entrevista
            
            # Verifica se o usuário quer parar
            if "parar" in mensagem_usuario.lower() or "encerrar" in mensagem_usuario.lower():
                self.entrevista_ativa = False
                resposta_ia = "Simulação encerrada! Ótimo trabalho! Para começar uma nova entrevista, clique em 'Nova Entrevista' no menu lateral."
            
            elif self.api_disponivel:
                # Chamada real da API
                resposta_ia = self.model_chat.send_message(mensagem_usuario).text
            
            else:
                # Simulação básica sem API
                time.sleep(1)
                resposta_ia = f"**(Resposta simulada para: '{mensagem_usuario}...')**\n\nPróxima pergunta: Qual é o seu maior desafio nesta área e como você o supera?"

        except Exception as e:
            resposta_ia = f"Desculpe, houve um erro ao processar a resposta da IA: {e}"
            self.entrevista_ativa = False
            
        
        # 3. Atualiza a interface (deve ser chamado na thread principal)
        self.master.after(0, lambda: self.atualizar_interface_apos_ia(resposta_ia))


    def atualizar_interface_apos_ia(self, resposta_ia):
        self.adicionar_mensagem_ia(resposta_ia)

        # Desbloqueia a entrada
        self.ia_respondendo = False
        self.entry.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)
        self.entry.focus_set()
        
        # Rola para o final
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1)

    # (Métodos UTILITY METHODS, menu_usuario, adicionar_mensagem_usuario, adicionar_mensagem_ia, limpar_chat e abrir_historico ficam inalterados)
    # ================================
    #   UTILITY METHODS
    # ================================
    def menu_usuario(self):
        menu = Menu(self.master, tearoff=0)
        menu.add_command(label="Sair", command=self.callback_sair)
        try:
            # Posição ligeiramente diferente para o menu ficar visível
            menu.tk_popup(self.winfo_rootx() + self.winfo_width() - 150,
                          self.winfo_rooty() + 50)
        finally:
            menu.grab_release()

    def adicionar_mensagem_usuario(self, texto):
        frame = tk.Frame(self.chat_frame, bg="white")
        frame.pack(anchor="e", pady=5, padx=10, fill="x")

        # Ajuste para usar frame interno e garantir alinhamento à direita
        bubble_frame = tk.Frame(frame, bg="white")
        bubble_frame.pack(side="right")
        
        bubble = tk.Label(
            bubble_frame,
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

    def adicionar_mensagem_ia(self, texto):
        frame = tk.Frame(self.chat_frame, bg="white")
        frame.pack(anchor="w", pady=5, padx=10, fill="x")

        # Ajuste para usar frame interno e garantir alinhamento à esquerda
        bubble_frame = tk.Frame(frame, bg="white")
        bubble_frame.pack(side="left")

        bubble = tk.Label(
            bubble_frame,
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

    def limpar_chat(self):
        for widget in self.chat_frame.winfo_children():
            widget.destroy()

    def abrir_historico(self):
        self.limpar_chat()
        self.adicionar_mensagem_ia("📂 Aqui aparecerá o histórico de entrevistas (em desenvolvimento).")