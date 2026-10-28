import os
import sqlite3
from pathlib import Path
from contextlib import contextmanager

DEFAULT_DB = Path(__file__).parent / "data" / "seu_tema.db"
DB_PATH = Path(os.getenv("DB_PATH", str(DEFAULT_DB)))


@contextmanager
def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), timeout=30)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA busy_timeout = 30000")
        conn.execute("PRAGMA foreign_keys = ON")
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def inicializar_banco():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                agente TEXT NOT NULL,
                prompt TEXT NOT NULL,
                saida TEXT,
                criado_em TEXT NOT NULL DEFAULT
                    (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
                atualizado_em TEXT NOT NULL DEFAULT
                    (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
                verificado INTEGER NOT NULL DEFAULT 0
                    CHECK (verificado IN (0, 1))
            )
        """)


def inserir_prompt(agente, prompt, saida=None):
    if not agente.strip() or not prompt.strip():
        raise ValueError("Agente e prompt são obrigatórios.")

    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO produtos (agente, prompt, saida) VALUES (?, ?, ?)",
            (agente.strip(), prompt.strip(), saida),
        )
        return cursor.lastrowid


def listar_prompts(limite=100):
    limite = max(1, min(int(limite), 500))
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM produtos ORDER BY item_id DESC LIMIT ?",
            (limite,),
        ).fetchall()
        return [dict(row) for row in rows]
