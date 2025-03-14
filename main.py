import os
import streamlit as st
from dotenv import load_dotenv
from utils.auth import Authenticator
from services.create_tables import create_all_tables

load_dotenv()

create_all_tables()

allowed_users = os.getenv("ALLOWED_USERS").split(",")

authenticator = Authenticator(
  allowed_users=allowed_users,
  token_key=os.getenv("TOKEN_KEY"),
  secret_path="client_secret.json",
  redirect_uri="http://localhost:8501",
)
authenticator.check_auth()

auth_col, user_col = st.columns(2)
with auth_col:
  authenticator.login()

  if st.session_state["connected"]:
    home, logout = st.columns(2)
    with home:
      if st.session_state['user_info'].get('role') == 'gestor':
        if st.button("Painel do Gestor", use_container_width=True):
          st.switch_page("pages/manager_page.py")
      elif st.session_state['user_info'].get('role') == 'pesquisador':
        if st.button("Painel do Pesquisador", use_container_width=True):
          st.switch_page("pages/researcher.py")
    with logout:
      if st.button("Log out", use_container_width=True):
        authenticator.logout()

  if authenticator.is_valid == False:
    st.write(f"Escolha um email autenticado! Caso seu email não seja válido, entre em contato com o administrador.")

with user_col:
  if st.button("Consultar preços", use_container_width=True):
      st.switch_page("pages/user_panel.py")

if st.session_state["connected"]:
  st.divider()
  st.title(f"Bem vindo! {st.session_state['user_info'].get('name')}")
