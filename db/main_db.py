import sqlite3
from db import queries

db_store = sqlite3.connect('db/store.sqlite3')
cursor = db_store.cursor()


async def sql_insert_store_products(model_name, category, size_1, price, product_id, photo):
    cursor.execute(queries.INSERT_store_products_QUERY, (
        model_name, category, size_1, price, product_id, photo
    ))
    db_store.commit()


async def sql_insert_orders(model_name, category, size_1, price, product_id, photo):
    cursor.execute(queries.INSERT_orders_QUERY, (
        model_name, category, size_1, price, product_id, photo
    ))


def get_db_connection():
    return sqlite3.connect('db/store.sqlite3')


def fetch_all_products():
    conn = get_db_connection()
    products = conn.execute("""
        SELECT * FROM store_products
    """).fetchall()
    conn.close()
    return products


