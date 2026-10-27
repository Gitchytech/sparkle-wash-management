
from database.db import get_connection


def add_customer(name, db_name=None):
    with get_connection(db_name) as connection:
        cursor = connection.execute(
            "INSERT INTO customers (name) VALUES (?)",
            (name.strip(),)
        )
        return cursor.lastrowid



def add_order(customer_id, weight, db_name=None):
    with get_connection(db_name) as connection:
        cursor = connection.execute(
            "INSERT INTO orders (customer_id, weight) VALUES (?, ?)",
            (customer_id, weight)
        )
        return cursor.lastrowid


def get_customers(db_name=None):
    with get_connection(db_name) as connection:
        return connection.execute(
            "SELECT id, name FROM customers ORDER BY id"
        ).fetchall()


def get_orders(db_name=None):
    with get_connection(db_name) as connection:
        return connection.execute("""
            SELECT
                orders.id,
                customers.name,
                orders.weight
            FROM orders
            JOIN customers
                ON orders.customer_id = customers.id
            ORDER BY orders.id
        """).fetchall()


def get_customer(customer_id, db_name=None):
    with get_connection(db_name) as connection:
        return connection.execute(
            "SELECT id, name FROM customers WHERE id = ?",
            (customer_id,)
        ).fetchone()

def find_customer_by_name(name, db_name=None):
    with get_connection(db_name) as connection:
        return connection.execute(
            "SELECT id, name FROM customers WHERE name = ? COLLATE NOCASE",
            (name.strip(),)
        ).fetchone()

def get_customer_orders(customer_id, db_name=None):
    with get_connection(db_name) as connection:
        return connection.execute("""
            SELECT id, weight
            FROM orders
            WHERE customer_id = ?
            ORDER BY id
        """, (customer_id,)).fetchall()
