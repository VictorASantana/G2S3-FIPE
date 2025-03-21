import psycopg2
from datetime import datetime
from database_connection import create_connection

def insert_brands():
    conn = create_connection()
    cur = conn.cursor()

    brands = ["Chevrolet", "Ford", "Fiat", "Volkswagen", "Toyota", "Honda", "Hyundai", "Renault", "Peugeot", "Nissan"]
    for brand in brands:
        cur.execute("INSERT INTO brand (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;", (brand,))
    
    conn.commit()
    cur.close()
    conn.close()
    print("Marcas inseridas com sucesso!")

def insert_models():
    conn = create_connection()
    cur = conn.cursor()

    models = [
        (1, "Onix"), (1, "Cruze"), (2, "Fiesta"), (2, "Focus"), (3, "Palio"),
        (3, "Uno"), (4, "Gol"), (4, "Polo"), (5, "Corolla"), (6, "Civic")
    ]
    
    for brand_id, model_name in models:
        cur.execute("INSERT INTO model (brand_id, name) VALUES (%s, %s) ON CONFLICT (name) DO NOTHING;", (brand_id, model_name))
    
    conn.commit()
    cur.close()
    conn.close()
    print("Modelos inseridos com sucesso!")

def insert_vehicles():
    conn = create_connection()
    cur = conn.cursor()

    vehicles = [
        (1, 2020, 2021, 75000.00), (2, 2019, 2020, 65000.00), (3, 2021, 2021, 80000.00),
        (4, 2018, 2019, 55000.00), (5, 2022, 2023, 95000.00)
    ]
    
    for model_id, fabrication_year, model_year, average_price in vehicles:
        cur.execute("""
            INSERT INTO vehicles (model_id, fabrication_year, model_year, average_price)
            VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING;
        """, (model_id, fabrication_year, model_year, average_price))
    
    conn.commit()
    cur.close()
    conn.close()
    print("Veículos inseridos com sucesso!")

def insert_users():
    conn = create_connection()
    cur = conn.cursor()

    users = [
        ("gestor1", "gestor1@email.com", "gestor"),
        ("pesquisador1", "pesquisador1@email.com", "pesquisador"),
        ("gestor2", "gestor2@email.com", "gestor"),
        ("pesquisador2", "pesquisador2@email.com", "pesquisador")
    ]
    
    for user_name, email, role in users:
        cur.execute("""
            INSERT INTO users (user_name, email, role)
            VALUES (%s, %s, %s) ON CONFLICT (email) DO NOTHING;
        """, (user_name, email, role))
    
    conn.commit()
    cur.close()
    conn.close()
    print("Usuários inseridos com sucesso!")

# def insert_stores():
#     conn = create_connection()
#     cur = conn.cursor()

#     stores = [
#         (1, "AutoCar SP", "SP"), (2, "Veículos RJ", "RJ"),
#         (3, "TopCar MG", "MG"), (4, "Mega Autos SC", "SC")
#     ]
    
#     for user_id, name, state in stores:
#         cur.execute("""
#             INSERT INTO store (user_id, name, state)
#             VALUES (%s, %s, %s) ON CONFLICT (name) DO NOTHING;
#         """, (user_id, name, state))
    
#     conn.commit()
#     cur.close()
#     conn.close()
#     print("Lojas inseridas com sucesso!")

def insert_prices():
    conn = create_connection()
    cur = conn.cursor()

    prices = [
        (1, 1, 72000.00, datetime.now()), (2, 2, 63000.00, datetime.now()),
        (3, 3, 78000.00, datetime.now()), (4, 4, 54000.00, datetime.now()),
        (5, 1, 92000.00, datetime.now())
    ]
    
    for vehicle_id, store_id, price, collect_date in prices:
        cur.execute("""
            INSERT INTO prices (vehicle_id, store_id, price, collect_date)
            VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING;
        """, (vehicle_id, store_id, price, collect_date))
    
    conn.commit()
    cur.close()
    conn.close()
    print("Preços inseridos com sucesso!")

if __name__ == "__main__":
    insert_brands()
    insert_models()
    insert_vehicles()
    insert_users()
    #insert_stores()
    insert_prices()

    print("Banco de dados populado com sucesso!")