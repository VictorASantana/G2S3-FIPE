import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import calendar

from services.vehicle_monthly_query import get_queries_by_user, delete_vehicle_monthly_query
from services.vehicles import get_vehicles, get_avg_price, get_vehicle_details
from user_tabs.compare_stores_tab import run_compare_stores_history
from services.vehicle_monthly_avg import get_vehicle_monthly_avg
from user_tabs.future_prices import interpolation_consult_history

def run_my_queries():
    st.subheader("Minhas Consultas Salvas")

    if "user_info" not in st.session_state or not st.session_state["user_info"]:
        st.warning("Você precisa estar logado para visualizar suas consultas salvas.")
        return

    current_user_id = st.session_state["user_info"]["user_id"]
    
    with st.expander("Consulta de comparação com dólar"):
        st.write("insira aqui a função que retorna as consultas salvas")
    
    with st.expander("Consulta de comparação entre duas lojas"):
        run_compare_stores_history()
    
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

                vehicle1_avg_prices = get_vehicle_monthly_avg(vehicle1["id"])
                vehicle2_avg_prices = get_vehicle_monthly_avg(vehicle2["id"])

                data_vehicle1 = []
                data_vehicle2 = []

                month_mapping = {
                    "janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4, "maio": 5,
                    "junho": 6, "julho": 7, "agosto": 8, "setembro": 9, "outubro": 10,
                    "novembro": 11, "dezembro": 12
                }

                start_month = month_mapping[query[4].lower()]  # 'query[4]' é o mês inicial
                end_month = month_mapping[query[5].lower()]    # 'query[5]' é o mês final
                start_year = int(query[6])  
                end_year = int(query[6])

                months_years = generate_months(start_month, start_year, end_month, end_year)


                for month_num, year_num in months_years:
                    vehicle1_data = next((item for item in vehicle1_avg_prices if item[1] == month_num and item[2] == year_num), None)
                    vehicle2_data = next((item for item in vehicle2_avg_prices if item[1] == month_num and item[2] == year_num), None)

                    data_vehicle1.append(vehicle1_data[3] if vehicle1_data else None)
                    data_vehicle2.append(vehicle2_data[3] if vehicle2_data else None)

                df_comparison = pd.DataFrame({
                    "Mês/Ano": [f"{calendar.month_name[m]} {y}" for m, y in months_years],
                    f"{vehicle1['model']} ({vehicle1['brand']})": data_vehicle1,
                    f"{vehicle2['model']} ({vehicle2['brand']})": data_vehicle2
                })

                delete_button_key = f"excluir_{query[0]}"
                if st.button("Excluir Consulta", key=delete_button_key):
                    delete_vehicle_monthly_query(query[0])
                    st.write(f"Consulta de {vehicle1['model']} vs {vehicle2['model']} excluída com sucesso!")
                    st.rerun()

                if not df_comparison.empty:
                    button_key = f"exibir_grafico_{query[0]}"
                    close_button_key = f"fechar_grafico_{query[0]}"

                    if st.button("Exibir Gráfico", key=button_key):
                        fig, ax = plt.subplots(figsize=(10, 5))

                        ax.plot(df_comparison["Mês/Ano"], df_comparison[f"{vehicle1['model']} ({vehicle1['brand']})"], 
                                marker='o', linestyle='-', label=f"{vehicle1['model']} ({vehicle1['brand']})")

                        ax.plot(df_comparison["Mês/Ano"], df_comparison[f"{vehicle2['model']} ({vehicle2['brand']})"], 
                                marker='s', linestyle='-', label=f"{vehicle2['model']} ({vehicle2['brand']})")

                        ax.set_xlabel("Mês/Ano")
                        ax.set_ylabel("Preço Médio (R$)")
                        ax.set_title("Comparação de Preços Médios Mensais")
                        ax.legend()
                        ax.grid(True)
                        plt.xticks(rotation=45)

                        st.pyplot(fig)
                    
                        if st.button("Ocultar Gráfico", key=close_button_key):
                            st.empty()

                else:
                    st.write("Sem dados suficientes para exibir o gráfico.")
    
                st.write("---")

        else:
            st.write("Nenhuma consulta encontrada para este tipo.")
    
    with st.expander("Consulta de diferença entre dois veículos"):
        st.write("insira aqui a função que retorna as consultas salvas")
    
    with st.expander("Consulta de preços futuros"):
        interpolation_consult_history(current_user_id)