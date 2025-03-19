import streamlit as st
import sys
import os
import datetime
import pandas as pd
import calendar
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.brand import get_brands, get_brand_id_by_name
from services.model import get_models, get_model_id_by_name
from services.vehicles import get_vehicles, get_avg_price, get_vehicle_details
from services.vehicle_monthly_avg import get_vehicle_monthly_avg
from services.prices import get_store_id_by_vehicle_id
from services.store import read_store, get_store_id_by_name
from services.stores_comparison import create_stores_comparison, get_avg_price_by_month_given_vehicle_store
from services.vehicle_monthly_query import create_vehicle_monthly_query
from services.vehicle_monthly_query import get_queries_by_user

from user_tabs.compare_stores_tab import run_compare_stores
from user_tabs.compare_dolar_tab import run_compare_dolar 

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
    st.header("Comparar dois veículos")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Veículo 1")
        brand1 = st.selectbox("Selecione a Marca", ["Selecione uma marca"] + list(brand_options.keys()), label_visibility="visible", key="brand1")
        disable_model1 = brand1 == "Selecione uma marca"
        disable_vehicle1 = True

        models1 = []
        model_options1 = {}
        selected_model1 = "Selecione um modelo"

        if not disable_model1:
            brand_id1 = brand_options[brand1]
            models1 = get_models(brand_id1)
            model_options1 = {name: id for id, name in models1}

        selected_model1 = st.selectbox("Selecione o Modelo", ["Selecione um modelo"] + list(model_options1.keys()), disabled=disable_model1, label_visibility="visible", key="model1")
        disable_vehicle1 = selected_model1 == "Selecione um modelo"

        vehicles1 = []
        vehicle_options1 = {}
        selected_vehicle1 = "Selecione um veículo"

        if not disable_vehicle1:
            model_id1 = model_options1[selected_model1]
            vehicles1 = get_vehicles(model_id1)
            vehicle_options1 = {f"{mod_year}": id for id, mod_year, average_price in vehicles1}

        selected_vehicle1 = st.selectbox("Selecione o Veículo", ["Selecione um veículo"] + list(vehicle_options1.keys()), disabled=disable_vehicle1, label_visibility="visible", key="vehicle1")

    with col2:
        st.subheader("Veículo 2")
        brand2 = st.selectbox("Selecione a Marca", ["Selecione uma marca"] + list(brand_options.keys()), label_visibility="visible", key="brand2")
        disable_model2 = brand2 == "Selecione uma marca"
        disable_vehicle2 = True

        models2 = []
        model_options2 = {}
        selected_model2 = "Selecione um modelo"

        if not disable_model2:
            brand_id2 = brand_options[brand2]
            models2 = get_models(brand_id2)
            model_options2 = {name: id for id, name in models2}

        selected_model2 = st.selectbox("Selecione o Modelo", ["Selecione um modelo"] + list(model_options2.keys()), disabled=disable_model2, label_visibility="visible", key="model2")
        disable_vehicle2 = selected_model2 == "Selecione um modelo"

        vehicles2 = []
        vehicle_options2 = {}
        selected_vehicle2 = "Selecione um veículo"

        if not disable_vehicle2:
            model_id2 = model_options2[selected_model2]
            vehicles2 = get_vehicles(model_id2)
            vehicle_options2 = {f"{mod_year}": id for id, mod_year, average_price in vehicles2}

        selected_vehicle2 = st.selectbox("Selecione o Veículo", ["Selecione um veículo"] + list(vehicle_options2.keys()), disabled=disable_vehicle2, label_visibility="visible", key="vehicle2")


    col3, col4 = st.columns(2)

    with col3:
        start_month = st.selectbox("Mês Inicial", list(calendar.month_name[1:]), label_visibility="visible")
        start_year = st.selectbox("Ano Inicial", list(range(2000, datetime.datetime.now().year + 1)), label_visibility="visible")

    with col4:
        end_month = st.selectbox("Mês Final", list(calendar.month_name[1:]), label_visibility="visible")
        end_year = st.selectbox("Ano Final", list(range(2000, datetime.datetime.now().year + 1)), label_visibility="visible")

    compare_button = st.button("Comparar veículos", use_container_width=True)

    if compare_button:
        if selected_vehicle1 == "Selecione um veículo" or selected_vehicle2 == "Selecione um veículo":
            st.error("Você precisa selecionar ambos os veículos para comparar!")
        else:
            start_month_num = list(calendar.month_name).index(start_month)
            end_month_num = list(calendar.month_name).index(end_month)
            if (end_year < start_year) or (end_year == start_year and end_month_num < start_month_num):
                st.error("A data final não pode ser anterior à data inicial!")
            else:
                def generate_months(start_month, start_year, end_month, end_year):
                    months = []
                    current_month = start_month
                    current_year = start_year

                    while current_year < end_year or (current_year == end_year and current_month <= end_month):
                        months.append((current_month, current_year))
                        current_month += 1
                        if current_month > 12:
                            current_month = 1
                            current_year += 1

                    return months

                start_month_num = list(calendar.month_name).index(start_month)
                end_month_num = list(calendar.month_name).index(end_month)

                months_years = generate_months(start_month_num, start_year, end_month_num, end_year)

                vehicle1_avg_prices = get_vehicle_monthly_avg(vehicle_id=vehicle_options1[selected_vehicle1])
                vehicle2_avg_prices = get_vehicle_monthly_avg(vehicle_id=vehicle_options2[selected_vehicle2])

                data_vehicle1 = []
                data_vehicle2 = []

                for month_num, year_num in months_years:
                    vehicle1_data = next((item for item in vehicle1_avg_prices if item[1] == month_num and item[2] == year_num), None)
                    vehicle2_data = next((item for item in vehicle2_avg_prices if item[1] == month_num and item[2] == year_num), None)

                    data_vehicle1.append(vehicle1_data[3] if vehicle1_data else None)
                    data_vehicle2.append(vehicle2_data[3] if vehicle2_data else None)

                df_comparison = pd.DataFrame({
                    "Mês/Ano": [f"{calendar.month_name[m]} {y}" for m, y in months_years],
                    f"{selected_model1} ({brand1})": data_vehicle1,
                    f"{selected_model2} ({brand2})": data_vehicle2
                })

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader(f"{brand1} {selected_model1} {selected_vehicle1} - Preço Médio Mês a Mês")
                    st.dataframe(df_comparison[["Mês/Ano", f"{selected_model1} ({brand1})"]], use_container_width=True, hide_index=True)

                with col2:
                    st.subheader(f"{brand2} {selected_model2} {selected_vehicle2} - Preço Médio Mês a Mês")
                    st.dataframe(df_comparison[["Mês/Ano", f"{selected_model2} ({brand2})"]], use_container_width=True, hide_index=True)
                
                fig, ax = plt.subplots(figsize=(10, 5))

                ax.plot(df_comparison["Mês/Ano"], df_comparison[f"{selected_model1} ({brand1})"], marker='o', linestyle='-', label=f"{selected_model1} ({brand1})")
                ax.plot(df_comparison["Mês/Ano"], df_comparison[f"{selected_model2} ({brand2})"], marker='s', linestyle='-', label=f"{selected_model2} ({brand2})")

                ax.set_xlabel("Mês/Ano")
                ax.set_ylabel("Preço Médio (R$)")
                ax.set_title("Comparação de Preços Médios Mensais")
                ax.legend()
                ax.grid(True)
                plt.xticks(rotation=45)

                st.pyplot(fig)

                query_data = {
                "vehicle1_id": vehicle_options1[selected_vehicle1],
                "vehicle2_id": vehicle_options2[selected_vehicle2],
                "user_id": 1,  #ID do usuário logado aqui
                "start_month": start_month_num,
                "end_month": end_month_num,
                "start_year": start_year,
                "end_year": end_year
            }

                query_id = create_vehicle_monthly_query(query_data)

