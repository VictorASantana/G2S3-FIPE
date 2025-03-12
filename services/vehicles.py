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

# CREATE - Adicionar um novo veículo
def create_vehicle(model_id, fabrication_year, model_year, average_price):
    conn = create_connection()
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO vehicles (model_id, fabrication_year, model_year, average_price)
        VALUES (%s, %s, %s, %s) RETURNING id;
    """, (model_id, fabrication_year, model_year, average_price))
    
    vehicle_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return vehicle_id

# READ -
def get_vehicles(model_id):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, fabrication_year, model_year 
        FROM vehicles WHERE model_id = %s ORDER BY model_year;
    """, (model_id,))
    vehicles = cur.fetchall()
    cur.close()
    conn.close()
    return vehicles