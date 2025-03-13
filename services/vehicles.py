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
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id FROM vehicles
            WHERE model_id = %s
            AND fabrication_year = %s
            AND model_year = %s;
        """, (model_id, fabrication_year, model_year))
        
        existing_vehicle = cursor.fetchone()

        if existing_vehicle:
            print("Erro: Já existe um veículo com esse ano de fabricação e modelo.")
            return "Erro: Já existe um veículo com esse ano de fabricação e modelo."
        
        cursor.execute("""
            INSERT INTO vehicles (model_id, fabrication_year, model_year, average_price)
            VALUES (%s, %s, %s, %s);
        """, (model_id, fabrication_year, model_year, average_price))
        
        conn.commit()
        return "Veículo cadastrado com sucesso!"

    except psycopg2.Error as e:
        return f"Erro ao inserir veículo: {e}"
    
    finally:
        cursor.close()
        conn.close()

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