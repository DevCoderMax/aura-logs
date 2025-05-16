import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'logs.db')

def create_connection():
    """Cria uma conexão com o banco de dados SQLite3."""
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_table():
    """Cria a tabela se ela não existir."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stp_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            data_insercao TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
    print("Tabela criada/verificada com sucesso no banco de dados logs.db.")
