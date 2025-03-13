from services.database_connection import create_connection, table_exists
import psycopg2
import streamlit as st

def create_model_table():
    if not table_exists("model"):
        conn = create_connection()
        if conn is None:
            print("Erro: Falha ao conectar ao banco de dados.")
        else:
            print("Conexão estabelecida com sucesso!")
        if conn is None:
            print("Erro ao conectar ao banco de dados. Tabela 'model' não foi criada.")
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE model (
                id SERIAL PRIMARY KEY,
                brand_id INT REFERENCES brand(id) ON DELETE CASCADE,
                name TEXT UNIQUE NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("Tabela 'model' criada com sucesso.")
    else: 
        print("Tabela 'model' já existe. Verificando restrições...")

        # Verifica se a restrição já está correta
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT conname, confdeltype FROM pg_constraint 
            WHERE conrelid = 'model'::regclass 
            AND confrelid = 'brand'::regclass;
        """)
        constraint = cur.fetchone()

        if constraint and constraint[1] != 'c':  # 'c' significa CASCADE
            print("Atualizando restrição de chave estrangeira...")
            cur.execute("ALTER TABLE model DROP CONSTRAINT model_brand_id_fkey;")
            cur.execute("""
                ALTER TABLE model ADD CONSTRAINT model_brand_id_fkey 
                FOREIGN KEY (brand_id) REFERENCES brand(id) ON DELETE CASCADE;
            """)
            conn.commit()
            print("Restrição atualizada para ON DELETE CASCADE.")

        cur.close()
        conn.close()  

def create_model(brand_id, name):
    conn = create_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO model (brand_id, name) VALUES (%s, %s) RETURNING id;", (brand_id, name))
        model_id = cur.fetchone()[0]
        conn.commit()
        st.success(f"Modelo '{name}' adicionado!") # à marca '{selected_brand}'!") 
        return model_id
    except psycopg2.Error as e:
        st.error("Modelo já existe") 
    finally:
        cur.close()
        conn.close()

def get_models(brand_id):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM model WHERE brand_id = %s ORDER BY name;", (brand_id,))
    models = cur.fetchall()
    cur.close()
    conn.close()
    return models

def get_model_id_by_name(name):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT id FROM model WHERE name = %s;", (name,))
    model_id = cur.fetchone()[0]
    cur.close()
    conn.close()
    return model_id

def update_model(model_id, new_name):
    conn = create_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE model SET name = %s WHERE id = %s;", (new_name, model_id))
        conn.commit()
        st.success(f"Modelo atualizada para '{new_name}'!")
    except psycopg2.Error as e:
        st.error("Modelo já existe") 
    finally:
        cur.close()
        conn.close()
    #return f"Modelo {model_id} atualizado para {new_name} com sucesso."

def delete_model(model_id):
    conn = create_connection()
    cur = conn.cursor()
    
    cur.execute("DELETE FROM model WHERE id = %s;", (model_id,))
    conn.commit()
    
    cur.close()
    conn.close()
    return f"Modelo {model_id} deletado com sucesso."
  
def get_models_by_brand(brand_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM model WHERE brand_id = %s;", (brand_id,))
    models = cursor.fetchall()
    conn.close()
    return models
