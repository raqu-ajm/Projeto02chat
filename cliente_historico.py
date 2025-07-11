#(cliente com banco SQLite local)
import sqlite3
from datetime import datetime

# Criação do banco de dados e tabela
conn = sqlite3.connect("historico_conversa.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS mensagens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        remetente TEXT,
        destinatario TEXT,
        mensagem TEXT,
        timestamp TEXT
    )
''')
conn.commit()

# Função para salvar uma mensagem
def salvar_mensagem(remetente, destinatario, mensagem):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO mensagens (remetente, destinatario, mensagem, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (remetente, destinatario, mensagem, timestamp))
    conn.commit()
    print(f"Mensagem salva: [{timestamp}] {remetente} -> {destinatario}: {mensagem}")

# Função para recuperar histórico com alguém
def carregar_historico(contato):
    cursor.execute('''
        SELECT remetente, mensagem, timestamp FROM mensagens
        WHERE remetente=? OR destinatario=?
        ORDER BY timestamp
    ''', (contato, contato))
    historico = cursor.fetchall()
    print(f"Histórico com {contato}:")
    for r, m, t in historico:
        print(f"[{t}] {r}: {m}")

# Simulação de uso
if __name__ == "__main__":
    salvar_mensagem("alice", "bob", "Oi, tudo bem?")
    salvar_mensagem("bob", "alice", "Tudo ótimo! E você?")
    carregar_historico("alice")
