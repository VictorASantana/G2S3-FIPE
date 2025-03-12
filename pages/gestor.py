import streamlit as st
import time
from services.store import create_store, read_store, update_store, delete_store, get_stores, get_all_stores_info
from services.user_register import get_all_user_info
import pandas as pd

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

if "selected_store_id" not in st.session_state:
    st.session_state["selected_store_id"] = None
if "selected_store_name" not in st.session_state:
    st.session_state["selected_store_name"] = None
if "selected_store_CNPJ" not in st.session_state:
    st.session_state["selected_store_CNPJ"] = "12.345.678/0001-95"
if "selected_store_state" not in st.session_state:
    st.session_state["selected_store_state"] = "AC"
if "selected_store_user_id" not in st.session_state:
    st.session_state["selected_store_user_id"] = None

if "updated_store_user_id" not in st.session_state:
    st.session_state["updated_store_user_id"] = None
if "updated_store_name" not in st.session_state:
    st.session_state["updated_store_name"] = None
if "updated_store_state" not in st.session_state:
    st.session_state["updated_store_state"] = None

st.title("Painel do Gestor")
st.write(f"Bem vindo! {st.session_state["user_name"]}")

create_col, stores_col = st.columns(2)

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

with stores_col:
    st.title("Selecione uma loja")
    
    #st.header("Selecione uma loja")
    available_stores_ids = get_all_stores_info(info="id")
    available_researchers_ids = get_all_stores_info(info="user_id")
    available_stores_names = get_all_stores_info(info="name")
    available_stores_state = get_all_stores_info(info="state")
    available_stores_CNPJ = get_all_stores_info(info="CNPJ")
    data = {
        "Id": available_stores_ids,
        "Id Pesquisador": available_researchers_ids,
        "Nome": available_stores_names,
        "Estado": available_stores_state,
        "CNPJ": available_stores_CNPJ
    }
    df = pd.DataFrame(data)

    stores_to_select = st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        height=300
    )

    st.write("Loja selecionada")
    selected_store = stores_to_select.selection.rows
    filtered_df = df.iloc[selected_store]
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
    )

    if len(filtered_df)>0:
        st.session_state["selected_store_id"] = filtered_df["Id"].values[0]
        st.session_state["selected_store_user_id"] = filtered_df["Id Pesquisador"].values[0]
        st.session_state["selected_store_name"] = filtered_df["Nome"].values[0]
        st.session_state["selected_store_CNPJ"] = filtered_df["Estado"].values[0]
        st.session_state["selected_store_state"] = filtered_df["Id"].values[0]


    update_name_col, update_state_col, update_researcher_col = st.columns(3)
    with update_name_col:
        st.session_state["updated_store_name"] = st.text_input("Novo Nome da loja", placeholder="Insira o novo nome da loja")
    with update_state_col:
        st.session_state["updated_store_state"] = st.selectbox("Estado", st.session_state["states_tuple"], placeholder="Selecione um novo estado")
    with update_researcher_col:
        available_researchers_id = get_all_user_info(info="id")
        available_researchers_name = get_all_user_info(info="user_name")
        updated_store_user_name = st.selectbox("Pesquisadores disponíveis", available_researchers_name, placeholder="Selecione um pesquisador", key="updated_store_user_name")
        id_idx = available_researchers_name.index(updated_store_user_name) 
        st.session_state["updated_store_user_id"] = available_researchers_id[id_idx]

    update_col, clear_update_col, delete_col = st.columns(3)
    with update_col:
        update_button = st.button("Atualizar informações", use_container_width=True)
        if update_button and st.session_state["selected_store_id"] is not None:
            update_store(int(st.session_state["selected_store_id"]),
                        st.session_state["updated_store_user_id"], 
                        st.session_state["updated_store_name"], 
                        st.session_state["updated_store_state"]
            )
            st.rerun()
        elif update_button:
            st.write("Selecione uma loja!")

    with clear_update_col:
        cancel_update_button = st.button("Cancelar atualização", use_container_width=True, key="cancel_update_button")
        if cancel_update_button:
            st.rerun()  

    with delete_col:
        remove_store_button = st.button("Remover loja", use_container_width=True, key="remove_store_button")
        if remove_store_button and st.session_state["selected_store_id"] is not None:
            delete_store(int(st.session_state["selected_store_id"]))
            st.rerun()
        elif remove_store_button:
            st.write("Selecione uma loja!")