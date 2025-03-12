from services.database_connection import create_connection, table_exists

def create_model_table():
    if not table_exists("model"):
        conn = create_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE model (
                id SERIAL PRIMARY KEY,
                brand_id INT REFERENCES brand(id),
                name TEXT UNIQUE NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("Tabela 'model' criada com sucesso.")
    else: 
        print("Tabela 'model' já existe.")

def get_models_by_brand(brand_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM model WHERE brand_id = %s;", (brand_id,))
    models = cursor.fetchall()
    conn.close()
    return models