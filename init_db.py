from database import inicializar_banco, inserir_prompt, get_connection


def main():
    inicializar_banco()

    with get_connection() as conn:
        quantidade = conn.execute(
            "SELECT COUNT(*) FROM produtos"
        ).fetchone()[0]

    if quantidade == 0:
        item_id = inserir_prompt(
            "PromptVault Agent",
            "Explique o que é uma API REST.",
            "Uma API REST permite a comunicação entre sistemas por HTTP.",
        )
        print(f"Registro de teste criado: {item_id}")
    else:
        print("O banco já contém registros; nenhum dado foi inserido.")

    print("Banco inicializado com sucesso.")


if __name__ == "__main__":
    main()
