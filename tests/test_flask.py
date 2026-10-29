import tempfile
import unittest
from pathlib import Path

from app import create_app
from database.db import create_tables
from database.operations import add_customer, add_order, record_payment


class TestFlaskDashboard(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_name = str(Path(self.temp_dir.name) / "test.db")

        create_tables(self.db_name)

        customer_id = add_customer("Dashboard Test", self.db_name)
        add_order(customer_id, 2, self.db_name)
        add_order(customer_id, 3, self.db_name)
        record_payment(customer_id, 100, self.db_name)

        app = create_app({
            "TESTING": True,
            "DATABASE": self.db_name,
        })
        self.client = app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_homepage_status(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_dashboard_displays_summary(self):
        response = self.client.get("/")
        html = response.get_data(as_text=True)

        self.assertIn("Total Customers", html)
        self.assertIn("Total Orders", html)
        self.assertIn("<h3>Total Customers</h3>", html)
        self.assertIn("<h3>Total Orders</h3>", html)
        self.assertIn("<h3>Total Customers</h3>\n                    <p>1</p>", html)
        self.assertIn("<h3>Total Orders</h3>\n                    <p>2</p>", html)
        self.assertIn("5.00 kg", html)
        self.assertIn("KSh 100.00", html)

    def test_stylesheet_is_served(self):
        response = self.client.get("/static/style.css")

        try:
            self.assertEqual(response.status_code, 200)
            self.assertIn(
                ".dashboard-grid",
                response.get_data(as_text=True),
            )
        finally:
            response.close()

if __name__ == "__main__":
    unittest.main()
