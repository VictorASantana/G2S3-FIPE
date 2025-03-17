import streamlit as st
import time
from services.database_connection import create_connection
from services.brand import get_brands
from services.prices import save_price, get_prices_by_user, update_price, delete_price
from services.store import get_stores
from services.model import get_models_by_brand
from services.vehicles import get_vehicles_by_model
from utils.auth import check_required_role, get_logged_in_user_id

check_required_role('pesquisador')

def researcher_panel():
    st.title("Painel do Pesquisador")
    col_left, col_spacer, col_right = st.columns([1,6,1])
    with col_left:
        st.write(f"Bem vindo! {st.session_state['user_info'].get('name')}")
    with col_spacer:
        pass
    with col_right:
        go_back = st.button("Voltar")
        if go_back:
            st.switch_page("main.py")

    user_id = get_logged_in_user_id()  # Obtém o ID do usuário logado

    tab1, tab2, tab3 = st.tabs(["Registrar Preço", "Meus Preços", "Editar/Excluir Preço"])

    with tab1:
        stores = get_stores()
        store_options = {"Selecione...": None}
        store_options.update({store[1]: store[0] for store in stores})
        store_selected = st.selectbox("Selecione a loja", list(store_options.keys()))

        if store_selected != "Selecione...":
            store_id = store_options[store_selected]

            brands = get_brands()
            brand_options = {"Selecione...": None}
            brand_options.update({brand[1]: brand[0] for brand in brands})
            brand_selected = st.selectbox("Selecione a marca", list(brand_options.keys()))

            if brand_selected != "Selecione...":
                brand_id = brand_options[brand_selected]

                models = get_models_by_brand(brand_id)
                model_options = {"Selecione...": None}
                model_options.update({model[1]: model[0] for model in models})
                model_selected = st.selectbox("Selecione o modelo", list(model_options.keys()))

                if model_selected != "Selecione...":
                    model_id = model_options[model_selected]

                    vehicles = get_vehicles_by_model(model_id)
                    vehicle_options = {"Selecione...": None}
                    vehicle_options.update({f"{v[2]}": v[0] for v in vehicles})
                    vehicle_selected = st.selectbox("Selecione o ano do modelo do veículo", list(vehicle_options.keys()))

                    if vehicle_selected != "Selecione...":
                        vehicle_id = vehicle_options[vehicle_selected]

                        price = st.number_input("Digite o preço", min_value=0.0, format="%.2f")
                        collect_date = st.date_input("Data de coleta", max_value="today")

                        if st.button("OK"):
                            if 0 < price < 100000000.00:
                                save_price(store_id, vehicle_id, price, collect_date, user_id)
                                st.success("Preço registrado com sucesso!")
                            else:
                                st.error("Por favor, insira um preço válido.")

    with tab2:
        st.subheader("Meus Preços Registrados")
        prices = get_prices_by_user(user_id)

        if prices:
            for price in prices:
                price_id, store_name, brand_name, model_name, year, price_value, collect_date = price
                st.write(f"📌 {brand_name} {model_name} ({year}) - {store_name}: R$ {price_value:,.2f} ({collect_date.strftime('%d/%m/%Y')})")
        else:
            st.info("Você ainda não registrou nenhum preço.")

    with tab3:
        st.subheader("Editar ou Excluir Preço")

        prices = get_prices_by_user(user_id)
        price_options = {"Selecione...": None}
        price_options.update({
             f"{brand_name} {model_name} ({year}) - {store_name} - R$ {price_value:,.2f} ({collect_date.strftime('%d/%m/%Y')})": price_id
             for (price_id, store_name, brand_name, model_name, year, price_value, collect_date) in prices
         })
    
        price_selected = st.selectbox("Selecione o preço para editar/excluir", price_options)

        if price_selected != "Selecione...":
            price_id = price_options[price_selected]

            new_price = st.number_input("Novo preço", min_value=0.0, format="%.2f")
            new_collect_date = st.date_input("Nova data de coleta", max_value="today")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Salvar Alterações"):
                    result = update_price(price_id, new_price, new_collect_date, user_id)
                    if "Erro" in result:
                        st.error(result)
                    else:
                        st.success(result)
                    time.sleep(1)
                    st.rerun()
            with col2:
                if st.button("Excluir Preço", help="Essa ação não pode ser desfeita!"):
                    result = delete_price(price_id, user_id)
                    if "Erro" in result:
                        st.error(result)
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.success(result)
                        time.sleep(1)
                        st.rerun()
                    

if __name__ == "__main__":
    researcher_panel()
