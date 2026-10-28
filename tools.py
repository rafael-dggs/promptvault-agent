import sqlite3
from database import get_connection


def consultar_prompt(item_id: int) -> dict:
    """
    Consulta o prompt, a resposta e os metadados de um registro.
    Args:
        item_id: ID inteiro positivo do registro.
    Returns:
        Dicionário contendo os dados do registro.
    Raises:
        ValueError: ID inválido ou registro inexistente.
        RuntimeError: Falha no banco de dados.
    """
    if isinstance(item_id, bool) or not isinstance(item_id, int) or item_id <= 0:
        raise ValueError("item_id deve ser um inteiro positivo.")

    try:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM produtos WHERE item_id = ?", (item_id,)
            ).fetchone()
            if row is None:
                raise ValueError(f"Registro {item_id} não encontrado.")
            return dict(row)
    except sqlite3.Error as exc:
        raise RuntimeError("Falha ao consultar o banco.") from exc


def verificar_prompt(item_id: int) -> dict:
    """
    Marca um registro como verificado.
    Args:
        item_id: ID inteiro positivo do registro.
    Returns:
        Dicionário com os dados atualizados.
    Raises:
        ValueError: ID inválido ou registro inexistente.
        RuntimeError: Falha no banco de dados.
    """
    if isinstance(item_id, bool) or not isinstance(item_id, int) or item_id <= 0:
        raise ValueError("item_id deve ser um inteiro positivo.")

    try:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                UPDATE produtos
                SET verificado = 1,
                    atualizado_em = strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
                WHERE item_id = ?
                """,
                (item_id,),
            )
            if cursor.rowcount == 0:
                raise ValueError(f"Registro {item_id} não encontrado.")
            row = conn.execute(
                "SELECT * FROM produtos WHERE item_id = ?", (item_id,)
            ).fetchone()
            return dict(row)
    except sqlite3.Error as exc:
        raise RuntimeError("Falha ao atualizar o banco.") from exc
