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

def get_vehicles(model_id):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, model_year, average_price
        FROM vehicles WHERE model_id = %s ORDER BY model_year;
    """, (model_id,))
    vehicles = cur.fetchall()
    cur.close()
    conn.close()
    return vehicles

def update_vehicle(vehicle_id, model_id, fabrication_year, model_year):
    conn = create_connection()
    cur = conn.cursor()
    
    cur.execute("""
        UPDATE vehicles 
        SET model_id = %s, fabrication_year = %s, model_year = %s
        WHERE id = %s;
    """, (model_id, fabrication_year, model_year, vehicle_id))
    
    conn.commit()
    cur.close()
    conn.close()
    return f"Veículo {vehicle_id} atualizado com sucesso."

def delete_vehicle(vehicle_id):
    conn = create_connection()
    cur = conn.cursor()
    
    cur.execute("DELETE FROM vehicles WHERE id = %s;", (vehicle_id,))
    conn.commit()
    
    cur.close()
    conn.close()
    return f"Veículo {vehicle_id} deletado com sucesso."