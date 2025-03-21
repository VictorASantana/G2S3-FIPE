import streamlit as st
import psycopg2
from services.database_connection import create_connection, table_exists

def create_interpolation_query():
  if not table_exists('interpolation_query'):
    conn = create_connection()
    cur = conn.cursor()

    cur.execute("""
      CREATE TABLE interpolation_query (
        id SERIAL PRIMARY KEY,
        coefficient_a FLOAT NOT NULL,
        coefficient_b FLOAT NOT NULL,
        vehicle_id INTEGER REFERENCES vehicles(id) ON DELETE CASCADE,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        query_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    """)

    conn.commit()
    cur.close()
    print("Tabela 'interpolation_query' criada com sucesso.")
  else:
    print("Tabela 'interpolation_query' já existe.")

def insert_interpolation_query(query_data):
  conn = create_connection()
  cur = conn.cursor()
  try:

    cur.execute(
      """
        INSERT INTO interpolation_query (
          coefficient_a, coefficient_b, vehicle_id, user_id, query_date
        ) VALUES (%s, %s, %s, %s, NOW())
        RETURNING id;
      """,
      (query_data['a'].item(), query_data['b'].item(), query_data['vehicle_id'], query_data['user_id'])
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

def get_interpolation_query(query_id):
  conn = create_connection()
  cur = conn.cursor()

  try:
    cur.execute("SELECT * FROM interpolation_query WHERE id = %s", (query_id))
    return cur.fetchone()
  except psycopg2.Error as e:
    print(f"Erro ao buscar consulta: {e}")
  finally:
    cur.close()
    conn.close()

def get_interpolation_queries_by_user(user_id):
  conn = create_connection()
  cur = conn.cursor()
  try:
    cur.execute("SELECT * FROM interpolation_query WHERE user_id = %s ORDER BY query_date DESC;", (user_id,))
    queries = cur.fetchall()
    formatted_queries = []

    for query in queries:
      formatted_queries.append({
        "id": query[0],
        "coef_a": query[1],
        "coef_b": query[2],
        "vehicle_id": query[3],
        "query_date": query[5]
      })
    return formatted_queries
  except psycopg2.Error as e:
    print(f"Erro ao buscar consultas do usuário: {e}")
    return []
  finally:
    cur.close()
    conn.close()

def delete_interpolation_query(query_id):
    conn = create_connection()
    cur = conn.cursor()
    try:
      cur.execute("DELETE FROM interpolation_query WHERE id = %s;", (query_id))
      conn.commit()
    except psycopg2.Error as e:
      print(f"Erro ao deletar consulta: {e}")
    finally:
      cur.close()
      conn.close()
