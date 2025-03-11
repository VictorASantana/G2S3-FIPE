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

def get_brands():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM brand;")
    brands = cursor.fetchall()
    conn.close()
    return brands

def get_models_by_brand(brand_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM model WHERE brand_id = %s;", (brand_id,))
    models = cursor.fetchall()
    conn.close()
    return models

def get_vehicles_by_model(model_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, fabrication_year, model_year, average_price
        FROM vehicles
        WHERE model_id = %s;
    """, (model_id,))
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
    store_options = {"Selecione...": None}
    store_options.update({store[1]: store[0] for store in stores})
    store_selected = st.selectbox("Selecione a loja", list(store_options.keys()))

    if store_selected != "Selecione...":
        store_id = store_options[store_selected]

        brands = get_brands()
        brand_options = {"Selecione...": None}
        brand_options.update({brand[1]: brand[0] for brand in brands})
        brand_selected = st.selectbox("Selecione a marca", list(brand_options.keys()))

        if brand_selected != "Selecione...":
            brand_id = brand_options[brand_selected]

            models = get_models_by_brand(brand_id)
            model_options = {"Selecione...": None}
            model_options.update({model[1]: model[0] for model in models})
            model_selected = st.selectbox("Selecione o modelo", list(model_options.keys()))

            if model_selected != "Selecione...":
                model_id = model_options[model_selected]

                vehicles = get_vehicles_by_model(model_id)
                vehicle_options = {"Selecione...": None}
                vehicle_options.update({f"{v[2]}": v[0] for v in vehicles})
                vehicle_selected = st.selectbox("Selecione o ano do modelo do veículo", list(vehicle_options.keys()))

                if vehicle_selected != "Selecione...":
                    vehicle_id = vehicle_options[vehicle_selected]

                    price = st.number_input("Digite o preço", min_value=0.0, format="%.2f")
                    collect_date = st.date_input("Data de coleta")

                    if st.button("OK"):
                        if 0 < price < 100000000.00:
                            save_price(store_id, vehicle_id, price, collect_date)
                            st.success("Preço registrado com sucesso!")
                        else:
                            st.error("Por favor, insira um preço válido.")

if __name__ == "__main__":
    researcher_panel()