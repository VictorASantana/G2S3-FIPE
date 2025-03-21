from services.database_connection import create_connection, table_exists
from services.user_register import get_all_user_info
import psycopg2
import streamlit as st

def create_store_table():
    if not table_exists("store"):
        conn = create_connection()
        cur = conn.cursor()

        # Criando o tipo ENUM se ainda não existir
        cur.execute("""
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'store_state') THEN
                    CREATE TYPE store_state AS ENUM ('AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 
                                                   'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 
                                                   'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO');
                END IF;
            END $$;
        """)

        cur.execute("""
            CREATE TABLE store (
                id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(id),
                name TEXT NOT NULL,
                state store_state NOT NULL,
                CNPJ TEXT UNIQUE NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("Tabela 'store' criada com sucesso.")
    else: 
        pass
        #print("Tabela 'store' já existe.")

def get_stores():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM store;")
    stores = cursor.fetchall()
    conn.close()
    return stores

def get_all_stores_info(info="id"): 
    """Retorna uma lista com todos os "info" dos lojas."""
    
    info_list = ['id', 'user_id', 'name', 'state', 'CNPJ']
    try:
        idx = info_list.index(info) 
    except ValueError:
        print(f"'{info}' not found in the store table.")
        return None

    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT {info} FROM store;")
        user_info = [row[0] for row in cursor.fetchall()]
        return user_info

    except psycopg2.Error as e:
        print(f"Erro ao buscar {info} das lojas: {e}")
        return []

    finally:
        cursor.close()
        conn.close()
  
def create_store(user_id, name, state='AC', CNPJ='12.345.678/0001-95'):
    conn = create_connection()
    cursor = conn.cursor()

    create_store_table()  

    try:
        cursor.execute("SELECT * FROM store WHERE CNPJ = %s;", (CNPJ,))
        existing_store = cursor.fetchone()

        if not existing_store:
            if user_id in get_all_user_info(info="id"):
                cursor.execute(
                    "INSERT INTO store (user_id, name, state, CNPJ) VALUES (%s, %s, %s, %s)",
                    (user_id, name, state, CNPJ)
                )
                conn.commit()
                st.success("Loja inserida com sucesso!")
                print("Loja inserida com sucesso!")
            else: 
                print("Pesquisador inválido! Selecione um id de pesquisador válido.")
        else:
            st.error("Loja já existe no banco de dados.")
            print("Loja já existe no banco de dados.")

    except psycopg2.Error as e:
        print(f"Erro ao inserir loja: {name}\n{e}")
    
    finally:
        cursor.close()
        conn.close()

def read_store(store_id):
    conn = create_connection()
    cursor = conn.cursor()

    create_store_table()  

    try:
        cursor.execute("SELECT * FROM store WHERE id = %s;", (store_id,))
        existing_store = cursor.fetchone()

        if existing_store:
            store_info = {
                'id': existing_store[0],
                'user_id': existing_store[1], 
                'name': existing_store[2], 
                'state': existing_store[3],        
            }
            return store_info
        else:
            print("Loja não existe no banco de dados.")

    except psycopg2.Error as e:
        print(f"Erro ao ler loja:\n{e}")
    
    finally:
        cursor.close()
        conn.close()

def update_store(store_id, user_id=None, name=None, state=None):
    conn = create_connection()
    cursor = conn.cursor()

    create_store_table()  

    try:
        cursor.execute("SELECT * FROM store WHERE id = %s;", (store_id,))
        existing_store = cursor.fetchone()

        if existing_store:
            
            #campos a serem atualizados
            updates = []
            values = []

            if user_id != existing_store[1]:
                updates.append("user_id = %s")
                values.append(user_id)
            if name != "" and name != existing_store[2]:
                updates.append("name = %s")
                values.append(name)
            if state != existing_store[3]:
                updates.append("state = %s")
                values.append(state)
            
            # checa se tem informacoes para atualizar
            if updates:
                print(updates)
                print(values)
                values.append(store_id)  # Adiciona o user_id para a cláusula WHERE
                update_query = f"UPDATE store SET {', '.join(updates)} WHERE id = %s;"
                cursor.execute(update_query, tuple(values))
                conn.commit()
                st.success(f"Loja atualizada com sucesso!")
                print(f"Loja com ID {store_id} atualizado com sucesso!")
            else:
                st.write(f"Nenhuma informação nova fornecida para atualização.")
                print("Nenhuma informação nova fornecida para atualização.")
        else:
            print("Loja não existe no banco de dados.")

    except psycopg2.Error as e:
        print(f"Erro ao ler loja:\n{e}")
    
    finally:
        cursor.close()
        conn.close()

def delete_store(store_id):
    conn = create_connection()
    cursor = conn.cursor()

    create_store_table()  

    try:
        cursor.execute("SELECT * FROM store WHERE id = %s;", (store_id,))
        existing_store = cursor.fetchone()

        if existing_store:
            cursor.execute("DELETE FROM store WHERE id = %s;", (store_id,))
            conn.commit()
            print("Loja removida com sucesso!")
        else:
            print("Loja não existe no banco de dados.")

    except psycopg2.Error as e:
        print(f"Erro ao remover loja {store_id}:\n{e}")
    
    finally:
        cursor.close()
        conn.close()

def get_store_id_by_name(name):
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT DISTINCT id
            FROM store 
            WHERE name = %s;
        """, (name,))
        
        store_id = cursor.fetchone()[0]
        return store_id
    except: 
        pass
    finally:
        cursor.close()
        conn.close()
    