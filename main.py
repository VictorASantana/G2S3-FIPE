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
authenticator.login()

if st.session_state["connected"]:
  st.write(f"Bem vindo! {st.session_state['user_info'].get('name')}")
  home, logout = st.columns(2)
  with home:
    if st.session_state['user_info'].get('role') == 'gestor':
      if st.button("Acessar Painel do Gestor", use_container_width=True):
        st.switch_page("pages/manager_page.py")
    elif st.session_state['user_info'].get('role') == 'pesquisador':
      if st.button("Acessar Painel do Pesquisador", use_container_width=True):
        st.switch_page("pages/researcher.py")
  with logout:
    if st.button("Log out", use_container_width=True):
      authenticator.logout()

if authenticator.is_valid == False:
  st.write(f"Escolha um email autenticado! Caso seu email não seja válido, entre em contato com o administrador.")
