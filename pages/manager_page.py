import streamlit as st
import psycopg2
from utils.auth import check_required_role
from services.user_register import get_all_users, update_user, delete_user, create_user, get_all_researcher_info, read_user
from services.brand import get_brands, create_brand, update_brand, delete_brand
from services.model import get_models_by_brand, create_model, update_model, delete_model
from services.vehicles import create_vehicle, get_vehicles_by_model, update_vehicle, delete_vehicle
from services.store import create_store, update_store, delete_store, get_stores, get_all_stores_info
import time
import pandas as pd

check_required_role('gestor')

st.set_page_config(
    page_title="Painel do Gestor",
    layout="wide"
)

time.sleep(0.1) # small timeout ensure config is applied

# initialize session_state variables
if "states_tuple" not in st.session_state:
    st.session_state["states_tuple"] = ('AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 
                                        'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 
                                        'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO')
if "new_store_name" not in st.session_state:
    st.session_state["new_store_name"] = ""
if "new_store_CNPJ" not in st.session_state:
    st.session_state["new_store_CNPJ"] = "12.345.678/0001-95"
if "new_store_state" not in st.session_state:
    st.session_state["new_store_state"] = "AC"
if "new_store_user_id" not in st.session_state:
    st.session_state["new_store_user_id"] = None

if "stores_available" not in st.session_state:
    st.session_state["stores_available"] = None
if "selected_store_id" not in st.session_state:
    st.session_state["selected_store_id"] = None
if "selected_store_name" not in st.session_state:
    st.session_state["selected_store_name"] = None
if "selected_store_CNPJ" not in st.session_state:
    st.session_state["selected_store_CNPJ"] = "12.345.678/0001-95"
if "selected_store_state" not in st.session_state:
    st.session_state["selected_store_state"] = "AC"
if "selected_store_user_id" not in st.session_state:
    st.session_state["selected_store_user_id"] = None

if "updated_store_user_id" not in st.session_state:
    st.session_state["updated_store_user_id"] = None
if "updated_store_name" not in st.session_state:
    st.session_state["updated_store_name"] = None
if "updated_store_state" not in st.session_state:
    st.session_state["updated_store_state"] = None

if "new_brand_button_key" not in st.session_state:
    st.session_state["new_brand_button_key"] = 0
if "new_model_button_key" not in st.session_state:
    st.session_state["new_model_button_key"] = 0

