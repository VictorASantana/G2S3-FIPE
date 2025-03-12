import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.brand import get_brands
from services.model import get_models
from services.vehicles import get_vehicles

# Título da página
st.title("Seleção de Veículo")

brands = get_brands()
brand_options = {name: id for id, name in brands}
selected_brand = st.selectbox("Selecione a Marca", ["Selecione uma marca"] + list(brand_options.keys()))

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
    disabled=disable_model  )

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
    disabled=disable_vehicle) 
