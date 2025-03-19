import streamlit as st
import sys
import os
import datetime
import pandas as pd
import calendar
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.brand import get_brands, get_brand_id_by_name
from services.model import get_models, get_model_id_by_name
from services.vehicles import get_vehicles, get_avg_price, get_vehicle_details
from services.prices import get_store_id_by_vehicle_id
from services.store import read_store, get_store_id_by_name
from services.stores_comparison import create_stores_comparison, get_avg_price_by_month_given_vehicle_store
from services.vehicle_monthly_query import get_queries_by_user

from user_tabs.compare_stores_tab import run_compare_stores
from user_tabs.compare_dolar_tab import run_compare_dolar 
from user_tabs.compare_two_vehicles import run_two_vehicles_compare
from user_tabs.my_queries import run_my_queries

st.set_page_config(layout="wide")

# Título da página
st.title("Consulta de veículos")

tabs = st.tabs([
    "Consulta de Preços", "P6 Comparação com dólar", "P7 Comparar duas lojas", 
    "P8 Comparar dois veículos", "P9 Diferença dois veículos", "P10 Preços futuros", "Minhas consultas"
])

with tabs[0]:
    with st.expander("Consulta de Preços", expanded=False):
        brands = get_brands()
        brand_options = {name: id for id, name in brands}
        selected_brand = st.selectbox("Selecione a Marca", ["Selecione uma marca"] + list(brand_options.keys()), label_visibility="visible")

        # Verifica se a marca foi selecionada para habilitar o dropdown de modelos
        disable_model = selected_brand == "Selecione uma marca"
        disable_vehicle = True  # O dropdown de veículo só será habilitado depois que um modelo for escolhido

        models = []
        model_options = {}
        selected_model = "Selecione um modelo"

        if not disable_model:
            brand_id = brand_options[selected_brand]
            models = get_models(brand_id)
            model_options = {name: id for id, name in models}

        selected_model = st.selectbox(
                "Selecione o Modelo", 
                ["Selecione um modelo"] + list(model_options.keys()), 
                disabled=disable_model,
                label_visibility="visible"
            )

        # Verifica se o modelo foi selecionado para habilitar o dropdown de veículos
        disable_vehicle = selected_model == "Selecione um modelo"

        vehicles = []
        vehicle_options = {}
        selected_vehicle = "Selecione um veículo"

        if not disable_vehicle:
            model_id = model_options[selected_model]
            vehicles = get_vehicles(model_id)
            vehicle_options = {f"{mod_year}": id for id,  mod_year, average_price in vehicles}

        selected_vehicle = st.selectbox(
            "Selecione o Veículo",
            ["Selecione um veículo"] + list(vehicle_options.keys()),
            disabled=disable_vehicle, 
            label_visibility="visible") 

        disable_price = selected_vehicle == "Selecione o Veículo"

        price_search = st.button(
                "Pesquisar preço",
                disabled=disable_vehicle,
                use_container_width=True
            ) 

        if price_search: 
            brand_id = get_brand_id_by_name(selected_brand)
            model_id = get_model_id_by_name(selected_model)
            avg_price = get_avg_price(model_id, selected_vehicle)
            data = {
                "Busca": ["Marca", "Modelo", "Ano modelo", "Data da consulta", "Preço médio"],
                "Resultado": [selected_brand, selected_model, selected_vehicle, 
                            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"R$ {avg_price:,.2f}"]
            }

            df = pd.DataFrame(data)

            def paint_table(row):
                paintings = []
                for col_idx, _ in enumerate(row):
                    if row.name == len(df) - 1: # Última linha -> Preço médio
                        paintings.append('background-color: #09727E; color: white;')
                    else:
                        if col_idx == 0:  
                            paintings.append('background-color: lightgreen; color: black;')
                        else:  
                            paintings.append('background-color: lightblue; color: black;')
                return paintings
                
            styled_df = df.style.apply(paint_table, axis=1)

            st.dataframe(
                styled_df, 
                use_container_width=True, 
                hide_index=True
            )

with tabs[1]:
    run_compare_dolar()
with tabs[2]:
    run_compare_stores()

with tabs[3]:
    run_two_vehicles_compare()

with tabs[4]:
    st.write("Diferença entre dois veículos - Em construção")

with tabs[5]:
    st.write("Preços futuros - Em construção")

with tabs[6]:
    run_my_queries()

st.markdown("<hr style='border: 1px dashed black; width:100%; border-radius: 10px;'>", unsafe_allow_html=True)

st.markdown(
    "<div style='text-align: center;'>Instituto Minerva — Tabela FIPE</div>",
    unsafe_allow_html=True
)