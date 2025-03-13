from services.database_connection import create_connection, table_exists
from utils.auth import get_logged_in_user_id

def create_prices_table():
    if not table_exists("prices"):
        conn = create_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS prices (
                id SERIAL PRIMARY KEY,
                vehicle_id INTEGER REFERENCES vehicles(id) ON DELETE CASCADE,
                store_id INTEGER REFERENCES store(id) ON DELETE CASCADE,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                price DECIMAL(10, 2) NOT NULL,
                collect_date TIMESTAMP NOT NULL
            );
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        
        print("Tabela 'prices' criada com sucesso.")
    else: 
        print("Tabela 'prices' já existe.")

def save_price(store_id, vehicle_id, price, collect_date, user_id):
    user_id = get_logged_in_user_id()
    print(f"Usuário logado: {user_id}")  # 🔍 Debug

    if not user_id:
        print("Erro: Usuário não autenticado.")
        return "Erro: Usuário não autenticado."

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO prices (store_id, vehicle_id, user_id, price, collect_date)
        VALUES (%s, %s, %s, %s, %s);
    """, (store_id, vehicle_id, user_id, price, collect_date))
    conn.commit()
    conn.close()

def update_price(price_id, new_price, new_collect_date, user_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE prices
        SET price = %s, collect_date = %s
        WHERE id = %s AND user_id = %s;
    """, (new_price, new_collect_date, price_id, user_id))
    
    if cursor.rowcount == 0:
        conn.close()
        return "Erro: Você não tem permissão para editar este preço."

    conn.commit()
    conn.close()
    return "Preço atualizado com sucesso!"

def delete_price(price_id, user_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM prices
        WHERE id = %s AND user_id = %s;
    """, (price_id, user_id))
    
    if cursor.rowcount == 0:
        conn.close()
        return "Erro: Você não tem permissão para excluir este preço."

    conn.commit()
    conn.close()
    return "Preço excluído com sucesso!"

def get_prices_by_user(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, s.name AS store_name, b.name AS brand_name, m.name AS model_name, 
               v.model_year, p.price, p.collect_date
        FROM prices p
        JOIN store s ON p.store_id = s.id
        JOIN vehicles v ON p.vehicle_id = v.id
        JOIN model m ON v.model_id = m.id
        JOIN brand b ON m.brand_id = b.id
        WHERE p.user_id = %s
        ORDER BY p.collect_date DESC;
    """, (user_id,))
    
    prices = cursor.fetchall()
    conn.close()
    return prices
