from services.database_connection import create_connection, table_exists

def create_brand_table():
    if not table_exists("brand"):
        conn = create_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS brand (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL
            );
        """)
        
        conn.commit()
        conn.commit()
        cur.close()
        conn.close()
        
        print("Tabela 'brand' criada com sucesso.")
    else: 
        print("Tabela 'brand' já existe.")

def create_brand(name):
    conn = create_connection()
    cur = conn.cursor()
    
    cur.execute("INSERT INTO brand (name) VALUES (%s) RETURNING id;", (name,))
    brand_id = cur.fetchone()[0]
    
    conn.commit()
    cur.close()
    conn.close()
    return brand_id

def get_brands():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM brand ORDER BY name;")
    brands = cur.fetchall()
    cur.close()
    conn.close()
    return brands

def get_brand_id_by_name(name):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT id FROM brand WHERE name = %s;", (name,))
    brand_id = cur.fetchone()[0]
    cur.close()
    conn.close()
    return brand_id

def update_brand(brand_id, new_name):
    conn = create_connection()
    cur = conn.cursor()
    
    cur.execute("UPDATE brand SET name = %s WHERE id = %s;", (new_name, brand_id))
    conn.commit()
    
    cur.close()
    conn.close()
    return f"Marca {brand_id} atualizada para {new_name} com sucesso."

def delete_brand(brand_id):
    conn = create_connection()
    cur = conn.cursor()
    
    cur.execute("DELETE FROM brand WHERE id = %s;", (brand_id,))
    conn.commit()
    
    cur.close()
    conn.close()
    return f"Marca {brand_id} deletada com sucesso."

