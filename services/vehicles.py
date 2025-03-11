import psycopg2
import streamlit as st
from database_connection import init_connection

def create_vehicles_table():
    conn = init_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vehicles (
                id SERIAL PRIMARY KEY,
                model_id INTEGER REFERENCES models(id) ON DELETE CASCADE,
                fabrication_year INTEGER NOT NULL,
                model_year INTEGER NOT NULL,
                average_price DECIMAL(10,2)
            );
        """)
        
        conn.commit()
        
        st.success("Tabela 'vehicles' criada com sucesso!")
        
    except psycopg2.Error as e:
        st.error(f"Erro ao criar a tabela 'vehicles': {e}")
    
    finally:
        cur.close()
        conn.close()
