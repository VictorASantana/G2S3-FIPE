from services.database_connection import create_connection, table_exists

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
                name TEXT UNIQUE NOT NULL,
                state store_state NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("Tabela 'store' criada com sucesso.")
    else: 
        print("Tabela 'store' já existe.")

