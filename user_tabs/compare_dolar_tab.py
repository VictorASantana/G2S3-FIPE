import streamlit as st
import datetime
import pandas as pd
import calendar
import matplotlib.pyplot as plt
from services.brand import get_brands
from services.model import get_models
from services.vehicles import get_vehicles
from services.monthly_dolar import get_dolar_values_between_dates
from services.vehicle_monthly_avg import get_vehicle_avg_prices_between_dates

def run_compare_dolar():

    month_mapping = {
    'January': 'janeiro',
    'February': 'fevereiro',
    'March': 'março',
    'April': 'abril',
    'May': 'maio',
    'June': 'junho',
    'July': 'julho',
    'August': 'agosto',
    'September': 'setembro',
    'October': 'outubro',
    'November': 'novembro',
    'December': 'dezembro'
}
    brands = get_brands()
    brand_options = {name: id for id, name in brands}
    selected_brand = st.selectbox("Selecione a Marca", ["Selecione uma marca"] + list(brand_options.keys()), label_visibility="visible", key = "compare_dolar_brand")
    disable_model = selected_brand == "Selecione a Marca"

    models = []
    model_options = {}
    selected_model = "Selecione um modelo"

    if not disable_model and selected_brand != "Selecione uma marca":
        brand_id = brand_options[selected_brand]
        models = get_models(brand_id)
        model_options = {name: id for id, name in models}
    elif selected_brand == "Selecione uma marca":
        disable_model = True
        disable_vehicle = True
        disable_store = True

    selected_model = st.selectbox("Selecione o Modelo", ["Selecione um modelo"] + list(model_options.keys()), disabled=disable_model, label_visibility="visible", key="compare_dolar_model")
    disable_vehicle = selected_model == "Selecione um modelo"

    vehicles = []
    vehicle_options = {}
    selected_vehicle = "Selecione um veículo"

    if not disable_vehicle:
        model_id = model_options[selected_model]
        vehicles = get_vehicles(model_id)
        vehicle_options = {f"{mod_year}": id for id, mod_year, average_price in vehicles}

    selected_vehicle = st.selectbox("Selecione o Veículo", ["Selecione um veículo"] + list(vehicle_options.keys()), disabled=disable_vehicle, label_visibility="visible", key="compare_dolar_vehicle")
    col3, col4 = st.columns(2)

    with col3:
        start_month = st.selectbox("Mês Inicial", list(calendar.month_name[1:]), label_visibility="visible", key = 'compare_dolar_start_month')
        start_year = st.selectbox("Ano Inicial", list(range(2000, datetime.datetime.now().year + 1)), label_visibility="visible", key = 'compare_dolar_start_year')

    with col4:
        end_month = st.selectbox("Mês Final", list(calendar.month_name[1:]), label_visibility="visible", key = 'compare_dolar_end_month')
        end_year = st.selectbox("Ano Final", list(range(2000, datetime.datetime.now().year + 1)), label_visibility="visible", key = 'compare_dolar_end_year')

    compare_button = st.button("Comparar veículo com Dólar", use_container_width=True)

    if compare_button:
        if selected_vehicle == "Selecione um veículo" :
            st.error("Você precisa selecionar um veículo para comparar!")
        else:
            start_month_num = list(calendar.month_name).index(start_month)
            end_month_num = list(calendar.month_name).index(end_month)
            if (end_year < start_year) or (end_year == start_year and end_month_num < start_month_num):
                st.error("A data final não pode ser anterior à data inicial!")
            else:
                start_month  = month_mapping.get(start_month)
                end_month = month_mapping.get(end_month)

                vehicle_avg_prices = get_vehicle_avg_prices_between_dates(vehicle_options[selected_vehicle],start_year, start_month, end_year, end_month)
                dolar_prices = get_dolar_values_between_dates(start_year, start_month, end_year, end_month)
                if vehicle_avg_prices:
                    df_vehicle = pd.DataFrame(vehicle_avg_prices, columns=['id', 'vehicle_id', 'month', 'year', 'avg_price'])
                    df_dolar = pd.DataFrame(dolar_prices, columns=['id', 'month', 'year', 'dollar_value'])

                    # Meses em ordem correta
                    month_order = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
                                'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']

                    # Ordenando os dados corretamente
                    df_vehicle['month'] = pd.Categorical(df_vehicle['month'], categories=month_order, ordered=True)
                    df_dolar['month'] = pd.Categorical(df_dolar['month'], categories=month_order, ordered=True)

                    df_vehicle = df_vehicle.sort_values(by=['year', 'month'])
                    df_dolar = df_dolar.sort_values(by=['year', 'month'])

                    # Normalizando os valores pelo primeiro mês
                    first_vehicle_price = df_vehicle.iloc[0]['avg_price']
                    first_dollar_price = df_dolar.iloc[0]['dollar_value']

                    df_vehicle['price_variation'] = ((df_vehicle['avg_price'] / first_vehicle_price) - 1) * 100
                    df_dolar['dollar_variation'] = ((df_dolar['dollar_value'] / first_dollar_price) - 1) * 100

                    # Unindo os dois DataFrames pela coluna de tempo (mês e ano)
                    df_merged = pd.merge(df_vehicle, df_dolar, on=['month', 'year'])

                    # Calculando a diferença entre as variações
                    df_merged['diff_variation'] = df_merged['price_variation'] - df_merged['dollar_variation']

                    # Plotando o gráfico
                    fig, ax = plt.subplots(figsize=(12, 6))
                    ax.plot(df_merged['month'].astype(str) + " " + df_merged['year'].astype(str), df_merged['price_variation'], label="Variação Preço Veículo (%)", marker='o')
                    ax.plot(df_merged['month'].astype(str) + " " + df_merged['year'].astype(str), df_merged['dollar_variation'], label="Variação Dólar (%)", marker='s')
                    ax.plot(df_merged['month'].astype(str) + " " + df_merged['year'].astype(str), df_merged['diff_variation'], label="Diferença (%)", marker='d', linestyle='dashed')

                    ax.axhline(0, color='black', linewidth=0.8, linestyle="--")
                    ax.set_xticklabels(df_merged['month'].astype(str) + " " + df_merged['year'].astype(str), rotation=45)
                    ax.set_xlabel("Mês/Ano")
                    ax.set_ylabel("Variação (%)")
                    ax.set_title("Variação do Preço do Veículo vs Dólar ao longo do Tempo")
                    ax.legend()
                    ax.grid(True)

                    # Exibir o gráfico no Streamlit
                    st.pyplot(fig)
                else: 
                    st.error("Não há preços cadastrados para o veículo no período selecionado")