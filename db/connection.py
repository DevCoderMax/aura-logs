import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'logs.db')

def get_connection():
    """Cria uma conexão com o banco de dados SQLite3."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Para retornar resultados como dicionários
    return conn

def execute_query(query, params=()):
    """Executa uma query no banco de dados e retorna o resultado."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    result = cursor.lastrowid
    conn.close()
    return result

def fetch_all(query, params=()):
    """Executa uma query de seleção e retorna todos os resultados."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return result

def fetch_one(query, params=()):
    """Executa uma query de seleção e retorna o primeiro resultado."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def insert_error(nome, descricao):
    """Insere um novo erro no banco de dados e retorna o ID."""
    data_insercao = datetime.now().isoformat()
    query = "INSERT INTO stp_table (nome, descricao, data_insercao) VALUES (?, ?, ?)"
    return execute_query(query, (nome, descricao, data_insercao))

def get_all_errors():
    """Retorna todos os erros do banco de dados."""
    query = "SELECT * FROM stp_table ORDER BY id DESC"
    return fetch_all(query)

def get_error_by_id(error_id):
    """Retorna um erro específico pelo ID."""
    query = "SELECT * FROM stp_table WHERE id = ?"
    return fetch_one(query, (error_id,))
