import psycopg2
import streamlit as st
from database_connection import create_connection, table_exists

def create_brand_table():
    if not table_exists("brand"):
        conn = create_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS brand (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            );
        """)
        
        conn.commit()
        conn.commit()
        cur.close()
        conn.close()
        
        print("Tabela 'brand' criada com sucesso.")
    else: 
        print("Tabela 'brand' já existe.")

def get_brands():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM brand;")
    brands = cursor.fetchall()
    conn.close()
    return brands