import streamlit as st
import datetime
import pandas as pd
import time

from services.brand import get_brands, get_brand_id_by_name
from services.model import get_models, get_model_id_by_name
from services.vehicles import get_vehicles, get_avg_price, get_vehicle_details
from services.prices import get_store_id_by_vehicle_id
from services.store import read_store, get_store_id_by_name
from services.stores_comparison import create_stores_comparison, get_avg_price_by_month_given_vehicle_store, get_all_comparisons, delete_comparison

if "compare_stores_first_store_id" not in st.session_state:
    st.session_state["compare_stores_first_store_id"] = None
if "compare_stores_second_store_id" not in st.session_state:
    st.session_state["compare_stores_second_store_id"] = None
if "compare_stores_first_store_name" not in st.session_state:
    st.session_state["compare_stores_first_store_name"] = "Selecione uma loja"
if "compare_stores_second_store_name" not in st.session_state:
    st.session_state["compare_stores_second_store_name"] = "Selecione uma loja"
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

if "disable_confirm_button" not in st.session_state:
    st.session_state["disable_confirm_button"] = True

if "results_comp" not in st.session_state:
    st.session_state["results_comp"] = None
if "show_results" not in st.session_state:
    st.session_state["show_results"] = None
if "clear_results" not in st.session_state:
    st.session_state["clear_results"] = None

def build_graph(first_store_name, first_store_avg, second_store_name, second_store_avg):

    all_months = sorted(
        set(first_store_avg.keys()) | set(second_store_avg.keys()), 
        key=lambda x: x
    )

    values1 = [float(first_store_avg[month]) if month in first_store_avg else None for month in all_months]
    values2 = [float(second_store_avg[month]) if month in second_store_avg else None for month in all_months]

    df = pd.DataFrame({
        "Meses": all_months,
        first_store_name: values1,
        second_store_name: values2
    })

    st.title("Preço do veículo em cada loja")
    st.line_chart(df, x="Meses", y=[first_store_name, second_store_name])

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
        st.session_state["compare_stores_first_store_name"] = first_store
        st.session_state["compare_stores_first_store_id"] = first_store_id
        st.session_state["compare_stores_start_month"] = start_date.month
        st.session_state["compare_stores_start_year"] = start_date.year
    with col_loja2: 
        second_store = st.selectbox("Selecione uma loja", ["Selecione uma loja"] + list(store_options.keys()), disabled=disable_store, label_visibility="visible", key="selected_second_store")
        second_store_id = get_store_id_by_name(second_store)
        end_date = st.date_input("Data final", max_value="today", disabled=disable_store, label_visibility="visible", key="selected_end_date")
        st.session_state["compare_stores_second_store_name"] = second_store
        st.session_state["compare_stores_second_store_id"] = second_store_id
        st.session_state["compare_stores_end_month"] = end_date.month
        st.session_state["compare_stores_end_year"] = end_date.year

    if st.session_state["compare_stores_first_store_name"] == "Selecione uma loja" or st.session_state["compare_stores_second_store_name"] == "Selecione uma loja":
        st.session_state["disable_confirm_button"] = True
    else:
        st.session_state["disable_confirm_button"] = False

    confirm_search = st.button("Comparar lojas", use_container_width=True, disabled=st.session_state["disable_confirm_button"], key="compare_stores_button")  
    if confirm_search:
        int_to_month = {
                1: 'janeiro', 2: 'fevereiro', 3: 'março', 4: 'abril', 5: 'maio', 6: 'junho',
                7: 'julho', 8: 'agosto', 9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'
            }
        if first_store != "Selicone uma loja" and second_store != "Selicone uma loja":
            if "user_info" in st.session_state:
                create_stores_comparison(st.session_state["user_info"]["user_email"], 
                                        st.session_state["compare_stores_first_store_id"], 
                                        st.session_state["compare_stores_second_store_id"], 
                                        st.session_state["compare_stores_vehicle_id"], 
                                        int_to_month[st.session_state["compare_stores_start_month"]], 
                                        st.session_state["compare_stores_start_year"],
                                        int_to_month[st.session_state["compare_stores_end_month"]],
                                        st.session_state["compare_stores_end_year"]
                                    )
        else:
            st.error("Selecione duas lojas para comparar os preços!")

        first_store_avg = get_avg_price_by_month_given_vehicle_store(st.session_state["compare_stores_vehicle_id"], st.session_state["compare_stores_first_store_id"], int_to_month[st.session_state["compare_stores_start_month"]], st.session_state["compare_stores_start_year"], int_to_month[st.session_state["compare_stores_end_month"]], st.session_state["compare_stores_end_year"])
        second_store_avg = get_avg_price_by_month_given_vehicle_store(st.session_state["compare_stores_vehicle_id"], st.session_state["compare_stores_second_store_id"], int_to_month[st.session_state["compare_stores_start_month"]], st.session_state["compare_stores_start_year"], int_to_month[st.session_state["compare_stores_end_month"]], st.session_state["compare_stores_end_year"])

        if len(first_store_avg) == 0 and len(second_store_avg) == 0:
            st.warning("Não há dados para nenhuma das lojas no período selecionado!")
        elif len(first_store_avg) == 0 and len(second_store_avg) > 0:
            st.warning(f"Não hádados para a loja {first_store} no período selecionado!")
        elif len(first_store_avg) > 0 and len(second_store_avg) == 0:
            st.warning(f"Não há dados para a loja {second_store} no período selecionado!")
        
        build_graph(first_store, first_store_avg, second_store, second_store_avg)

