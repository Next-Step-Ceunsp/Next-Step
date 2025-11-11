# splash.py
import tkinter as tk

class SplashScreen(tk.Frame):
    def __init__(self, master, callback_on_close, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.callback_on_close = callback_on_close
        self.config(bg="#18776e")

        # Título principal
        tk.Label(
            self,
            text="NextStep",
            font=("Arial", 28, "bold"),
            bg="#18776e",
            fg="white"
        ).pack(expand=True)

        # Subtítulo
        tk.Label(
            self,
            text="Simulador de Entrevistas",
            font=("Arial", 14),
            bg="#18776e",
            fg="#d1fff4"
        ).pack()

        # Animação simples (pontos piscando)
        self.pontos = tk.Label(self, text="", font=("Arial", 16), bg="#18776e", fg="white")
        self.pontos.pack(pady=20)

        self.animar_pontos()
        # Fecha splash depois de 2,5 segundos e chama a próxima tela
        self.after(2500, self.fechar_splash)

    def animar_pontos(self):
        atual = self.pontos.cget("text")
        if len(atual) < 3:
            self.pontos.config(text=atual + ".")
        else:
            self.pontos.config(text="")
        self.after(500, self.animar_pontos)

    def fechar_splash(self):
        self.pack_forget()
        self.callback_on_close()
