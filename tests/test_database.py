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
    get_customer_billing,
    record_payment,
    get_customer_payment_summary,
    get_customer_balance
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

    def test_record_payment(self):
        customer_id = add_customer("Payment Test", self.db_name)
        add_order(customer_id, 5, self.db_name)

        payment_id = record_payment(customer_id, 500, self.db_name)

        self.assertIsInstance(payment_id, int)

        with get_connection(self.db_name) as connection:
            payment = connection.execute(
                "SELECT customer_id, amount FROM payments WHERE id = ?",
                (payment_id,),
            ).fetchone()

        self.assertEqual(payment, (customer_id, 500.0))

    def test_reject_nonpositive_payment(self):
        customer_id = add_customer("Invalid Payment", self.db_name)

        for amount in (0, -100):
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    record_payment(customer_id, amount, self.db_name)

    def test_customer_payment_summary(self):
        customer_id = add_customer("Payment Summary Test", self.db_name)
        add_order(customer_id, 6, self.db_name)

        record_payment(customer_id, 500, self.db_name)
        record_payment(customer_id, 300, self.db_name)

        total_paid = get_customer_payment_summary(
            customer_id, self.db_name
        )

        self.assertEqual(total_paid, 800.0)

    def test_customer_with_no_payments(self):
        customer_id = add_customer("Unpaid Customer", self.db_name)

        total_paid = get_customer_payment_summary(
            customer_id, self.db_name
        )

        self.assertEqual(total_paid, 0)

    def test_unpaid_customer_balance(self):
        customer_id = add_customer("Unpaid Test", self.db_name)
        add_order(customer_id, 2, self.db_name)

        summary = get_customer_balance(customer_id, self.db_name)

        self.assertEqual(summary["total_billed"], 300)
        self.assertEqual(summary["total_paid"], 0)
        self.assertEqual(summary["balance"], 300)

    def test_partially_paid_customer_balance(self):
        customer_id = add_customer("Partial Test", self.db_name)
        add_order(customer_id, 2, self.db_name)
        record_payment(customer_id, 100, self.db_name)

        summary = get_customer_balance(customer_id, self.db_name)

        self.assertEqual(summary["total_billed"], 300)
        self.assertEqual(summary["total_paid"], 100)
        self.assertEqual(summary["balance"], 200)

    def test_fully_paid_customer_balance(self):
        customer_id = add_customer("Paid Test", self.db_name)
        add_order(customer_id, 2, self.db_name)
        record_payment(customer_id, 300, self.db_name)

        summary = get_customer_balance(customer_id, self.db_name)

        self.assertEqual(summary["total_billed"], 300)
        self.assertEqual(summary["total_paid"], 300)
        self.assertEqual(summary["balance"], 0)

    def test_reject_overpayment(self):
        customer_id = add_customer("Overpayment Test", self.db_name)
        add_order(customer_id, 2, self.db_name)  # KSh 300 bill

        with self.assertRaises(ValueError):
            record_payment(customer_id, 301, self.db_name)

    def test_reject_payment_for_nonexistent_customer(self):
        with self.assertRaises(ValueError):
            record_payment(999999, 100, self.db_name)

if __name__ == "__main__":
    unittest.main()
