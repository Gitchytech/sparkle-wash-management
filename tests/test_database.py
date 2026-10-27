import sqlite3
import tempfile
import unittest
from pathlib import Path

from database.db import create_tables, get_connection
from database.operations import (
    add_customer,
    add_order,
    find_customer_by_name,
    get_customer,
    get_customer_orders,
    get_customer_billing
)


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_name = str(Path(self.temp_dir.name) / "test.db")
        create_tables(self.db_name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_customer_and_order(self):
        customer_id = add_customer("Test Customer", self.db_name)
        order_id = add_order(customer_id, 4, self.db_name)

        orders = get_customer_orders(customer_id, self.db_name)

        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0], (order_id, 4.0))

    def test_get_customer(self):
        customer_id = add_customer("Jane", self.db_name)

       
        customer = get_customer(customer_id, self.db_name)

        self.assertEqual(customer, (customer_id, "Jane"))

    def test_find_customer_case_insensitive(self):
        add_customer("Test Customer", self.db_name)

       
        customer = find_customer_by_name("test customer", self.db_name)

        self.assertIsNotNone(customer)
        self.assertEqual(customer[1], "Test Customer")

    def test_multiple_orders(self):
        customer_id = add_customer("John", self.db_name)
        add_order(customer_id, 2, self.db_name)
        add_order(customer_id, 3, self.db_name)

        orders = get_customer_orders(customer_id, self.db_name)

        self.assertEqual(len(orders), 2)
        self.assertEqual([order[1] for order in orders], [2.0, 3.0])

    def test_order_requires_existing_customer(self):
        with self.assertRaises(sqlite3.IntegrityError):
            add_order(99999, 2, self.db_name)

    def test_order_rejects_nonpositive_weight(self):
        customer_id = add_customer("Constraint Test", self.db_name)

        for weight in (0, -2):
            with self.subTest(weight=weight):
                with self.assertRaises(sqlite3.IntegrityError):
                    add_order(customer_id, weight, self.db_name)

    def test_customer_billing(self):
        customer_id = add_customer("Billing Test", self.db_name)
        add_order(customer_id, 2, self.db_name)
        add_order(customer_id, 3, self.db_name)

        billing = get_customer_billing(customer_id, self.db_name)

        self.assertEqual(billing, (2, 5.0))


if __name__ == "__main__":
    unittest.main()
