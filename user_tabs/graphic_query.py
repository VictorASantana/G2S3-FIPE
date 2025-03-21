import streamlit as st
import matplotlib.pyplot as plt
import calendar
import datetime
import pandas as pd

from services.brand import get_brands
from services.model import get_models
from services.vehicles import get_vehicles
from services.vehicle_monthly_avg import get_vehicle_monthly_avg

def run_graphic_query():
    st.header("Consulta Gráfica de Veículos")

    # Dividir a tela em colunas para a seleção de veículos
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Veículo 1")
        brands = get_brands()
        brand_options = {name: id for id, name in brands}

        brand1 = st.selectbox(
            "Selecione a Marca", 
            ["Selecione uma marca"] + list(brand_options.keys()), 
            key="brand1_selectbox"
        )
        disable_model1 = brand1 == "Selecione uma marca"

        models1 = get_models(brand_options[brand1]) if not disable_model1 else []
        model_options1 = {name: id for id, name in models1}

        selected_model1 = st.selectbox(
            "Selecione o Modelo", 
            ["Selecione um modelo"] + list(model_options1.keys()), 
            key="model1_selectbox", 
            disabled=disable_model1
        )
        disable_vehicle1 = selected_model1 == "Selecione um modelo"

        vehicles1 = get_vehicles(model_options1[selected_model1]) if not disable_vehicle1 else []
        vehicle_options1 = {f"{mod_year}": id for id, mod_year, avg_price in vehicles1}

        selected_vehicle1 = st.selectbox(
            "Selecione o Veículo", 
            ["Selecione um veículo"] + list(vehicle_options1.keys()), 
            key="vehicle1_selectbox", 
            disabled=disable_vehicle1
        )

    with col2:
        st.subheader("Veículo 2")
        brand2 = st.selectbox(
            "Selecione a Marca", 
            ["Selecione uma marca"] + list(brand_options.keys()), 
            key="brand2_selectbox"
        )
        disable_model2 = brand2 == "Selecione uma marca"

        models2 = get_models(brand_options[brand2]) if not disable_model2 else []
        model_options2 = {name: id for id, name in models2}

        selected_model2 = st.selectbox(
            "Selecione o Modelo", 
            ["Selecione um modelo"] + list(model_options2.keys()), 
            key="model2_selectbox", 
            disabled=disable_model2
        )
        disable_vehicle2 = selected_model2 == "Selecione um modelo"

        vehicles2 = get_vehicles(model_options2[selected_model2]) if not disable_vehicle2 else []
        vehicle_options2 = {f"{mod_year}": id for id, mod_year, avg_price in vehicles2}

        selected_vehicle2 = st.selectbox(
            "Selecione o Veículo", 
            ["Selecione um veículo"] + list(vehicle_options2.keys()), 
            key="vehicle2_selectbox", 
            disabled=disable_vehicle2
        )

    # Seleção de período
    st.subheader("Selecione o Período")
    col3, col4 = st.columns(2)

    with col3:
        start_month = st.selectbox(
            "Mês Inicial", 
            list(calendar.month_name[1:]), 
            key="start_month_selectbox"
        )
        start_year = st.selectbox(
            "Ano Inicial", 
            list(range(2000, datetime.datetime.now().year + 1)), 
            key="start_year_selectbox"
        )

    with col4:
        end_month = st.selectbox(
            "Mês Final", 
            list(calendar.month_name[1:]), 
            key="end_month_selectbox"
        )
        end_year = st.selectbox(
            "Ano Final", 
            list(range(2000, datetime.datetime.now().year + 1)), 
            key="end_year_selectbox"
        )

    compare_button = st.button("Comparar veículos", key="compare_button")

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

                months_years = generate_months(start_month_num, start_year, end_month_num, end_year)

                vehicle1_avg_prices = get_vehicle_monthly_avg(vehicle_id=vehicle_options1[selected_vehicle1])
                vehicle2_avg_prices = get_vehicle_monthly_avg(vehicle_id=vehicle_options2[selected_vehicle2])

                data_vehicle1 = []
                data_vehicle2 = []
                price_differences = []

                for month_num, year_num in months_years:
                    vehicle1_data = next((item for item in vehicle1_avg_prices if item[1] == month_num and item[2] == year_num), None)
                    vehicle2_data = next((item for item in vehicle2_avg_prices if item[1] == month_num and item[2] == year_num), None)

                    price1 = vehicle1_data[3] if vehicle1_data else 0.00  # Substituir None por 0.00
                    price2 = vehicle2_data[3] if vehicle2_data else 0.00  # Substituir None por 0.00

                    data_vehicle1.append(price1)
                    data_vehicle2.append(price2)
                    price_differences.append(price1 - price2)

                # Criar DataFrame com foco na diferença de preço
                df_comparison = pd.DataFrame({
                    "Mês/Ano": [f"{calendar.month_name[m]} {y}" for m, y in months_years],
                    f"{selected_model1} ({brand1})": data_vehicle1,
                    f"{selected_model2} ({brand2})": data_vehicle2,
                    "Diferença de Preço (R$)": price_differences
                })

                # Exibir tabela e gráfico lado a lado
                col_table, col_graph = st.columns([1, 2])  # Tabela ocupa 1/3, gráfico ocupa 2/3

                with col_table:
                    st.subheader("Diferença entre as Cotações Médias Mensais")
                    st.dataframe(df_comparison, use_container_width=True, hide_index=True)

                with col_graph:
                    st.subheader("Gráfico de Diferença de Preços")
                    fig, ax = plt.subplots(figsize=(10, 5))

                    # Plotar as linhas de preço dos veículos
                    ax.plot(df_comparison["Mês/Ano"], df_comparison[f"{selected_model1} ({brand1})"], marker='o', linestyle='-', color='blue', label=f"{selected_model1} ({brand1})")
                    ax.plot(df_comparison["Mês/Ano"], df_comparison[f"{selected_model2} ({brand2})"], marker='o', linestyle='-', color='green', label=f"{selected_model2} ({brand2})")

                    # Plotar a diferença de preço
                    ax.plot(df_comparison["Mês/Ano"], df_comparison["Diferença de Preço (R$)"], marker='o', linestyle='-', color='red', label="Diferença de Preço (R$)")

                    # Configurações do gráfico
                    ax.set_xlabel("Mês/Ano")
                    ax.set_ylabel("Preço (R$)")
                    ax.set_title("Comparação de Preços Mensais")
                    ax.legend()
                    ax.grid(True)
                    plt.xticks(rotation=45)

                    st.pyplot(fig)