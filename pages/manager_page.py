import streamlit as st
from utils.auth import check_required_role
from services.user_register import get_all_users, update_user, delete_user, create_user
from services.brand import get_brands, create_brand, update_brand, delete_brand
from services.model import get_models_by_brand, create_model, update_model, delete_model
from services.vehicles import create_vehicle, get_vehicles_by_model, update_vehicle, delete_vehicle

check_required_role('gestor')

def gestor_panel():
    st.title("Painel do Gestor")
    if st.button("Voltar"):
      st.switch_page("main.py")
    menu = ["Gerenciar Marcas", "Gerenciar Modelos", "Gerenciar Veículos", "Gerenciar Usuários"]
    choice = st.sidebar.selectbox("Escolha uma opção", menu)
    
    if choice == "Gerenciar Marcas":
        st.header("Gerenciar Marcas")
        
        new_brand = st.text_input("Nome da Nova Marca")
        if st.button("Adicionar Marca"):
            create_brand(new_brand)
            st.success(f"Marca '{new_brand}' adicionada com sucesso!")
        
        brands = get_brands()
        brand_options = {b[1]: b[0] for b in brands}
        selected_brand = st.selectbox("Selecione uma marca para editar", ["Selecione"] + list(brand_options.keys()))
        
        if selected_brand != "Selecione":
            new_name = st.text_input("Novo Nome", selected_brand)
            if st.button("Atualizar Marca"):
                update_brand(brand_options[selected_brand], new_name)
                st.success(f"Marca atualizada para '{new_name}'!")
        
            if st.button("Excluir Marca"):
                delete_brand(brand_options[selected_brand])
                st.success(f"Marca '{selected_brand}' excluída com sucesso!")
    
    elif choice == "Gerenciar Modelos":
        st.header("Gerenciar Modelos")
        
        brands = get_brands()
        brand_options = {b[1]: b[0] for b in brands}
        selected_brand = st.selectbox("Selecione a marca", ["Selecione"] + list(brand_options.keys()))
        
        if selected_brand != "Selecione":
            brand_id = brand_options[selected_brand]
            
            new_model = st.text_input("Nome do Novo Modelo")
            if st.button("Adicionar Modelo"):
                create_model(brand_id, new_model)
                st.success(f"Modelo '{new_model}' adicionado à marca '{selected_brand}'!")
            
            models = get_models_by_brand(brand_id)
            model_options = {m[1]: m[0] for m in models}
            selected_model = st.selectbox("Selecione um modelo para editar", ["Selecione"] + list(model_options.keys()))
            
            if selected_model != "Selecione":
                new_model_name = st.text_input("Novo Nome", selected_model)
                if st.button("Atualizar Modelo"):
                    update_model(model_options[selected_model], new_model_name)
                    st.success(f"Modelo atualizado para '{new_model_name}'!")
                
                if st.button("Excluir Modelo"):
                    delete_model(model_options[selected_model])
                    st.success(f"Modelo '{selected_model}' excluído com sucesso!")
    
    elif choice == "Gerenciar Veículos":
        st.header("Gerenciar Veículos")
        
        brands = get_brands()
        brand_options = {b[1]: b[0] for b in brands}
        selected_brand = st.selectbox("Selecione a marca", ["Selecione"] + list(brand_options.keys()))
        
        if selected_brand != "Selecione":
            brand_id = brand_options[selected_brand]
            models = get_models_by_brand(brand_id)
            model_options = {m[1]: m[0] for m in models}
            selected_model = st.selectbox("Selecione o modelo", ["Selecione"] + list(model_options.keys()))
            
            if selected_model != "Selecione":
                model_id = model_options[selected_model]
                
                fabrication_year = st.number_input("Ano de Fabricação", min_value=1900, max_value=2100, step=1)
                model_year = st.number_input("Ano do Modelo", min_value=1900, max_value=2100, step=1)
                average_price = st.number_input("Preço Médio", min_value=0.0, format="%.2f")
                
                if st.button("Adicionar Veículo"):
                    create_vehicle(model_id, fabrication_year, model_year, average_price)
                    st.success("Veículo cadastrado com sucesso!")
                
                vehicles = get_vehicles_by_model(model_id)
                vehicle_options = {f"{v[1]}/{v[2]}": v[0] for v in vehicles}
                selected_vehicle = st.selectbox("Selecione um veículo para editar", ["Selecione"] + list(vehicle_options.keys()))
                
                if selected_vehicle != "Selecione":
                    vehicle_id = vehicle_options[selected_vehicle]
                    new_fabrication_year = st.number_input("Novo Ano de Fabricação", min_value=1900, max_value=2026, step=1)
                    new_model_year = st.number_input("Novo Ano do Modelo", min_value=1900, max_value=2026, step=1)
                    
                    if st.button("Atualizar Veículo"):
                        update_vehicle(vehicle_id, model_id, new_fabrication_year, new_model_year)
                        st.success("Veículo atualizado com sucesso!")
                    
                    if st.button("Excluir Veículo"):
                        delete_vehicle(vehicle_id)
                        st.success("Veículo excluído com sucesso!")

    elif choice == "Gerenciar Usuários":
      st.header("Gerenciar Usuários")
      if "editing_user_id" not in st.session_state:
        st.session_state.editing_user_id = None
      if "creating_user" not in st.session_state:
        st.session_state.creating_user = False

      #Painel de usuários
      users = get_all_users()

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
      st.subheader("Usuários Cadastrados: ")

      header1, header2, header3, header4, header5 = st.columns([3, 3, 3, 2, 2])
      with header1:
        styled_header_left("Nome do Usuário")
      with header2: 
        styled_header("Email")
      with header3:
        styled_header_right("Papel")

      for row in users:
        col1, col2, col3, col4, col5 = st.columns([3, 3, 3, 2, 2])

        with col1:
          st.write(row["name"])
        with col2:
          st.write(row["email"])
        with col3:
          st.write(row["role"])
        with col4:
          if st.button("Editar", key=f"edit_{row['id']}"):
            st.session_state.editing_user_id = row['id']
          with col5:
            if st.button("Excluir", key=f"delete_{row['id']}"):
              delete_user(row["id"])
              st.warning("Usuário excluído!")

        if st.session_state.editing_user_id == row['id']:
          with st.form(f"form_edit_{row['id']}", clear_on_submit=False):
            new_name = st.text_input("Nome", value=row["name"])
            new_email = st.text_input("Email", value=row["email"])
            new_role = st.selectbox("Role", ["gestor", "pesquisador"])
            form_col1, form_col2 = st.columns(2)
            with form_col1:
              if st.form_submit_button("Salvar", use_container_width=True):
                update_user(row["id"], new_name, new_email, new_role)
                st.success("Usuário atualizado!")
                st.session_state.editing_user_id = None
                st.rerun() 
            with form_col2:
              if st.form_submit_button("Cancelar", use_container_width=True):
                st.session_state.editing_user_id = None
                st.rerun() 

      st.divider()

      st.subheader("Cadastro: ")
      if st.button("Adicionar novo Usuário"):
        st.session_state.creating_user = True

      if st.session_state.creating_user:
        with st.form("Adding user", clear_on_submit=True):
          new_name = st.text_input("Nome")
          new_email = st.text_input("Email")
          new_role = st.selectbox("Role", ["pesquisador", "gestor"])
          form_col1, form_col2 = st.columns(2)
          with form_col1:
            if st.form_submit_button("Criar", use_container_width=True):
              create_user(new_name, new_email, new_role)
              st.success("Usuário Criado com Sucesso!")
              st.session_state.creating_user = False
              st.rerun() 
          with form_col2:
            if st.form_submit_button("Cancelar", use_container_width=True):
              st.session_state.creating_user = False
              st.rerun() 

if __name__ == "__main__":
    gestor_panel()
    