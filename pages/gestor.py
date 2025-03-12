import streamlit as st
import time
from services.store import create_store, read_store, update_store, delete_store
from services.user_register import get_all_user_info

st.set_page_config(
    page_title="Painel do Gestor",
    initial_sidebar_state="collapsed",
    layout="wide"
)

time.sleep(0.1) # small timeout ensure config is applied

# initialize session_state variables
if "user_name" not in st.session_state:
    st.session_state["user_name"] = "Gestor generico"
if "states_tuple" not in st.session_state:
    st.session_state["states_tuple"] = ('AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 
                                        'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 
                                        'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO')
if "new_store_name" not in st.session_state:
    st.session_state["new_store_name"] = None
if "new_store_CNPJ" not in st.session_state:
    st.session_state["new_store_CNPJ"] = "12.345.678/0001-95"
if "new_store_state" not in st.session_state:
    st.session_state["new_store_state"] = "AC"
if "new_store_user_id" not in st.session_state:
    st.session_state["new_store_user_id"] = None

st.title("Painel do Gestor")
st.write(f"Bem vindo! {st.session_state["user_name"]}")

create_col, update_col, delete_col = st.columns(3)

with create_col: #Future improvement -> after clean go back to placeholder
    st.title("Adicione uma loja")

    st.session_state["new_store_name"] = st.text_input("Nome da loja", placeholder="Insira o nome da loja")
    st.session_state["new_store_CNPJ"] = st.text_input("CNPJ", placeholder="Insira o CNPJ da loja")
    st.session_state["new_store_state"] = st.selectbox("Estado", st.session_state["states_tuple"], placeholder="Selecione um estado")

    available_researchers_id = get_all_user_info(info="id")
    available_researchers_name = get_all_user_info(info="user_name")
    new_store_user_name = st.selectbox("Pesquisadores disponíveis", available_researchers_name, placeholder="Selecione um pesquisador")
    id_idx = available_researchers_name.index(new_store_user_name) 
    st.session_state["new_store_user_id"] = available_researchers_id[id_idx]

    confirm_creation_col, clear_creation_col = st.columns(2)
    with confirm_creation_col:
        if st.button("Adicionar loja", use_container_width=True):
            create_store(st.session_state["new_store_user_id"], 
                         st.session_state["new_store_name"], 
                         st.session_state["new_store_state"], 
                         st.session_state["new_store_CNPJ"])
    with clear_creation_col:
        if st.button("Limpar campos", use_container_width=True):
            st.session_state["new_store_name"] = None
            st.session_state["new_store_CNPJ"] = "12.345.678/0001-95"
            st.session_state["new_store_state"] = "AC"
            st.session_state["new_store_user_id"] = None
            st.rerun()

with update_col:
    st.title("Atualize uma loja")
    st.write(f"Bem vindo! {st.session_state["user_name"]}")
with delete_col:
    st.title("Remova uma loja")
    st.write(f"Bem vindo! {st.session_state["user_name"]}")