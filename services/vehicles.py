from services.database_connection import create_connection, table_exists

def create_vehicles_table():
    if not table_exists("vehicles"):
        conn = create_connection()
        cur = conn.cursor()
       
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vehicles (
                id SERIAL PRIMARY KEY,
                model_id INTEGER REFERENCES model(id) ON DELETE CASCADE,
                fabrication_year INTEGER NOT NULL,
                model_year INTEGER NOT NULL,
                average_price DECIMAL(10,2)
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("Tabela 'vehicles' criada com sucesso.")
    else: 
        print("Tabela 'vehicles' já existe.")  

def get_vehicles_by_model(model_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, fabrication_year, model_year, average_price
        FROM vehicles
        WHERE model_id = %s;
    """, (model_id,))
    vehicles = cursor.fetchall()
    conn.close()
    return vehicles      