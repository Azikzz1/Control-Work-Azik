CREATE_TABLE_store_products = """
    CREATE TABLE IF NOT EXISTS store_products(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT,
    category TEXT,
    size_1 TEXT,
    price TEXT,
    product_id INTEGER,
    photo TEXT
    )
"""

INSERT_store_products_QUERY = """
    INSERT INTO store_products (model_name, category, size_1, price, product_id, photo)
    VALUES (?, ?, ?, ?, ?, ?)
"""