def format_date(month, year):
    months = {
        'janeiro': 'Jan', 'fevereiro': 'Fev', 'março': 'Mar', 'abril': 'Abr', 'maio': 'Mai', 'junho': 'Jun',
        'julho': 'Jul', 'agosto': 'Ago', 'setembro': 'Set', 'outubro': 'Out', 'novembro': 'Nov', 'dezembro': 'Dez'
    }
    return f"{months.get(month.lower(), month.capitalize())}/{str(year)[-2:]}"

def run_compare_stores_history():
    st.header("Histórico de pesquisas:")

    def styled_header_left(text: str):
        st.markdown(
            f"""
            <div style="
                background-color: rgba(240, 240, 240, 0.1);
                padding: 0.75rem 1rem;
                border-top-left-radius: 8px;
                font-weight: bold;
                color: inherit;
                height: 80px;
                margin-bottom: 20px;
                margin-top: 20px;
            ">
                {text}
            </div>
            """,
            unsafe_allow_html=True
        )

    def styled_header_right(text: str):
        st.markdown(
                f"""
                <div style="
                    background-color: rgba(240, 240, 240, 0.1);
                    padding: 0.75rem 1rem;
                    border-top-right-radius: 8px;
                    font-weight: bold;
                    color: inherit;
                    height: 80px;
                    margin-bottom: 20px;
                    margin-top: 20px;
                ">
                    {text}
                </div>
                """,
                unsafe_allow_html=True
            )

    def styled_header(text: str):
        st.markdown(
                f"""
                <div style="
                    background-color: rgba(240, 240, 240, 0.1);
                    padding: 0.75rem 1rem;
                    font-weight: bold;
                    color: inherit;
                    height: 80px;
                    margin-bottom: 20px;
                    margin-top: 20px;
                ">
                    {text}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    header1, header2, header3, header4, header5, header6, header7, _ = st.columns([3, 3, 3, 3, 3, 2, 2, 2])
    with header1:
        styled_header_left("Veículo")
    with header2: 
        styled_header("Loja 1")
    with header3:
        styled_header_right("Loja 2")
    with header4:
        styled_header_right("Data Inicial")
    with header5:
        styled_header_right("Data Final")

    comparisons = get_all_comparisons_by_email(st.session_state["user_info"]["user_email"])
    if comparisons:
        for comp in comparisons: 
            temp_vehicle_info = get_vehicle_details(comp["Veículo"])
            comp['Veículo Info'] = f"{temp_vehicle_info['model']}/{temp_vehicle_info['year']}"
            comp['Nome Loja 1'] = read_store(comp['Loja 1'])['name']
            comp['Nome Loja 2'] = read_store(comp['Loja 2'])['name']
            comp['Mês/Ano Inicial'] = format_date(comp['Mês Inicial'], comp['Ano Inicial'])
            comp['Mês/Ano Final'] = format_date(comp['Mês Final'], comp['Ano Final'])

        for comp in comparisons:
            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([3, 3, 3, 3, 3, 2, 2, 2])

            with col1:
                st.write(comp["Veículo Info"])
            with col2:
                st.write(comp['Nome Loja 1'])
            with col3:
                st.write(comp['Nome Loja 2'])
            with col4:
                st.write(comp["Mês/Ano Inicial"])
            with col5:
                st.write(comp["Mês/Ano Final"])
            with col6:
                st.session_state["show_results"] = st.button("Resultados", key=f"show_{comp['id']}")
                st.session_state["results_comp"] = comp
            with col7:
                st.session_state["clear_results"] = st.button("Limpar", key=f"clear_{comp['id']}")
            with col8:
                if st.button("Excluir", key=f"delete_{comp['id']}"):
                    delete_comparison(comp["id"])
                    st.success("Busca removida!")
                    time.sleep(1)
                    st.rerun()

            if st.session_state["show_results"]:
                first_store_avg = get_avg_price_by_month_given_vehicle_store(st.session_state["results_comp"]["Veículo"], st.session_state["results_comp"]["Loja 1"], st.session_state["results_comp"]["Mês Inicial"], st.session_state["results_comp"]["Ano Inicial"], st.session_state["results_comp"]["Mês Final"], st.session_state["results_comp"]["Ano Final"])
                second_store_avg = get_avg_price_by_month_given_vehicle_store(st.session_state["results_comp"]["Veículo"], st.session_state["results_comp"]["Loja 2"], st.session_state["results_comp"]["Mês Inicial"], st.session_state["results_comp"]["Ano Inicial"], st.session_state["results_comp"]["Mês Final"], st.session_state["results_comp"]["Ano Final"])

                build_graph(st.session_state["results_comp"]["Nome Loja 1"], first_store_avg, st.session_state["results_comp"]["Nome Loja 2"], second_store_avg)
                if st.session_state["clear_results"]:
                    st.rerun()