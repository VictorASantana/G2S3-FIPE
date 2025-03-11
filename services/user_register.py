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
                    CREATE TYPE user_role AS ENUM ('gestor', 'pesquisador');
                END IF;
            END $$;
        """)

        cur.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                user_name TEXT UNIQUE NOT NULL,
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
            print("Usuário inserido com sucesso!")
        else:
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
                print(f"Usuário com ID {user_id} atualizado com sucesso!")
            else:
                print("Nenhuma informação nova fornecida para atualização.")
        else:
            print("Usuário não existe no banco de dados.")

    except psycopg2.Error as e:
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
            print("Usuário removido com sucesso!")
        else:
            print("Usuário não existe no banco de dados.")

    except psycopg2.Error as e:
        print(f"Erro ao remover usuário {user_id}:\n{e}")
    
    finally:
        cursor.close()
        conn.close()