def gestor_panel():
    st.title("Painel do Gestor")
    st.write(f"Bem vindo! {st.session_state['user_info'].get('name')}")

    if st.button("Voltar"):
      st.switch_page("main.py")
    
    menu = ["Gerenciar Marcas", "Gerenciar Modelos", "Gerenciar Veículos", "Gerenciar Usuários", "Gerenciar Lojas"]
    choice = st.sidebar.selectbox("Escolha uma opção", menu)
    
    if choice == "Gerenciar Marcas":
        st.header("Gerenciar Marcas")
        
        new_brand = st.text_input("Nome da Nova Marca", key=st.session_state["new_brand_button_key"])
        if st.button("Adicionar Marca"):
            if new_brand != "": 
                create_brand(new_brand)
                st.session_state["new_brand_button_key"] += 1
            else:
                st.error(f"Campo nome não pode ser vazio!")
            time.sleep(1)
            st.rerun()

        brands = get_brands()
        brand_options = {b[1]: b[0] for b in brands}
        selected_brand = st.selectbox("Selecione uma marca para editar", ["Selecione"] + list(brand_options.keys()))
        
        if selected_brand != "Selecione":
            new_name = st.text_input("Novo Nome", selected_brand)
            if st.button("Atualizar Marca"):
                if new_name != "": 
                    update_brand(brand_options[selected_brand], new_name)
                else:
                    st.error(f"Campo novo nome não pode ser vazio!")
                time.sleep(1)
                st.rerun()
        
            if st.button("Excluir Marca"):
                delete_brand(brand_options[selected_brand])
                st.success(f"Marca '{selected_brand}' excluída com sucesso!")
                st.rerun()
    
    elif choice == "Gerenciar Modelos":
        st.header("Gerenciar Modelos")
        
        brands = get_brands()
        brand_options = {b[1]: b[0] for b in brands}
        selected_brand = st.selectbox("Selecione a marca", ["Selecione"] + list(brand_options.keys()))
        
        if selected_brand != "Selecione":
            brand_id = brand_options[selected_brand]
            
            new_model = st.text_input("Nome do Novo Modelo", key=st.session_state["new_model_button_key"])
            if st.button("Adicionar Modelo"):
                if new_model != "":
                    create_model(brand_id, new_model)
                    st.session_state["new_model_button_key"] += 1
                else:
                    st.error(f"Campo novo nome não pode ser vazio!")
                time.sleep(1)
                st.rerun()
            
            models = get_models_by_brand(brand_id)
            model_options = {m[1]: m[0] for m in models}
            selected_model = st.selectbox("Selecione um modelo para editar", ["Selecione"] + list(model_options.keys()))
            
            if selected_model != "Selecione":
                new_model_name = st.text_input("Novo Nome", selected_model)
                if st.button("Atualizar Modelo"):
                    if new_model_name != "":
                        update_model(model_options[selected_model], new_model_name)
                    else:
                        st.error(f"Campo novo nome não pode ser vazio!")
                
                if st.button("Excluir Modelo"):
                    delete_model(model_options[selected_model])
                    st.success(f"Modelo '{selected_model}' excluído com sucesso!")
                    time.sleep(1)
                    st.rerun()
    
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
                  result = create_vehicle(model_id, fabrication_year, model_year, average_price)
                
                  if "Erro" in result:
                      st.error(result)
                  else:
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
              time.sleep(1)
              st.rerun()
              

        if st.session_state.editing_user_id == row['id']:
          with st.form(f"form_edit_{row['id']}", clear_on_submit=False):
            new_name = st.text_input("Nome", value=row["name"])
            new_email = st.text_input("Email", value=row["email"])
            new_role = st.selectbox("Role", ["gestor", "pesquisador"])
            form_col1, form_col2 = st.columns(2)
            with form_col1:
                if st.form_submit_button("Salvar", use_container_width=True):
                    if new_name == "" or new_email == "":
                        st.error("Preencha todos os campos!")
                    else:
                        update_user(row["id"], new_name, new_email, new_role)
                    st.session_state.editing_user_id = None
                    time.sleep(1)
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
            if st.form_submit_button("Cadastrar", use_container_width=True):
                if new_name == "" or new_email == "":
                    st.error("Preencha todos os campos!")
                else:
                    create_user(new_name, new_email, new_role)
                st.session_state.creating_user = False
                time.sleep(1)
                st.rerun() 
          with form_col2:
            if st.form_submit_button("Cancelar", use_container_width=True):
              st.session_state.creating_user = False
              st.rerun() 

    elif choice == "Gerenciar Lojas":
      create_col, stores_col = st.columns(2)

      with create_col: #Future improvement -> after clean go back to placeholder
        st.title("Adicione uma loja")

        st.session_state["new_store_name"] = st.text_input("Nome da loja", placeholder="Insira o nome da loja")
        st.session_state["new_store_CNPJ"] = st.text_input("CNPJ", placeholder="Insira o CNPJ da loja")
        st.session_state["new_store_state"] = st.selectbox("Estado", st.session_state["states_tuple"], placeholder="Selecione um estado")

        available_researchers_id = get_all_researcher_info(info="id") 
        available_researchers_name = get_all_researcher_info(info="user_name")
        new_store_user_name = st.selectbox("Pesquisadores disponíveis", available_researchers_name, placeholder="Selecione um pesquisador")
        id_idx = available_researchers_name.index(new_store_user_name) 

        st.session_state["new_store_user_id"] = available_researchers_id[id_idx]

        confirm_creation_col, clear_creation_col = st.columns(2)
        with confirm_creation_col:
          if st.button("Adicionar loja", use_container_width=True):
            if st.session_state["new_store_name"] == "" or st.session_state["new_store_CNPJ"] == "":
                st.error("Preencha todos os campos!")
            else: 
                create_store(st.session_state["new_store_user_id"], 
                            st.session_state["new_store_name"], 
                            st.session_state["new_store_state"], 
                            st.session_state["new_store_CNPJ"])
                time.sleep(1)
                st.rerun()
        with clear_creation_col:
          if st.button("Limpar campos", use_container_width=True):
              st.session_state["new_store_name"] = ""
              st.session_state["new_store_CNPJ"] = "12.345.678/0001-95"
              st.session_state["new_store_state"] = "AC"
              st.session_state["new_store_user_id"] = None
              st.rerun()

      with stores_col:
        st.title("Selecione uma loja")
        
        #st.header("Selecione uma loja")
        available_stores_ids = get_all_stores_info(info="id")
        available_researchers_ids = get_all_stores_info(info="user_id")
        user_names_candidates = []
        for id in available_researchers_ids:
            user = read_user(int(id))
            user_names_candidates.append(user["user_name"])
        available_stores_names = get_all_stores_info(info="name")
        available_stores_state = get_all_stores_info(info="state")
        available_stores_CNPJ = get_all_stores_info(info="CNPJ")
        
        data = {
            "Id": available_stores_ids, 
            "Id Pesquisador": user_names_candidates,
            "Nome": available_stores_names,
            "Estado": available_stores_state,
            "CNPJ": available_stores_CNPJ
        }
        df = pd.DataFrame(data)

        stores_to_select = st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
            height=300
        )

        st.write("Loja selecionada")
        selected_store = stores_to_select.selection.rows
        filtered_df = df.iloc[selected_store]
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
        )

        if len(filtered_df)>0:
            st.session_state["selected_store_id"] = filtered_df["Id"].values[0]
            st.session_state["selected_store_user_id"] = filtered_df["Id Pesquisador"].values[0]
            st.session_state["selected_store_name"] = filtered_df["Nome"].values[0]
            st.session_state["selected_store_CNPJ"] = filtered_df["Estado"].values[0]
            st.session_state["selected_store_state"] = filtered_df["Id"].values[0]


        update_name_col, update_state_col, update_researcher_col = st.columns(3)
        with update_name_col:
            st.session_state["updated_store_name"] = st.text_input("Novo Nome da loja", placeholder="Insira o novo nome da loja")
        with update_state_col:
            st.session_state["updated_store_state"] = st.selectbox("Estado", st.session_state["states_tuple"], placeholder="Selecione um novo estado")
        with update_researcher_col:
            available_researchers_id = get_all_researcher_info(info="id")
            available_researchers_name = get_all_researcher_info(info="user_name")
            updated_store_user_name = st.selectbox("Pesquisadores disponíveis", available_researchers_name, placeholder="Selecione um pesquisador", key="updated_store_user_name")
            id_idx = available_researchers_name.index(updated_store_user_name) 
            st.session_state["updated_store_user_id"] = available_researchers_id[id_idx]

        update_col, clear_update_col, delete_col = st.columns(3)
        with update_col:
            update_button = st.button("Atualizar informações", use_container_width=True)
            if update_button and st.session_state["selected_store_id"] is not None:
                print(st.session_state["selected_store_id"])
                update_store(int(st.session_state["selected_store_id"]),
                            st.session_state["updated_store_user_id"], 
                            st.session_state["updated_store_name"], 
                            st.session_state["updated_store_state"]
                )
                time.sleep(1)
                st.rerun()
            elif update_button:
                st.write("Selecione uma loja!")

        with clear_update_col:
            cancel_update_button = st.button("Cancelar atualização", use_container_width=True, key="cancel_update_button")
            if cancel_update_button:
                st.rerun()  

        with delete_col:
            remove_store_button = st.button("Remover loja", use_container_width=True, key="remove_store_button")
            if remove_store_button and st.session_state["selected_store_id"] is not None:
                delete_store(int(st.session_state["selected_store_id"]))
                st.success("Loja excluída com sucesso!")
                time.sleep(1)
                st.rerun()
            elif remove_store_button:
                st.write("Selecione uma loja!")

if __name__ == "__main__":
    gestor_panel()