import streamlit as st
import psycopg2

DB_CONFIG = {
    "dbname": st.secrets["DB_NAME"],
    "user": st.secrets["DB_USER"],
    "password": st.secrets["DB_PASSWORD"],
    "host": st.secrets["DB_HOST"],
    "port": st.secrets["DB_PORT"]
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

def table_exists(table_name):
  conn = create_connection()
  cur = conn.cursor()
  
  cur.execute("""
      SELECT EXISTS (
          SELECT FROM information_schema.tables 
          WHERE table_name = %s
      );
  """, (table_name,))
  
  exists = cur.fetchone()[0]
  
  cur.close()
  conn.close()
  return exists