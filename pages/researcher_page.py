import streamlit as st
from utils.auth import check_required_role

check_required_role('pesquisador')

st.write("Bem vindo!")
