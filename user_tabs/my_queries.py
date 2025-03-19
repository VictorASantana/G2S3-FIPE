import streamlit as st

from services.vehicle_monthly_query import get_queries_by_user
from services.vehicles import get_vehicles, get_avg_price, get_vehicle_details

def run_my_queries():
    st.subheader("Minhas Consultas Salvas")

    current_user_id = 1
    
    with st.expander("Consulta de comparação com dólar"):
        st.write("insira aqui a função que retorna as consultas salvas")
    
    with st.expander("Consulta de comparação entre duas lojas"):
        st.write("insira aqui a função que retorna as consultas salvas")
    
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
    
                st.write("---")

        else:
            st.write("Nenhuma consulta encontrada para este tipo.")
    
    with st.expander("Consulta de diferença entre dois veículos"):
        st.write("insira aqui a função que retorna as consultas salvas")
    
    with st.expander("Consulta de preços futuros"):
        st.write("insira aqui a função que retorna as consultas salvas")