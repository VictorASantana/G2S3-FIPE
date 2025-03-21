import streamlit as st
import psycopg2
from services.database_connection import create_connection, table_exists

def create_user_table():
    if not table_exists("users"):
        conn = create_connection()
        cur = conn.cursor()

        # Criando o tipo ENUM se ainda não existir
        cur.execute("""
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role') THEN
                    CREATE TYPE user_role AS ENUM ('gestor', 'pesquisador', 'usuario');
                END IF;
            END $$;
        """)

        cur.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                user_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                role user_role NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("Tabela 'users' criada com sucesso.")
    else: 
        print("Tabela 'users' já existe.")

def get_all_user_info(info="id"): 
    """Retorna uma lista com todos os "info" dos usuários."""
    
    info_list = ['id', 'user_name', 'email', 'role']
    try:
        idx = info_list.index(info) 
    except ValueError:
        print(f"'{info}' not found in the user table.")
        return None

    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT {info} FROM users;")
        user_info = [row[0] for row in cursor.fetchall()]
        return user_info

    except psycopg2.Error as e:
        print(f"Erro ao buscar {info} dos usuários: {e}")
        return []

    finally:
        cursor.close()
        conn.close()

def get_all_researcher_info(info="id"): 
    """Retorna uma lista com todos os "info" dos pesquisadores."""
    
    info_list = ['id', 'user_name', 'email', 'role']
    try:
        idx = info_list.index(info) 
    except ValueError:
        print(f"'{info}' not found in the user table.")
        return None

    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT {info} FROM users WHERE role = 'pesquisador';")
        user_info = [row[0] for row in cursor.fetchall()]
        return user_info

    except psycopg2.Error as e:
        print(f"Erro ao buscar {info} dos usuários: {e}")
        return []

    finally:
        cursor.close()
        conn.close()

def get_all_users():
    conn = create_connection()
    cursor = conn.cursor()

    try: 
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        formatted_users = []
        for user in users:
            formatted_users.append({
                "id": user[0],
                "name": user[1],
                "email": user[2],
                "role": user[3]
            })
        return formatted_users

    except psycopg2.Error as e:
        print(f"Erro ao buscar usuários: {e}")
        return None

    finally:
        cursor.close()
        conn.close()

def create_user(user_name, email, role='pesquisador'):
    conn = create_connection()
    cursor = conn.cursor()

    create_user_table()  

    try:
        cursor.execute("SELECT * FROM users WHERE email = %s;", (email,))
        existing_user = cursor.fetchone()

        if not existing_user:
            cursor.execute(
                "INSERT INTO users (user_name, email, role) VALUES (%s, %s, %s)",
                (user_name, email, role)
            )
            conn.commit()
            st.success("Usuário cadastrado com Sucesso!")
            print("Usuário inserido com sucesso!")
        else:
            st.error("Usuário já cadastrado!")
            print("Usuário já existe no banco de dados.")

    except psycopg2.Error as e:
        print(f"Erro ao inserir usuário: {user_name}\n{e}")
    
    finally:
        cursor.close()
        conn.close()

def read_user(user_id):
    conn = create_connection()
    cursor = conn.cursor()

    create_user_table()  

    try:
        cursor.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
        existing_user = cursor.fetchone()

        if existing_user:
            user_info = {
                'id': existing_user[0],
                'user_name': existing_user[1], 
                'email': existing_user[2], 
                'role': existing_user[3],        
            }
            return user_info
        else:
            print("Usuário não existe no banco de dados.")

    except psycopg2.Error as e:
        print(f"Erro ao ler usuário:\n{e}")
    
    finally:
        cursor.close()
        conn.close()

def update_user(user_id, user_name=None, email=None, role=None):
    conn = create_connection()
    cursor = conn.cursor()

    create_user_table()  

    try:
        cursor.execute("SELECT * FROM users WHERE email = %s;", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            
            #campos a serem atualizados
            updates = []
            values = []

            if user_name:
                updates.append("user_name = %s")
                values.append(user_name)
            if email:
                updates.append("email = %s")
                values.append(email)
            if role:
                updates.append("role = %s")
                values.append(role)
            
            # checa se tem informacoes para atualizar
            if updates:
                values.append(user_id)  # Adiciona o user_id para a cláusula WHERE
                update_query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s;"
                cursor.execute(update_query, tuple(values))
                conn.commit()
                st.success("Usuário atualizado!")
                print(f"Usuário com ID {user_id} atualizado com sucesso!")
            else:
                print("Nenhuma informação nova fornecida para atualização.")
        else:
            print("Usuário não existe no banco de dados.")

    except psycopg2.Error as e:
        st.error("Usuário já existe!")
        print(f"Erro ao ler usuário:\n{e}")
    
    finally:
        cursor.close()
        conn.close()

def delete_user(user_id):
    conn = create_connection()
    cursor = conn.cursor()

    create_user_table()  

    try:
        cursor.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            conn.commit()
            st.success("Usuário excluído com sucesso")
        else:
            print("Usuário não existe no banco de dados.")

    except psycopg2.Error as e:
        st.error(f"Erro ao deletar usuário: {e}")
    
    finally:
        cursor.close()
        conn.close()

#  if not existing_user:
#    cursor.execute("INSERT INTO users (google_id, email) VALUES (%s, %s)", (google_id, email))
#    conn.commit()
  
#  cursor.close()
#  conn.close()

def get_user_by_email(email):
    try: 
        conn = create_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, user_name, email, role FROM users WHERE email = %s;",
            (email,)
        )

        user = cur.fetchone()

        cur.close()
        conn.close()

        if user:
            return {
                'user_id': user[0],  # Adicionando o user_id
                'user_name': user[1],
                'email': user[2],
                'role': user[3]
            }
        else:
            return None
    
    except psycopg2.Error as e:
        print(f"Erro ao buscar usuário: {e}")
        return None