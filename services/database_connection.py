import psycopg2
import streamlit as st

DB_CONFIG = {
    "dbname": st.secrets["postgresql"]["DB_NAME"],
    "user": st.secrets["postgresql"]["DB_USER"],
    "password": st.secrets["postgresql"]["DB_PASSWORD"],
    "host": st.secrets["postgresql"]["DB_HOST"],
    "port": st.secrets["postgresql"]["DB_PORT"]
}

def create_connection():
    try:
        conn = psycopg2.connect(
            dbname=DB_CONFIG["dbname"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"]
        )
        return conn
    except Exception as e:
        st.error(f"Erro ao conectar com o banco de dados: {e}")
        return None
    
def execute_query(query, params=None):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()  # Confirma a execução da query
            return cursor
        except Exception as e:
            st.error(f"Erro ao executar a query: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