with tabs[4]:
    st.write("Diferença entre dois veículos - Em construção")

with tabs[5]:
    st.write("Preços futuros - Em construção")

with tabs[6]:
    st.subheader("Minhas Consultas Salvas")

    current_user_id = 1
    
    with st.expander("Consulta de comparação com dólar"):
        st.write("insira aqui a função que retorna as consultas salvas")
    
    with st.expander("Consulta de comparação entre duas lojas"):
        st.write("insira aqui a função que retorna as consultas salvas")
    
    with st.expander("Consulta de comparação entre dois veículos"):
        queries = get_queries_by_user(current_user_id)
        
        if queries:
            for query in queries:
                vehicle1 = get_vehicle_details(query[1])
                vehicle2 = get_vehicle_details(query[2])
                
                query_date = query[8]

                formatted_date = query_date.strftime('%d/%m/%Y %H:%M:%S')

                st.subheader(f"Consulta realizada em {formatted_date}")

                st.write(f"**Veículo 1**: {vehicle1['brand']} {vehicle1['model']} ({vehicle1['year']})")
                st.write(f"**Veículo 2**: {vehicle2['brand']} {vehicle2['model']} ({vehicle2['year']})")
                st.write(f"**Mês Inicial**: {query[4]} | **Ano Inicial**: {query[6]}")
                st.write(f"**Mês Final**: {query[5]} | **Ano Final**: {query[6]}")
    
                st.write("---")

        else:
            st.write("Nenhuma consulta encontrada para este tipo.")
    
    with st.expander("Consulta de diferença entre dois veículos"):
        st.write("insira aqui a função que retorna as consultas salvas")
    
    with st.expander("Consulta de preços futuros"):
        st.write("insira aqui a função que retorna as consultas salvas")

st.markdown("<hr style='border: 1px dashed black; width:100%; border-radius: 10px;'>", unsafe_allow_html=True)

st.markdown(
    "<div style='text-align: center;'>Instituto Minerva — Tabela FIPE</div>",
    unsafe_allow_html=True
)
