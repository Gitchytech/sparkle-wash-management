import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_NAME = Path(__file__).resolve().parent.parent / "sparkle_wash.db"


@contextmanager
def get_connection(db_name=None):
    connection = sqlite3.connect(db_name or DB_NAME)
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        with connection:
            yield connection
    finally:
        connection.close()


def create_tables(db_name=None):
    with get_connection(db_name) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                weight REAL NOT NULL CHECK (weight > 0),
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                amount REAL NOT NULL CHECK (amount > 0),
                payment_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """)
