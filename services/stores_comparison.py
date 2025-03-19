from services.database_connection import create_connection, table_exists
from services.vehicles import get_all_vehicles_info
from services.store import get_all_stores_info
from services.prices import get_vehicle_ids_by_store_id

import psycopg2
import streamlit as st
from datetime import datetime

def create_stores_comp_table():
    if not table_exists("stores_comp"):
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
            CREATE TABLE stores_comp (
                id SERIAL PRIMARY KEY,
                user_email TEXT REFERENCES users(email),
                first_store INT REFERENCES store(id),
                second_store INT REFERENCES store(id),
                vehicle_id INT REFERENCES vehicles(id),
                start_month month_enum NOT NULL,
                start_year INT NOT NULL,
                end_month month_enum NOT NULL,
                end_year INT NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("Tabela 'stores_comp' criada com sucesso.")
    else: 
        print("Tabela 'stores_comp' já existe.")

def create_stores_comparison(user_email, first_store, second_store, vehicle_id, start_month, start_year, end_month, end_year):
    conn = create_connection()
    cursor = conn.cursor()

    create_stores_comp_table()  

    try:
        cursor.execute("""
                        SELECT * FROM stores_comp  
                        WHERE user_email = %s AND first_store = %s AND second_store = %s AND 
                              vehicle_id = %s AND start_month = %s AND start_year = %s AND end_month = %s AND end_year = %s;""", 
                        (user_email, first_store, second_store, vehicle_id, start_month, start_year, end_month, end_year)
                    )
        existing_comparison = cursor.fetchone()

        if not existing_comparison:
            if vehicle_id in get_all_vehicles_info(info="id") or first_store not in get_all_stores_info(info="id") or second_store not in get_all_stores_info(info="id"): 
                if vehicle_id in get_vehicle_ids_by_store_id(first_store) and vehicle_id in get_vehicle_ids_by_store_id(second_store):
                    cursor.execute(
                        """INSERT INTO stores_comp (user_email, first_store, second_store, vehicle_id, start_month, start_year, end_month, end_year) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        (user_email, first_store, second_store, vehicle_id, start_month, start_year, end_month, end_year)
                    )
                    conn.commit()
                    #st.success("Loja inserida com sucesso!")
                    print("Comparação inserida com sucesso!")
                else:
                    print("Comparação inválida! Selecione um veículo existente nas duas lojas.")
            else: 
                print("Comparação inválida! Selecione um veículo e lojas existentes.")
        else:
            #st.error("Loja já existe no banco de dados.")
            print("Comparação já existe no banco de dados.")

    except psycopg2.Error as e:
        print(f"Erro ao inserir nova comparação:\n{e}")
    
    finally:
        cursor.close()
        conn.close()

def read_store_comparison(comparison_id):
    conn = create_connection()
    cursor = conn.cursor()

    create_stores_comp_table()  

    try:
        cursor.execute("SELECT * FROM stores_comp WHERE id = %s;", (comparison_id,))
        existing_comparison = cursor.fetchone()
        if existing_comparison: 
            comparison_info = {
                'id': existing_comparison[0],
                'user_email': existing_comparison[1],
                'first_store': existing_comparison[2],
                'second_store': existing_comparison[3],
                'vehicle_id': existing_comparison[4],
                'start_month': existing_comparison[5],
                'start_year': existing_comparison[6],
                'end_month': existing_comparison[7],
                'end_year': existing_comparison[8]        
            }
            return comparison_info
        else:
            print("Comparação não existe no banco de dados.")

    except psycopg2.Error as e:
        print(f"Erro ao ler comparação:\n{e}")
    
    finally:
        cursor.close()
        conn.close()

def get_non_empty_updated_values(comparison_id, first_store, second_store, vehicle_id, start_month, start_year, end_month, end_year):

    new_current_values = read_store_comparison(comparison_id)
    print("old: ")
    print(new_current_values)
    if first_store:
        new_current_values["first_store"] = first_store
    if second_store:
        new_current_values["second_store"] = second_store
    if vehicle_id:
        new_current_values["vehicle_id"] = vehicle_id
    if start_month:
        new_current_values["start_month"] = start_month
    if start_year:
        new_current_values["start_year"] = start_year
    if end_month:
        new_current_values["end_month"] = end_month
    if end_year:
        new_current_values["end_year"] = end_year
    
    return new_current_values

def update_comparison(comparison_id, user_email, first_store, second_store, vehicle_id, start_month, start_year, end_month, end_year):
    conn = create_connection()
    cursor = conn.cursor()

    create_stores_comp_table()  

    try:
        cursor.execute("SELECT * FROM store WHERE id = %s;", (comparison_id,))
        existing_store = cursor.fetchone()

        if existing_store:
            new_current_values = get_non_empty_updated_values(comparison_id, first_store, second_store, vehicle_id, start_month, start_year, end_month, end_year)
            print("new: ")
            print(new_current_values)
            cursor.execute("""
                    UPDATE stores_comp
                    SET first_store = %s, second_store = %s, vehicle_id = %s, start_month = %s, start_year = %s, end_month = %s, end_year = %s
                    WHERE id = %s AND user_email = %s;
                """, 
                (new_current_values["first_store"], new_current_values["second_store"], new_current_values["vehicle_id"], new_current_values["start_month"], 
                new_current_values["start_year"], new_current_values["end_month"], new_current_values["end_year"], comparison_id, user_email)
            )
            conn.commit()
        else:
            print("Comparação não existe no banco de dados.")

    except psycopg2.Error as e:
        print(f"Erro ao ler comparação:\n{e}")
    
    finally:
        cursor.close()
        conn.close()

def delete_comparison(comparison_id):
    conn = create_connection()
    cursor = conn.cursor()

    create_stores_comp_table()  

    try:
        cursor.execute("SELECT * FROM stores_comp WHERE id = %s;", (comparison_id,))
        existing_comparison = cursor.fetchone()

        if existing_comparison:
            cursor.execute("DELETE FROM stores_comp WHERE id = %s;", (comparison_id,))
            conn.commit()
            print("Comparação removida com sucesso!")
        else:
            print("Comparação não existe no banco de dados.")

    except psycopg2.Error as e:
        print(f"Erro ao remover comparação {comparison_id}:\n{e}")
    
    finally:
        cursor.close()
        conn.close()

def get_avg_price_by_month_given_vehicle_store(vehicle_id, store_id, start_month, start_year, end_month, end_year):
    
    month_to_int = {
        'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4, 'maio': 5, 'junho': 6,
        'julho': 7, 'agosto': 8, 'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
    }

    start_date = datetime(start_year, month_to_int[start_month], 1)
    end_date = datetime(end_year, month_to_int[end_month], 30)

    start_string = start_date.strftime('%Y-%m-%d %H:%M:%S')
    end_string = end_date.strftime('%Y-%m-%d %H:%M:%S')

    conn = create_connection()
    cur = conn.cursor()

    try:
        query = """
            SELECT EXTRACT(MONTH FROM collect_date) AS month,
                   EXTRACT(YEAR FROM collect_date) AS year,
                   AVG(price) AS avg_price
            FROM prices 
            WHERE vehicle_id = %s
            AND store_id = %s
            AND collect_date >= %s
            AND collect_date <= %s
            GROUP BY year, month
            ORDER BY year, month;
        """
        cur.execute(query, (vehicle_id, store_id, f"{start_string}", f"{end_string}"))
        results = cur.fetchall()

        avg_prices = {}
        for row in results:
            month_name = {
                1: 'janeiro', 2: 'fevereiro', 3: 'março', 4: 'abril', 5: 'maio', 6: 'junho',
                7: 'julho', 8: 'agosto', 9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'
            }.get(int(row[0]), 'Unknown')  

            avg_prices[f"{int(row[1])}/{month_name}"] = row[2]
            
        return avg_prices

    except psycopg2.Error as e:
        print(f"Erro ao calcular e armazenar preços médios mensais: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def get_all_comparisons():
    conn = create_connection()
    cursor = conn.cursor()

    try: 
        cursor.execute("SELECT * FROM stores_comp")
        comparisons = cursor.fetchall()
        formatted_comparisons = []
        for comparison in comparisons:
            formatted_comparisons.append({
                "id": comparison[0],
                "user_email": comparison[1],
                "Loja 1": comparison[2],
                "Loja 2": comparison[3],
                "Veículo": comparison[4],
                "Mês Inicial": comparison[5],
                "Ano Inicial": comparison[6],
                "Mês Final": comparison[7],
                "Ano Final": comparison[8],
            })
        return formatted_comparisons

    except psycopg2.Error as e:
        print(f"Erro ao buscar comparações: {e}")
        return None

    finally:
        cursor.close()
        conn.close()

def get_all_comparisons_by_email(email):
    conn = create_connection()
    cursor = conn.cursor()

    try: 
        cursor.execute("SELECT * FROM stores_comp WHERE user_email = %s", (email,))
        comparisons = cursor.fetchall()
        formatted_comparisons = []
        for comparison in comparisons:
            formatted_comparisons.append({
                "id": comparison[0],
                "user_email": comparison[1],
                "Loja 1": comparison[2],
                "Loja 2": comparison[3],
                "Veículo": comparison[4],
                "Mês Inicial": comparison[5],
                "Ano Inicial": comparison[6],
                "Mês Final": comparison[7],
                "Ano Final": comparison[8],
            })
        return formatted_comparisons

    except psycopg2.Error as e:
        print(f"Erro ao buscar comparações: {e}")
        return None

    finally:
        cursor.close()
        conn.close()