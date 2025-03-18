import psycopg2
from services.database_connection import create_connection, table_exists

def create_vehicle_monthly_avg_table():
    if not table_exists("vehicle_monthly_avg"):
        conn = create_connection()
        cur = conn.cursor()

        cur.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'month_enum') THEN
                    CREATE TYPE month_enum AS ENUM (
                        'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
                        'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'
                    );
                END IF;
            END $$;
        """)

        cur.execute("""
            CREATE TABLE vehicle_monthly_avg (
                id SERIAL PRIMARY KEY,
                vehicle_id INTEGER REFERENCES vehicles(id) ON DELETE CASCADE,
                month month_enum NOT NULL,
                year INTEGER NOT NULL,
                avg_price DECIMAL(10,2) NOT NULL,
                UNIQUE (vehicle_id, month, year) -- Garante que não há duplicatas
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("Tabela 'vehicle_monthly_avg' criada com sucesso.")
    else:
        print("Tabela 'vehicle_monthly_avg' já existe.")


def calculate_and_store_monthly_avg():
    conn = create_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO vehicle_monthly_avg (vehicle_id, month, year, avg_price)
            SELECT 
                p.vehicle_id,
                CASE 
                    WHEN EXTRACT(MONTH FROM p.collect_date) = 1 THEN 'janeiro'
                    WHEN EXTRACT(MONTH FROM p.collect_date) = 2 THEN 'fevereiro'
                    WHEN EXTRACT(MONTH FROM p.collect_date) = 3 THEN 'março'
                    WHEN EXTRACT(MONTH FROM p.collect_date) = 4 THEN 'abril'
                    WHEN EXTRACT(MONTH FROM p.collect_date) = 5 THEN 'maio'
                    WHEN EXTRACT(MONTH FROM p.collect_date) = 6 THEN 'junho'
                    WHEN EXTRACT(MONTH FROM p.collect_date) = 7 THEN 'julho'
                    WHEN EXTRACT(MONTH FROM p.collect_date) = 8 THEN 'agosto'
                    WHEN EXTRACT(MONTH FROM p.collect_date) = 9 THEN 'setembro'
                    WHEN EXTRACT(MONTH FROM p.collect_date) = 10 THEN 'outubro'
                    WHEN EXTRACT(MONTH FROM p.collect_date) = 11 THEN 'novembro'
                    WHEN EXTRACT(MONTH FROM p.collect_date) = 12 THEN 'dezembro'
                END::month_enum AS month,
                EXTRACT(YEAR FROM p.collect_date) AS year,
                AVG(p.price) AS avg_price
            FROM prices p
            GROUP BY p.vehicle_id, month, year
            ON CONFLICT (vehicle_id, month, year)
            DO UPDATE SET avg_price = EXCLUDED.avg_price;
        """)
        conn.commit()
        print("Preços médios mensais armazenados com sucesso.")
    except psycopg2.Error as e:
        print(f"Erro ao calcular e armazenar preços médios mensais: {e}")
    finally:
        cur.close()
        conn.close()

def create_vehicle_monthly_avg(vehicle_id, month, year, avg_price):
    conn = create_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO vehicle_monthly_avg (vehicle_id, month, year, avg_price)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (vehicle_id, month, year)
            DO UPDATE SET avg_price = EXCLUDED.avg_price;
        """, (vehicle_id, month, year, avg_price))
        conn.commit()
        print("Registro inserido/atualizado com sucesso.")
    except psycopg2.Error as e:
        print(f"Erro ao inserir registro: {e}")
    finally:
        cur.close()
        conn.close()

def get_vehicle_monthly_avg(vehicle_id=None, year=None):
    conn = create_connection()
    cur = conn.cursor()
    try:
        query = "SELECT * FROM vehicle_monthly_avg WHERE 1=1"
        params = []

        if vehicle_id:
            query += " AND vehicle_id = %s"
            params.append(vehicle_id)

        if year:
            query += " AND year = %s"
            params.append(year)

        cur.execute(query, tuple(params))
        records = cur.fetchall()
        return records
    except psycopg2.Error as e:
        print(f"Erro ao buscar registros: {e}")
        return []
    finally:
        cur.close()
        conn.close()

def update_vehicle_monthly_avg(vehicle_id, month, year, new_avg_price):
    conn = create_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE vehicle_monthly_avg
            SET avg_price = %s
            WHERE vehicle_id = %s AND month = %s AND year = %s
        """, (new_avg_price, vehicle_id, month, year))
        conn.commit()
        print("Registro atualizado com sucesso.")
    except psycopg2.Error as e:
        print(f"Erro ao atualizar registro: {e}")
    finally:
        cur.close()
        conn.close()

def delete_vehicle_monthly_avg(vehicle_id, month, year):
    conn = create_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            DELETE FROM vehicle_monthly_avg
            WHERE vehicle_id = %s AND month = %s AND year = %s
        """, (vehicle_id, month, year))
        conn.commit()
        print("Registro deletado com sucesso.")
    except psycopg2.Error as e:
        print(f"Erro ao deletar registro: {e}")
    finally:
        cur.close()
        conn.close()