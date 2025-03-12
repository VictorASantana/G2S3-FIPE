# -*- coding: utf-8 -*-
import streamlit as st

# Configuração da página
st.set_page_config(page_title="AutoValor FIPE", page_icon="🚗", layout="centered")

# Título da aplicação
st.title(" AutoValor FIPE")

# Botão expansível para "Consulta de Preços"
with st.expander("🚗 Consulta de Preços", expanded=False):
    # Campo expansivo para selecionar a marca do veículo
    marca = st.selectbox(
        "",  # Descrição do campo em branco
        ["Selecione uma marca", "Ford", "Toyota", "Volkswagen", "Chevrolet", "Fiat", "Honda", "BMW", 
         "Mercedes-Benz", "Audi", "Porsche", "Ferrari", "Lamborghini", "Maserati", "Aston Martin", 
         "Jaguar", "Land Rover", "Chrysler", "Dodge", "Jeep", "Nissan", "Hyundai", "Kia", "Subaru", 
         "Mazda", "Peugeot", "Renault", "Citroën", "Alfa Romeo", "Tesla", "McLaren"]
    )
    
    # Campo expansivo para selecionar o modelo do veículo
    modelo = st.selectbox(
        "",  # Descrição do campo em branco
        ["Selecione um modelo", "F-150", "Hilux", "Gol", "Onix", "Uno", "Civic", "Mustang", "Camaro", 
         "Porsche 911", "Ferrari F40", "Chevrolet Corvette", "Dodge Charger", "Nissan GT-R", "Lamborghini Aventador", 
         "Maserati GranTurismo", "Aston Martin DB9", "Jaguar E-Type", "Ford GT", "Shelby Cobra", "BMW M3", 
         "Mercedes-Benz AMG GT", "Audi R8", "McLaren 720S", "Plymouth Barracuda", "Chevrolet Camaro SS", 
         "Toyota Supra", "Mazda RX-7", "Subaru Impreza WRX STI", "Alfa Romeo Giulia Quadrifoglio", "Tesla Roadster",
         "Chevette", "Fusca", "Opala", "Chevrolet Bel Air", "Ford Maverick", "Corsa Classic", "Karmann Ghia", "Dodge Dart"]
    )

    # Campo expansivo para selecionar o ano de modelo do veículo
    ano_modelo = st.selectbox(
        "",  # Descrição do campo em branco
        ["Selecione um ano", "2020", "2021", "2022", "2023", "2024", "1960", "1970", "1980", "1990", "2000"]
    )

    # Botão de pesquisa expansivo
    if st.button("Pesquisar"):
        if marca != "Selecione uma marca" and mes_ano:
            st.success(f"Consultando preços para {marca} em {mes_ano}...")
            # Adiciona a lógica para buscar no banco de dados
        else:
            st.warning("Por favor, selecione uma marca e insira o mês/ano.")

# Rodapé
st.markdown("---")
st.write("Desafio Minerva [Power Tow] - © 2025 AutoValor FIPE")

