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

#def insert_user(google_id, email):
#  conn = init_connection()
#  cursor = conn.cursor()

#  create_user_table()

#  cursor.execute("SELECT * FROM users WHERE google_id = %s;", (google_id,))
#  existing_user = cursor.fetchone()

#  if not existing_user:
#    cursor.execute("INSERT INTO users (google_id, email) VALUES (%s, %s)", (google_id, email))
#    conn.commit()
  
#  cursor.close()
#  conn.close()