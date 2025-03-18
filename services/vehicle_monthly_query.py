import psycopg2
from services.database_connection import create_connection, table_exists

def create_vehicle_monthly_query_table():
    if not table_exists("vehicle_monthly_query"):
        conn = create_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE vehicle_monthly_query (
                id SERIAL PRIMARY KEY,
                vehicle1_id INTEGER REFERENCES vehicles(id) ON DELETE CASCADE,
                vehicle2_id INTEGER REFERENCES vehicles(id) ON DELETE CASCADE,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                start_month month_enum NOT NULL,
                end_month month_enum NOT NULL,
                start_year INTEGER NOT NULL,
                end_year INTEGER NOT NULL,
                query_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        print("Tabela 'vehicle_monthly_query' criada com sucesso.")
    else:
        print("Tabela 'vehicle_monthly_query' já existe.")

if __name__ == "__main__":
    create_vehicle_monthly_query_table()

def create_vehicle_monthly_query(query_data):
    conn = create_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO vehicle_monthly_query (
                vehicle1_id, vehicle2_id, user_id, start_month, end_month,
                start_year, end_year, query_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
            RETURNING id;
            """,
            (
                query_data["vehicle1_id"], query_data["vehicle2_id"], query_data["user_id"],
                query_data["start_month"], query_data["end_month"],
                query_data["start_year"], query_data["end_year"]
            )
        )
        query_id = cur.fetchone()[0]
        conn.commit()
        return query_id
    except psycopg2.Error as e:
        print(f"Erro ao inserir consulta: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def get_vehicle_monthly_query(query_id):
    conn = create_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM vehicle_monthly_query WHERE id = %s;", (query_id,))
        return cur.fetchone()
    except psycopg2.Error as e:
        print(f"Erro ao buscar consulta: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def get_queries_by_user(user_id):
    conn = create_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM vehicle_monthly_query WHERE user_id = %s ORDER BY query_date DESC;", (user_id,))
        return cur.fetchall()
    except psycopg2.Error as e:
        print(f"Erro ao buscar consultas do usuário: {e}")
        return []
    finally:
        cur.close()
        conn.close()

def delete_vehicle_monthly_query(query_id):
    conn = create_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM vehicle_monthly_query WHERE id = %s;", (query_id,))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Erro ao deletar consulta: {e}")
    finally:
        cur.close()
        conn.close()
