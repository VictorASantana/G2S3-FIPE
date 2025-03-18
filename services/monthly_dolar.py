from services.database_connection import create_connection, table_exists
import psycopg2
import streamlit as st

def create_monthly_dolar_table():
    if not table_exists("monthly_dolar"):
        conn = create_connection()
        cur = conn.cursor()

        # Criando o tipo ENUM se ainda não existir
        cur.execute("""
            DO $$ 
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'month_enum') THEN
                    CREATE TYPE month_enum AS ENUM ( 'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
                         'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro');
                END IF;
            END $$;
        """)

        cur.execute("""
            CREATE TABLE monthly_dolar (
                id SERIAL PRIMARY KEY,
                month month_enum NOT NULL,
                year INTEGER NOT NULL,
                value DECIMAL(10,2) NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("Tabela 'monthly_dolar' criada com sucesso.")
    else: 
        print("Tabela 'monthly_dolar' já existe.")

def create_month_dolar(month, year, value):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO monthly_dolar (month, year, value) VALUES (%s, %s, %s)
        """, (month, year, value))
        conn.commit()
        st.success("Entrada inserida com sucesso!")
        print("Entrada inserida com sucesso!")
    except psycopg2.Error as e:
        print(f"Erro ao inserir entrada: {e}")
    finally:
        cursor.close()
        conn.close()

def read_monthly_dolar(entry_id):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM monthly_dolar WHERE id = %s;", (entry_id,))
        entry = cursor.fetchone()

        if entry:
            return {
                'id': entry[0],
                'month': entry[1],
                'year': entry[2],
                'value': entry[3]
            }
        else:
            print("Entrada não encontrada.")
    except psycopg2.Error as e:
        print(f"Erro ao buscar entrada: {e}")
    finally:
        cursor.close()
        conn.close()

def update_monthly_dolar(entry_id, month=None, year=None, value=None):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM monthly_dolar WHERE id = %s;", (entry_id,))
        existing_entry = cursor.fetchone()

        if existing_entry:
            updates = []
            values = []

            if month and month != existing_entry[1]:
                updates.append("month = %s")
                values.append(month)
            if year and year != existing_entry[2]:
                updates.append("year = %s")
                values.append(year)
            if value and value != existing_entry[3]:
                updates.append("value = %s")
                values.append(value)
            
            if updates:
                values.append(entry_id)
                update_query = f"UPDATE monthly_dolar SET {', '.join(updates)} WHERE id = %s;"
                cursor.execute(update_query, tuple(values))
                conn.commit()
                st.success("Entrada atualizada com sucesso!")
                print("Entrada atualizada com sucesso!")
            else:
                print("Nenhuma atualização necessária.")
        else:
            print("Entrada não encontrada.")
    except psycopg2.Error as e:
        print(f"Erro ao atualizar entrada: {e}")
    finally:
        cursor.close()
        conn.close()

def delete_monthly_dolar(entry_id):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM monthly_dolar WHERE id = %s;", (entry_id,))
        existing_entry = cursor.fetchone()

        if existing_entry:
            cursor.execute("DELETE FROM monthly_dolar WHERE id = %s;", (entry_id,))
            conn.commit()
            print("Entrada removida com sucesso!")
        else:
            print("Entrada não encontrada.")
    except psycopg2.Error as e:
        print(f"Erro ao remover entrada: {e}")
    finally:
        cursor.close()
        conn.close()

def get_dolar_values_between_dates(start_year, start_month, end_year, end_month):
    """

    """
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, month, year, value FROM monthly_dolar
            WHERE (year > %s OR (year = %s AND month >= %s::month_enum))
            AND (year < %s OR (year = %s AND month <= %s::month_enum))
            ORDER BY year, month;
        """, (start_year, start_year, start_month, end_year, end_year, end_month))

        results = cursor.fetchall()

        if not results:
            print("Nenhum dado encontrado para o período especificado.")
        else:
            for row in results:
                print(row)

        return results

    except psycopg2.Error as e:
        print(f"Erro ao buscar valores do dólar:\n{e}")

    finally:
        cursor.close()
        conn.close()