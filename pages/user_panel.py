import streamlit as st
import sys
import os
import datetime
import pandas as pd
import calendar
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.brand import get_brands, get_brand_id_by_name
from services.model import get_models, get_model_id_by_name
from services.vehicles import get_vehicles, get_avg_price
from services.vehicle_monthly_avg import get_vehicle_monthly_avg
from services.prices import get_store_id_by_vehicle_id
from services.store import read_store, get_store_id_by_name
from services.stores_comparison import create_stores_comparison, get_avg_price_by_month_given_vehicle_store

st.set_page_config(layout="wide")

if "compare_stores_first_store_id" not in st.session_state:
    st.session_state["compare_stores_first_store_id"] = None
if "second_store_id" not in st.session_state:
    st.session_state["compare_stores_second_store_id"] = None
if "compare_stores_vehicle_id" not in st.session_state:
    st.session_state["compare_stores_vehicle_id"] = None
if "compare_stores_start_month" not in st.session_state:
    st.session_state["compare_stores_start_month"] = None
if "compare_stores_start_year" not in st.session_state:
    st.session_state["compare_stores_start_year"] = None
if "compare_stores_end_month" not in st.session_state:
    st.session_state["compare_stores_end_month"] = None
if "compare_stores_end_year" not in st.session_state:
    st.session_state["compare_stores_end_year"] = None

# Título da página
st.title("Seleção de Veículo")

