import sqlite3
from hashlib import sha256

def conectar():
    return sqlite3.connect("nextstep.db")

def criar_tabelas():
    conn = conectar()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS entrevistas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        area TEXT,
        nivel TEXT,
        pergunta TEXT,
        resposta TEXT,
        feedback TEXT,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )''')

    conn.commit()
    conn.close()

def registrar_usuario(nome, email, senha):
    conn = conectar()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                  (nome, email, sha256(senha.encode()).hexdigest()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def autenticar_usuario(email, senha):
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT id, nome FROM usuarios WHERE email=? AND senha=?", 
              (email, sha256(senha.encode()).hexdigest()))
    usuario = c.fetchone()
    conn.close()
    return usuario

def salvar_entrevista(usuario_id, area, nivel, pergunta, resposta, feedback):
    conn = conectar()
    c = conn.cursor()
    c.execute("INSERT INTO entrevistas (usuario_id, area, nivel, pergunta, resposta, feedback) VALUES (?, ?, ?, ?, ?, ?)",
              (usuario_id, area, nivel, pergunta, resposta, feedback))
    conn.commit()
    conn.close()

def listar_entrevistas(usuario_id):
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT area, nivel, pergunta, resposta, feedback FROM entrevistas WHERE usuario_id=?", (usuario_id,))
    entrevistas = c.fetchall()
    conn.close()
    return entrevistas
