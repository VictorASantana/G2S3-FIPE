import streamlit as st
import pandas as pd
from utils.exponential import exponential_interpolation
from datetime import datetime

from services.brand import get_brands, get_brand_id_by_name
from services.model import get_models, get_model_id_by_name
from services.vehicles import get_vehicles, get_avg_price
from services.vehicle_monthly_avg import get_vehicle_monthly_avg
from utils.months import month_to_number


def interpolation_consult():
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
              'date': datetime(price[2], month_to_number(price[1]), 1),
              'value': float(price[3])
          }
        )
      
      exponential_interpolation(formatted_data)
