import psycopg2
import streamlit as st
from services.database_connection import create_connection, table_exists

def create_price_changes_table():
    if not table_exists("price_changes"):
        conn = create_connection()
        cur = conn.cursor()

        # Criar a tabela price_changes
        cur.execute("""
            CREATE TABLE IF NOT EXISTS price_changes (
                id SERIAL PRIMARY KEY,
                vehicle_id INTEGER REFERENCES vehicles(id) ON DELETE CASCADE
            );
        """)

        # Criar a função que será usada pelos triggers
        cur.execute("""
            CREATE OR REPLACE FUNCTION track_price_changes() RETURNS TRIGGER AS $$
            BEGIN
                -- Adiciona o veículo na price_changes se ainda não existir
                INSERT INTO price_changes (vehicle_id)
                SELECT NEW.vehicle_id
                WHERE NOT EXISTS (
                    SELECT 1 FROM price_changes WHERE vehicle_id = NEW.vehicle_id
                );
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)

        # Criar triggers para capturar INSERT, UPDATE e DELETE na tabela "prices"
        cur.execute("""
            CREATE OR REPLACE TRIGGER trigger_price_insert
            AFTER INSERT ON prices
            FOR EACH ROW EXECUTE FUNCTION track_price_changes();
        """)

        cur.execute("""
            CREATE OR REPLACE TRIGGER trigger_price_update
            AFTER UPDATE ON prices
            FOR EACH ROW EXECUTE FUNCTION track_price_changes();
        """)

        cur.execute("""
            CREATE OR REPLACE TRIGGER trigger_price_delete
            AFTER DELETE ON prices
            FOR EACH ROW EXECUTE FUNCTION track_price_changes();
        """)

        conn.commit()
        cur.close()
        conn.close()

        print("Tabela 'price_changes' e triggers criados com sucesso.")
    else:
        print("Tabela 'price_changes' já existe.")