tabs = st.tabs([
    "Consulta de Preços", "Comparação com dólar", "Comparar duas lojas", 
    "Comparar dois veículos", "Diferença dois veículos", "Preços futuros", "Minhas consultas"
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
    st.write("Comparação com o dólar - Em construção")

with tabs[2]:
    st.write("Comparar duas lojas - Em construção")

    brands = get_brands()
    brand_options = {name: id for id, name in brands}
    selected_brand = st.selectbox("Selecione a Marca", ["Selecione uma marca"] + list(brand_options.keys()), label_visibility="visible", key="compare_brands_model")
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

    selected_model = st.selectbox("Selecione o Modelo", ["Selecione um modelo"] + list(model_options.keys()), disabled=disable_model, label_visibility="visible", key="compare_stores_model")
    disable_vehicle = selected_model == "Selecione um modelo"

    vehicles = []
    vehicle_options = {}
    selected_vehicle = "Selecione um veículo"

    if not disable_vehicle:
        model_id = model_options[selected_model]
        vehicles = get_vehicles(model_id)
        vehicle_options = {f"{mod_year}": id for id, mod_year, average_price in vehicles}

    selected_vehicle = st.selectbox("Selecione o Veículo", ["Selecione um veículo"] + list(vehicle_options.keys()), disabled=disable_vehicle, label_visibility="visible", key="compare_vehicle_model")
    disable_store = selected_vehicle == "Selecione um veículo"

    store_options = {}
    if not disable_store:
        vehicle_id = vehicle_options[selected_vehicle]
        st.session_state["compare_stores_vehicle_id"] = vehicle_id
        store_ids = get_store_id_by_vehicle_id(vehicle_id)
        for store_id in store_ids:
            store_info = read_store(store_id)
            store_options[store_info["name"]] = store_id
    
        print(st.session_state["compare_stores_vehicle_id"], store_ids)

    col_loja1, col_loja2 = st.columns(2)
    with col_loja1: 
        first_store = st.selectbox("Selicone uma loja", ["Selecione uma loja"] + list(store_options.keys()), disabled=disable_store, label_visibility="visible", key="selected_first_store")
        first_store_id = get_store_id_by_name(first_store)
        start_date = st.date_input("Data inicial", max_value="today", disabled=disable_store, label_visibility="visible", key="selected_start_date")
        st.session_state["compare_stores_first_store_id"] = first_store_id
        st.session_state["compare_stores_start_month"] = start_date.month
        st.session_state["compare_stores_start_year"] = start_date.year
    with col_loja2: 
        second_store = st.selectbox("Selicone uma loja", ["Selecione uma loja"] + list(store_options.keys()), disabled=disable_store, label_visibility="visible", key="selected_second_store")
        second_store_id = get_store_id_by_name(second_store)
        end_date = st.date_input("Data final", max_value="today", disabled=disable_store, label_visibility="visible", key="selected_end_date")
        st.session_state["compare_stores_second_store_id"] = second_store_id
        st.session_state["compare_stores_end_month"] = end_date.month
        st.session_state["compare_stores_end_year"] = end_date.year

    if st.session_state["compare_stores_first_store_id"] != "Selicone uma loja" and st.session_state["compare_stores_second_store_id"] != "Selicone uma loja":
        disable_compare_store = False
    else:
        disable_compare_store = True
    
    confirm_search = st.button("Comparar lojas", use_container_width=True, disabled=disable_compare_store, key="compare_stores_button")  
    if confirm_search:
        int_to_month = {
                1: 'janeiro', 2: 'fevereiro', 3: 'março', 4: 'abril', 5: 'maio', 6: 'junho',
                7: 'julho', 8: 'agosto', 9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'
            }
        create_stores_comparison("luccagamballi@gmail.com", 
                                st.session_state["compare_stores_first_store_id"], 
                                st.session_state["compare_stores_second_store_id"], 
                                st.session_state["compare_stores_vehicle_id"], 
                                int_to_month[st.session_state["compare_stores_start_month"]], 
                                st.session_state["compare_stores_start_year"],
                                int_to_month[st.session_state["compare_stores_end_month"]],
                                st.session_state["compare_stores_end_year"]
                            )
        first_store_avg = get_avg_price_by_month_given_vehicle_store(st.session_state["compare_stores_vehicle_id"], st.session_state["compare_stores_first_store_id"], int_to_month[st.session_state["compare_stores_start_month"]], st.session_state["compare_stores_start_year"], int_to_month[st.session_state["compare_stores_end_month"]], st.session_state["compare_stores_end_year"])
        second_store_avg = get_avg_price_by_month_given_vehicle_store(st.session_state["compare_stores_vehicle_id"], st.session_state["compare_stores_second_store_id"], int_to_month[st.session_state["compare_stores_start_month"]], st.session_state["compare_stores_start_year"], int_to_month[st.session_state["compare_stores_end_month"]], st.session_state["compare_stores_end_year"])

        months = list(first_store_avg.keys())
        values1 = [float(v) for v in first_store_avg.values()]
        values2 = [float(v) for v in second_store_avg.values()]

        df = pd.DataFrame({
            "Meses": months,
            "Loja 1": values1,
            "Loja 2": values2
        })

        st.title("Preço do veículo em cada loja")
        st.line_chart(df, x="Meses", y=["Loja 1", "Loja 2"])


with tabs[3]:  # Aba "Comparar dois veículos"
    st.header("Comparar dois veículos")

    # Layout em duas colunas para os dois veículos
    col1, col2 = st.columns(2)

    # Seleção do primeiro veículo (coluna 1)
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

    # Seleção do segundo veículo (coluna 2)
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

    # Mês e ano de início
    with col3:
        start_month = st.selectbox("Mês Inicial", list(calendar.month_name[1:]), label_visibility="visible")
        start_year = st.selectbox("Ano Inicial", list(range(2000, datetime.datetime.now().year + 1)), label_visibility="visible")

    # Mês e ano de fim
    with col4:
        end_month = st.selectbox("Mês Final", list(calendar.month_name[1:]), label_visibility="visible")
        end_year = st.selectbox("Ano Final", list(range(2000, datetime.datetime.now().year + 1)), label_visibility="visible")

    # Botão de comparação
    compare_button = st.button("Comparar veículos", use_container_width=True)

    if compare_button:
        def generate_months(start_month, start_year, end_month, end_year):
            months = []
            current_month = start_month
            current_year = start_year

            while current_year < end_year or (current_year == end_year and current_month <= end_month):
                months.append(f"{calendar.month_name[current_month]} {current_year}")
                current_month += 1
                if current_month > 12:
                    current_month = 1
                    current_year += 1

            return months

        # Converter meses para números
        start_month_num = list(calendar.month_name).index(start_month)
        end_month_num = list(calendar.month_name).index(end_month)

        months = generate_months(start_month_num, start_year, end_month_num, end_year)

        # Buscar os dados de preços médios mensais para os dois veículos no intervalo de datas
        vehicle1_avg_prices = get_vehicle_monthly_avg(vehicle_id=vehicle_options1[selected_vehicle1], year=start_year)
        vehicle2_avg_prices = get_vehicle_monthly_avg(vehicle_id=vehicle_options2[selected_vehicle2], year=start_year)

        # Organizar os dados para exibição
        data_vehicle1 = []
        data_vehicle2 = []

        # Ajuste aqui para garantir que estamos pegando as colunas corretamente
        for month in months:
            # Extrair o mês e ano do formato 'Mês Ano'
            month_name, year = month.split()
            month_num = list(calendar.month_name).index(month_name)

            vehicle1_data = next((item for item in vehicle1_avg_prices if item[1] == month_num and item[2] == int(year)), None)
            vehicle2_data = next((item for item in vehicle2_avg_prices if item[1] == month_num and item[2] == int(year)), None)

            data_vehicle1.append(vehicle1_data[3] if vehicle1_data else None)
            data_vehicle2.append(vehicle2_data[3] if vehicle2_data else None)

        df_comparison = pd.DataFrame({
            "Mês/Ano": months,
            f"{selected_model1} ({brand1})": data_vehicle1,
            f"{selected_model2} ({brand2})": data_vehicle2
        })

        # Exibir os dados de comparação
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"{selected_model1} ({brand1}) - Preço Médio Mês a Mês")
            st.dataframe(df_comparison[[ "Mês/Ano", f"{selected_model1} ({brand1})"]], use_container_width=True, hide_index=True)

        with col2:
            st.subheader(f"{selected_model2} ({brand2}) - Preço Médio Mês a Mês")
            st.dataframe(df_comparison[[ "Mês/Ano", f"{selected_model2} ({brand2})"]], use_container_width=True, hide_index=True)


with tabs[4]:
    st.write("Diferença entre dois veículos - Em construção")

with tabs[5]:
    st.write("Preços futuros - Em construção")

with tabs[6]:
    st.write("Minhas consultas - Em construção")

st.markdown("<hr style='border: 1px dashed black; width:100%; border-radius: 10px;'>", unsafe_allow_html=True)

st.markdown(
    "<div style='text-align: center;'>Instituto Minerva — Tabela FIPE</div>",
    unsafe_allow_html=True
)
