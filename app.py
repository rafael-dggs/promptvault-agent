import streamlit as st
from database import inicializar_banco, inserir_prompt, listar_prompts
from tools import consultar_prompt, verificar_prompt
from agent import executar_agente
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="PromptVault Agent", page_icon="🤖")
inicializar_banco()

st.title("🤖 PromptVault Agent")
st.caption("Azure AI Foundry + SQLite")

if "historico" not in st.session_state:
    st.session_state.historico = []
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

with st.sidebar:
    st.header("Ferramentas")
    item_id = st.number_input("ID do registro", min_value=1, step=1)

    if st.button("Consultar registro"):
        try:
            st.json(consultar_prompt(int(item_id)))
        except ValueError as exc:
            st.warning(str(exc))
        except RuntimeError as exc:
            st.error(str(exc))

    if st.button("Verificar registro"):
        try:
            st.json(verificar_prompt(int(item_id)))
        except ValueError as exc:
            st.warning(str(exc))
        except RuntimeError as exc:
            st.error(str(exc))

    st.divider()
    st.subheader("Últimas interações")
    for registro in listar_prompts(20):
        st.markdown(f"**#{registro['item_id']} — {registro['agente']}**")
        st.caption(registro["criado_em"])
        st.write(registro["prompt"][:100])

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

entrada = st.chat_input("Digite sua pergunta...")

if entrada:
    st.session_state.mensagens.append({"role": "user", "content": entrada})
    with st.chat_message("user"):
        st.markdown(entrada)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Consultando o agente..."):
                resposta = executar_agente(
                    entrada, st.session_state.historico
                )
                st.markdown(resposta)

        registro_id = inserir_prompt(
            "PromptVault Agent", entrada, resposta
        )
        st.session_state.historico.extend([
            {"role": "user", "content": entrada},
            {"role": "assistant", "content": resposta},
        ])
        st.session_state.mensagens.append({
            "role": "assistant", "content": resposta
        })
        st.caption(f"Interação salva no registro #{registro_id}")

    except (ValueError, RuntimeError) as exc:
        st.error(f"Não foi possível concluir: {exc}")
    except Exception:
        st.error("Erro inesperado. Consulte os logs da aplicação.")
