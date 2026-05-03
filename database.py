import sqlite3
def init_db():
    conn = sqlite3.connect("inventory.db")
    cursor =conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                quantity INTEGER,
                price REAL,
                low_stock_alert INTEGER DEFAULT 10
        )
    """)
    conn.commit()
    conn.close()
init_db()
