import psycopg2
import streamlit as st
from services.database_connection import create_connection, table_exists

def create_prices_table():
    if not table_exists("prices"):
        conn = create_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS prices (
                id SERIAL PRIMARY KEY,
                vehicle_id INTEGER REFERENCES vehicles(id) ON DELETE CASCADE,
                store_id INTEGER REFERENCES store(id) ON DELETE CASCADE,
                price DECIMAL(10, 2) NOT NULL,
                collect_date TIMESTAMP NOT NULL
            );
        """)
        
        conn.commit()
        conn.commit()
        cur.close()
        conn.close()
        
        print("Tabela 'prices' criada com sucesso.")
    else: 
        print("Tabela 'prices' já existe.")
