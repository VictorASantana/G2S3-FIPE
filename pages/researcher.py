import sys
import os
import streamlit as st
import psycopg2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'services')))

from database_connection import create_connection

def get_stores():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM store;")
    stores = cursor.fetchall()
    conn.close()
    return stores

def get_vehicles():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT v.id, b.name AS brand, m.name AS model, v.fabrication_year, v.model_year, v.average_price
        FROM vehicles v
        JOIN model m ON v.model_id = m.id
        JOIN brand b ON m.brand_id = b.id;
    """)

    vehicles = cursor.fetchall()
    conn.close()
    return vehicles

def save_price(store_id, vehicle_id, price, collect_date):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO prices (store_id, vehicle_id, price, collect_date)
        VALUES (%s, %s, %s, %s);
    """, (store_id, vehicle_id, price, collect_date))
    conn.commit()
    conn.close()

def researcher_panel():
    st.title("Painel do Pesquisador")
    
    stores = get_stores()
    store_options = [store[1] for store in stores]
    store_selected = st.selectbox("Selecione a loja", store_options)
    store_id = stores[store_options.index(store_selected)][0]
    
    vehicles = get_vehicles()
    vehicle_options = [f"{vehicle[1]} {vehicle[2]} ({vehicle[3]} - {vehicle[4]})" for vehicle in vehicles]
    vehicle_selected = st.selectbox("Selecione o veículo", vehicle_options)
    vehicle_id = vehicles[vehicle_options.index(vehicle_selected)][0]

    price = st.number_input("Digite o preço", min_value=0.0, format="%.2f")

    collect_date = st.date_input("Data de coleta")

    if st.button("OK"):
        if price > 0:
            save_price(store_id, vehicle_id, price, collect_date)
            st.success("Preço registrado com sucesso!")
        else:
            st.error("Por favor, insira um preço válido.")

if __name__ == "__main__":
    researcher_panel()