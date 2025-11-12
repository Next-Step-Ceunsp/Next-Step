import tkinter as tk
from tkinter import messagebox, scrolledtext
import google.generativeai as genai
import datetime

# ==============================================
# CONFIGURAÇÃO DA API DO GEMINI
# ==============================================
API_KEY = "AIzaSyAbsTFbP72DHffkCiaz8nVZzE6AkKInqI4"  # 🔒 Substitua pela sua chave real do Google AI Studio

try:
    genai.configure(api_key=API_KEY)
    modelo = genai.GenerativeModel("gemini-1.5-pro-latest")  # ✅ Modelo compatível
except Exception as e:
    messagebox.showerror("Erro", f"Falha ao inicializar o modelo Gemini: {e}")
    modelo = None


# ==============================================
# CLASSE DO SIMULADOR DE ENTREVISTA
# ==============================================
class SimuladorEntrevista(tk.Frame):
    def __init__(self, master, usuario, callback_sair):
        super().__init__(master)
        self.master = master
        self.usuario = usuario
        self.callback_sair = callback_sair
        self.historico = []

        self.pack(fill="both", expand=True)
        self.criar_interface()

    def criar_interface(self):
        self.master.title("NextStep - Simulador de Entrevistas")
        self.master.geometry("900x600")
        self.master.configure(bg="#f5f5f5")

        titulo = tk.Label(self, text=f"Bem-vindo, {self.usuario} 👋", font=("Arial", 22, "bold"), bg="#f5f5f5")
        titulo.pack(pady=15)

        # Caixa de texto da entrevista
        self.texto_entrevista = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=90, height=20, font=("Arial", 11))
        self.texto_entrevista.pack(padx=20, pady=10)

        # Campo de entrada
        self.entrada = tk.Entry(self, width=80, font=("Arial", 12))
        self.entrada.pack(pady=10)

        # Botões principais
        botoes_frame = tk.Frame(self, bg="#f5f5f5")
        botoes_frame.pack(pady=10)

        tk.Button(botoes_frame, text="Gerar Pergunta", command=self.gerar_pergunta,
                  bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
                  relief="ridge", padx=10, pady=5).grid(row=0, column=0, padx=5)

        tk.Button(botoes_frame, text="Enviar Resposta", command=self.enviar_resposta,
                  bg="#2196F3", fg="white", font=("Arial", 11, "bold"),
                  relief="ridge", padx=10, pady=5).grid(row=0, column=1, padx=5)

        tk.Button(botoes_frame, text="Gerar Feedback", command=self.gerar_feedback,
                  bg="#FF9800", fg="white", font=("Arial", 11, "bold"),
                  relief="ridge", padx=10, pady=5).grid(row=0, column=2, padx=5)

        tk.Button(botoes_frame, text="Ver Histórico", command=self.ver_historico,
                  bg="#9C27B0", fg="white", font=("Arial", 11, "bold"),
                  relief="ridge", padx=10, pady=5).grid(row=0, column=3, padx=5)

        tk.Button(botoes_frame, text="Sair", command=self.sair,
                  bg="#F44336", fg="white", font=("Arial", 11, "bold"),
                  relief="ridge", padx=10, pady=5).grid(row=0, column=4, padx=5)

    # ===========================================================
    # Funções principais
    # ===========================================================
    def gerar_pergunta(self):
        """Gera uma nova pergunta de entrevista usando o Gemini"""
        if not modelo:
            messagebox.showerror("Erro", "O modelo Gemini não foi inicializado corretamente.")
            return

        try:
            resposta = modelo.generate_content("Gere uma pergunta de entrevista de emprego realista e profissional.")
            pergunta = resposta.text.strip()
            self.texto_entrevista.insert(tk.END, f"\nPergunta: {pergunta}\n")
            self.texto_entrevista.see(tk.END)
            self.historico.append({"tipo": "pergunta", "conteudo": pergunta})
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar pergunta: {e}")

    def enviar_resposta(self):
        """Envia a resposta do usuário"""
        resposta = self.entrada.get().strip()
        if not resposta:
            messagebox.showwarning("Aviso", "Digite uma resposta antes de enviar.")
            return

        self.texto_entrevista.insert(tk.END, f"Resposta: {resposta}\n")
        self.entrada.delete(0, tk.END)
        self.historico.append({"tipo": "resposta", "conteudo": resposta})

    def gerar_feedback(self):
        """Gera um feedback da entrevista baseado na última resposta"""
        if not modelo:
            messagebox.showerror("Erro", "O modelo Gemini não foi inicializado corretamente.")
            return

        # Pega a última resposta do histórico
        ultima_resposta = next((item["conteudo"] for item in reversed(self.historico) if item["tipo"] == "resposta"), None)

        if not ultima_resposta:
            messagebox.showwarning("Aviso", "Nenhuma resposta encontrada para gerar feedback.")
            return

        try:
            prompt = f"Analise a seguinte resposta de entrevista e forneça um feedback construtivo:\n\n{ultima_resposta}"
            resposta = modelo.generate_content(prompt)
            feedback = resposta.text.strip()
            self.texto_entrevista.insert(tk.END, f"\n💬 Feedback: {feedback}\n")
            self.texto_entrevista.see(tk.END)
            self.historico.append({"tipo": "feedback", "conteudo": feedback})
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao gerar feedback: {e}")

    def ver_historico(self):
        """Mostra o histórico de perguntas e respostas"""
        if not self.historico:
            messagebox.showinfo("Histórico", "Nenhuma entrevista registrada ainda.")
            return

        janela_hist = tk.Toplevel(self)
        janela_hist.title("Histórico de Entrevistas")
        janela_hist.geometry("700x500")
        janela_hist.configure(bg="#fafafa")

        tk.Label(janela_hist, text=f"Histórico de {self.usuario}", font=("Arial", 16, "bold"), bg="#fafafa").pack(pady=10)

        caixa = scrolledtext.ScrolledText(janela_hist, wrap=tk.WORD, width=80, height=25, font=("Arial", 10))
        caixa.pack(padx=10, pady=10)

        for item in self.historico:
            tipo = item["tipo"].capitalize()
            conteudo = item["conteudo"]
            data = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            caixa.insert(tk.END, f"[{data}] {tipo}: {conteudo}\n\n")

        caixa.configure(state="disabled")

    def sair(self):
        """Retorna para a tela de login"""
        resposta = messagebox.askyesno("Sair", "Deseja realmente sair?")
        if resposta:
            self.destroy()
            self.callback_sair()
