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

def create_model(brand_id, name):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO model (brand_id, name) VALUES (%s, %s) RETURNING id;", (brand_id, name))
    model_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return model_id

def get_models(brand_id):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM model WHERE brand_id = %s ORDER BY name;", (brand_id,))
    models = cur.fetchall()
    cur.close()
    conn.close()
    return models