import streamlit as st
from utils.auth import check_required_role
from services.user_register import get_all_users, update_user, delete_user, create_user

check_required_role('gestor')

st.title("Painel de Usuários")
if st.button("Voltar"):
  st.switch_page("main.py")

if "editing_user_id" not in st.session_state:
  st.session_state.editing_user_id = None
if "creating_user" not in st.session_state:
  st.session_state.creating_user = False

#Painel de usuários
users = get_all_users()

def styled_header_left(text: str):
    st.markdown(
        f"""
        <div style="
            background-color: rgba(240, 240, 240, 0.1);
            padding: 0.75rem 1rem;
            border-top-left-radius: 8px;
            font-weight: bold;
            color: inherit;
            height: 80px;
            margin-bottom: 20px;
            margin-top: 20px;
        ">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )

def styled_header_right(text: str):
  st.markdown(
        f"""
        <div style="
            background-color: rgba(240, 240, 240, 0.1);
            padding: 0.75rem 1rem;
            border-top-right-radius: 8px;
            font-weight: bold;
            color: inherit;
            height: 80px;
            margin-bottom: 20px;
            margin-top: 20px;
        ">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )

def styled_header(text: str):
  st.markdown(
        f"""
        <div style="
            background-color: rgba(240, 240, 240, 0.1);
            padding: 0.75rem 1rem;
            font-weight: bold;
            color: inherit;
            height: 80px;
            margin-bottom: 20px;
            margin-top: 20px;
        ">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()
st.subheader("Usuários Cadastrados: ")

header1, header2, header3, header4, header5 = st.columns([3, 3, 3, 2, 2])
with header1:
  styled_header_left("Nome do Usuário")
with header2: 
  styled_header("Email")
with header3:
  styled_header_right("Papel")

for row in users:
  col1, col2, col3, col4, col5 = st.columns([3, 3, 3, 2, 2])

  with col1:
    st.write(row["name"])
  with col2:
    st.write(row["email"])
  with col3:
    st.write(row["role"])
  with col4:
    if st.button("Editar", key=f"edit_{row['id']}"):
      st.session_state.editing_user_id = row['id']
    with col5:
      if st.button("Excluir", key=f"delete_{row['id']}"):
        delete_user(row["id"])
        st.warning("Usuário excluído!")

  if st.session_state.editing_user_id == row['id']:
    with st.form(f"form_edit_{row['id']}", clear_on_submit=False):
      new_name = st.text_input("Nome", value=row["name"])
      new_email = st.text_input("Email", value=row["email"])
      new_role = st.selectbox("Role", ["gestor", "pesquisador"])
      form_col1, form_col2 = st.columns(2)
      with form_col1:
        if st.form_submit_button("Salvar", use_container_width=True):
          update_user(row["id"], new_name, new_email, new_role)
          st.success("Usuário atualizado!")
          st.session_state.editing_user_id = None
      with form_col2:
        if st.form_submit_button("Cancelar", use_container_width=True):
          st.session_state.editing_user_id = None
          st.rerun() 


st.divider()

st.subheader("Cadastro: ")
if st.button("Adicionar novo Usuário"):
  st.session_state.creating_user = True

if st.session_state.creating_user:
  with st.form("Adding user", clear_on_submit=True):
    new_name = st.text_input("Nome")
    new_email = st.text_input("Email")
    new_role = st.selectbox("Role", ["pesquisador", "gestor"])
    form_col1, form_col2 = st.columns(2)
    with form_col1:
      if st.form_submit_button("Criar", use_container_width=True):
        create_user(new_name, new_email, new_role)
        st.success("Usuário Criado com Sucesso!")
        st.session_state.creating_user = False
        st.rerun() 
    with form_col2:
      if st.form_submit_button("Cancelar", use_container_width=True):
        st.session_state.creating_user = False
        st.rerun() 
    