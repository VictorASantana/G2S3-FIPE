import psycopg2
import streamlit as st

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
    
    try:
        cur.execute("""
            SELECT id FROM vehicles
            WHERE model_id = %s
            AND fabrication_year = %s
            AND model_year = %s;
        """, (model_id, fabrication_year, model_year))
        
        existing_vehicle = cur.fetchone()

        if existing_vehicle:
            st.error("Erro: Já existe um veículo com esse ano de fabricação e modelo.")
            return "Erro: Já existe um veículo com esse ano de fabricação e modelo."
        
        cur.execute("""
            UPDATE vehicles
            SET model_id = %s, fabrication_year = %s, model_year = %s
            WHERE id = %s;
        """, (model_id, fabrication_year, model_year, vehicle_id))
        
        conn.commit()
        st.success("Veículo atualizado com sucesso!")
        return f"Veículo {vehicle_id} atualizado com sucesso."

    except psycopg2.Error as e:
        return f"Erro ao inserir veículo: {e}"
    
    finally:
        cur.close()
        conn.close()
    
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

def update_vehicle_average_price():
    conn = create_connection()
    cur = conn.cursor()
    
    try:
       
        cur.execute("""
            UPDATE vehicles
            SET average_price = subquery.avg_price
            FROM (
                SELECT p.vehicle_id, AVG(p.price) AS avg_price
                FROM prices p
                WHERE p.vehicle_id IN (SELECT vehicle_id FROM price_changes)
                GROUP BY p.vehicle_id
            ) AS subquery
            WHERE vehicles.id = subquery.vehicle_id;
        """)

        cur.execute("DELETE FROM price_changes;")

        conn.commit()
        print("Preço médio atualizado para os veículos alterados. Alterações resetadas.")
    except Exception as e:
        print(f"Erro ao atualizar preços médios: {e}")
    finally:
        cur.close()
        conn.close()

def get_avg_price(model_id, model_year): 
    """Retorna o preco medio a partir das informocoes de busca -> ("marca" "modelo" "veiculo")"""
    
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT average_price
            FROM vehicles
            WHERE model_id = %s AND model_year = %s;
        """, (model_id, model_year))
        avg_price = cursor.fetchone()[0]
        return avg_price

    except psycopg2.Error as e:
        print(f"Erro ao buscar preço das vehicles: {e}")
        return []

    finally:
        cursor.close()
        conn.close()  

def get_all_vehicles_info(info="id"): 
    """Retorna uma lista com todos os "info" dos veiculos."""
    
    info_list = ['id', 'model_id', 'fabrication_year', 'model_year', 'average_price']
    try:
        idx = info_list.index(info) 
    except ValueError:
        print(f"'{info}' not found in the vehicles table.")
        return None

    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT {info} FROM vehicles;")
        vehicle_info = [row[0] for row in cursor.fetchall()]
        return vehicle_info

    except psycopg2.Error as e:
        print(f"Erro ao buscar {info} dos vehicles: {e}")
        return []

    finally:
        cursor.close()
        conn.close()

def get_vehicle_details(vehicle_id):
    conn = create_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT v.id, b.name AS brand, m.name AS model, v.model_year
            FROM vehicles v
            JOIN model m ON v.model_id = m.id
            JOIN brand b ON m.brand_id = b.id
            WHERE v.id = %s;
        """, (vehicle_id,))
        
        vehicle = cur.fetchone()

        if vehicle:
            return {"id": vehicle[0], "brand": vehicle[1], "model": vehicle[2], "year": vehicle[3]}
        else:
            return None
    except psycopg2.Error as e:
        print(f"Erro ao buscar detalhes do veículo: {e}")
        return None
    finally:
        cur.close()
        conn.close()