import time
import streamlit as st

from datetime import datetime
from utils.exponential import exponential_interpolation
from services.brand import get_brands
from services.model import get_models
from services.vehicles import get_vehicles, get_vehicle_details
from services.vehicle_monthly_avg import get_vehicle_monthly_avg
from services.interpolation_query import get_interpolation_queries_by_user, delete_interpolation_query

if "show_interpolation_results" not in st.session_state:
  st.session_state.show_interpolation_results = None


def future_prices():
  st.title("Consultar Interpolação Exponencial: ")

  with st.expander("Consulta de Preços", expanded=False):
    brands = get_brands()
    brand_options = {name: id for id, name in brands}
    selected_brand = st.selectbox("Selecione a Marca", ["Selecione uma marca"] + list(brand_options.keys()), label_visibility="visible", key="interpolation_selector")

    disable_model = selected_brand == "Selecione uma marca"
    disable_vehicle = True 

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
      label_visibility="visible",
      key="interpolation_model_selector"
    )

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
      label_visibility="visible",
      key='interpolation_vehicle_consult') 
    
    if selected_vehicle != 'Selecione um veículo' and selected_vehicle:
      selected_vehicle = vehicle_options[selected_vehicle]
    disable_price = selected_vehicle == "Selecione um veículo"

    future_price_search = st.button(
      "Pesquisar preço",
      disabled=disable_price,
      use_container_width=True,
      key="interpolation_future_price"
    ) 

    if future_price_search: 
      avg_prices = get_vehicle_monthly_avg(selected_vehicle)
      formatted_data = []

      for price in avg_prices:
        formatted_data.append(
          {
              'date': datetime(price[2], price[1], 1),
              'value': float(price[3])
          }
        )

      if "user_info" in st.session_state and "user_id" in st.session_state["user_info"]:
        user_id = st.session_state["user_info"]["user_id"]
      else:
        user_id = None        

      exponential_interpolation(formatted_data, user_id, selected_vehicle)

def interpolation_consult_history(user_id):
  st.header("Histórico de Consultas")

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

  header1, header2, header3, header4, header5, header6, header7 = st.columns([3, 3, 2, 3, 3, 3, 2])
  with header1:
    styled_header_left("Marca")
  with header2: 
    styled_header("Modelo")
  with header3:
    styled_header("Ano")
  with header4:
    styled_header("Equação")
  with header5:
    styled_header_right("Data de Consulta")

  comparisons = get_interpolation_queries_by_user(user_id)
  
  for comparison in comparisons:
    col1, col2, col3, col4, col5, col6, col7 = st.columns([3, 3, 2, 3, 3, 3, 2])
    avg_prices = get_vehicle_monthly_avg(comparison['vehicle_id'])
    vehicle_details = get_vehicle_details(comparison['vehicle_id'])
    formatted_data = []

    for price in avg_prices:
      formatted_data.append(
        {
          'date': datetime(price[2], price[1], 1),
          'value': float(price[3])
        }
      )

    with col1:
      st.write(vehicle_details["brand"])
    with col2:
      st.write(vehicle_details["model"])
    with col3:
      st.write(vehicle_details["year"])
    with col4:
      st.write(f"{comparison['coef_a']:.2f}e$^{{{comparison['coef_b']:.2f}x}}$")
    with col5:
      st.write(f"{comparison['query_date'].strftime('%d/%m/%Y')}")
    with col6:
      if st.button("Resultados", key=f"show_{comparison['id']}"):
        st.session_state.show_interpolation_results = comparison['id']
        st.rerun()
    with col7:
      if st.button("Excluir", key=f"delete_{comparison['id']}"):
        delete_interpolation_query(comparison['id'])
        time.sleep(1)
        st.rerun()

    if st.session_state.show_interpolation_results == comparison['id']:
      exponential_interpolation(formatted_data, None, None)