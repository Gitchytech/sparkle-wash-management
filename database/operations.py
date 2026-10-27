
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


def get_customer_billing(customer_id, db_name=None):
    with get_connection(db_name) as connection:
        return connection.execute("""
            SELECT
                COUNT(id),
                COALESCE(SUM(weight), 0)
            FROM orders
            WHERE customer_id = ?
        """, (customer_id,)).fetchone()


def record_payment(customer_id, amount, db_name=None):
    if amount <= 0:
        raise ValueError("Payment amount must be greater than zero.")

    with get_connection(db_name) as connection:
        cursor = connection.execute(
            """
            INSERT INTO payments (customer_id, amount)
            VALUES (?, ?)
            """,
            (customer_id, amount),
        )
        return cursor.lastrowid

def get_customer_payment_summary(customer_id, db_name=None):
    with get_connection(db_name) as connection:
        return connection.execute("""
            SELECT
                COALESCE(SUM(amount), 0)
            FROM payments
            WHERE customer_id = ?
        """, (customer_id,)).fetchone()[0]


def get_customer_balance(customer_id, db_name=None):
    order_count, total_weight = get_customer_billing(
        customer_id, db_name
    )
    total_billed = total_weight * 150

    total_paid = get_customer_payment_summary(
        customer_id, db_name
    )

    return {
        "order_count": order_count,
        "total_weight": total_weight,
        "total_billed": total_billed,
        "total_paid": total_paid,
        "balance": total_billed - total_paid,
    }
