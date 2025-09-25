# db_sqlite.py
import sqlite3
from typing import List, Tuple, Optional

DB_FILE = "dados.sqlite"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS estados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cidades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        estado_id INTEGER NOT NULL,
        FOREIGN KEY (estado_id) REFERENCES estados(id),
        UNIQUE(nome, estado_id)
    );
    """)
    conn.commit()
    conn.close()

def insert_estado(nome: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO estados (nome) VALUES (?)", (nome,))
    conn.commit()
    cur.execute("SELECT id FROM estados WHERE nome = ?", (nome,))
    row = cur.fetchone()
    conn.close()
    return row["id"] if row else -1

def list_estados() -> List[Tuple[int, str]]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome FROM estados ORDER BY nome")
    rows = cur.fetchall()
    conn.close()
    return [(r["id"], r["nome"]) for r in rows]

def insert_cidade(nome: str, estado_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO cidades (nome, estado_id) VALUES (?, ?)", (nome, estado_id))
    conn.commit()
    cur.execute("SELECT id FROM cidades WHERE nome = ? AND estado_id = ?", (nome, estado_id))
    row = cur.fetchone()
    conn.close()
    return row["id"] if row else -1

def list_cidades_by_estado(estado_id: int) -> List[Tuple[int, str]]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome FROM cidades WHERE estado_id = ? ORDER BY nome", (estado_id,))
    rows = cur.fetchall()
    conn.close()
    return [(r["id"], r["nome"]) for r in rows]

def get_cidade_by_id(cidade_id: int) -> Optional[sqlite3.Row]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, estado_id FROM cidades WHERE id = ?", (cidade_id,))
    row = cur.fetchone()
    conn.close()
    return row

if __name__ == "__main__":
    create_tables()
    print("Tabelas SQLite criadas (ou já existentes)")
