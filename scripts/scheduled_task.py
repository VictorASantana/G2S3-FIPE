import psycopg2
import datetime
import streamlit as st
#from services.database_connection import create_connection, table_exists

DB_CONFIG = {
    "dbname": st.secrets["DB_NAME"],
    "user": st.secrets["DB_USER"],
    "password": st.secrets["DB_PASSWORD"],
    "host": st.secrets["DB_HOST"],
    "port": st.secrets["DB_PORT"]
}

def calculate_average_price(vehicle_id):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Buscar preços para o veículo
    cursor.execute('SELECT price FROM prices WHERE vehicle_id = %s', (vehicle_id,))
    prices = cursor.fetchall()

    conn.close()

    if prices:
        average_price = sum(price[0] for price in prices) / len(prices)
        return average_price
    return None

def update_vehicle_averages():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Buscar todos os veículos
    cursor.execute('SELECT id FROM vehicles')
    vehicles = cursor.fetchall()

    for vehicle in vehicles:
        vehicle_id = vehicle[0]
        average_price = calculate_average_price(vehicle_id)

        if average_price:
            # Atualizar o valor médio no banco de dados
            cursor.execute('''
                UPDATE vehicles
                SET average_price = %s, last_updated = %s
                WHERE id = %s
            ''', (average_price, datetime.datetime.now(), vehicle_id))

    # Salvar as alterações e fechar a conexão
    conn.commit()
    conn.close()

    print('Valores médios atualizados com sucesso!')

if __name__ == '__main__':
    update_vehicle_averages()