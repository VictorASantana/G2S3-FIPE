from services.database_connection import create_connection
from services.user_register import create_user_table
from services.brand import create_brand_table
from services.model import create_model_table
from services.vehicles import create_vehicles_table
from services.store import create_store_table
from services.prices import create_prices_table
from services.price_changes import create_price_changes_table
from services.monthly_dolar import create_monthly_dolar_table
from services.vehicle_monthly_avg import create_vehicle_monthly_avg_table
from services.vehicle_monthly_query import create_vehicle_monthly_query_table

def create_all_tables():
    create_connection()
    try:
        create_user_table()
        create_brand_table()
        create_model_table()
        create_vehicles_table()
        create_store_table()
        create_prices_table()
        create_price_changes_table()
        create_monthly_dolar_table()
        create_vehicle_monthly_avg_table()
        create_vehicle_monthly_query_table()
        print("Todas as tabelas foram criadas com sucesso.")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")