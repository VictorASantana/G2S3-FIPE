import streamlit as st
import datetime
import pandas as pd

from services.brand import get_brands, get_brand_id_by_name
from services.model import get_models, get_model_id_by_name
from services.vehicles import get_vehicles, get_avg_price, get_vehicle_details
from services.prices import get_store_id_by_vehicle_id
from services.store import read_store, get_store_id_by_name
from services.stores_comparison import create_stores_comparison, get_avg_price_by_month_given_vehicle_store

def run_compare_stores():
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