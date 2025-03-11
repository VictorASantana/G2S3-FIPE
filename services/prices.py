import psycopg2
import streamlit as st
from database_connection import init_connection

def create_prices_table():
    conn = init_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS prices (
                id SERIAL PRIMARY KEY,
                vehicle_id INTEGER REFERENCES vehicles(id) ON DELETE CASCADE,
                store_id INTEGER REFERENCES stores(id) ON DELETE CASCADE,
                price DECIMAL(10, 2) NOT NULL,
                collect_date TIMESTAMP NOT NULL
            );
        """)
        
        conn.commit()
        
        st.success("Tabela 'prices' criada com sucesso!")
        
    except psycopg2.Error as e:
        st.error(f"Erro ao criar a tabela 'prices': {e}")
    
    finally:
        cur.close()
        conn.close()
