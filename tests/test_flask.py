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
            "WTF_CSRF_ENABLED": False,
            "DATABASE": self.db_name,
        })
        self.client = app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_homepage_status(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_customers_page_status(self):
        response = self.client.get("/customers")
        self.assertEqual(response.status_code, 200)

    def test_customers_page_displays_customer(self):
        response = self.client.get("/customers")
        html = response.get_data(as_text=True)

        self.assertIn("Dashboard Test", html)
        self.assertIn("Customer Management", html)

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

    def test_register_customer(self):
        response = self.client.post(
            "/customers",
            data={"name": "New Test Customer"},
        )

        self.assertEqual(response.status_code, 302)

        response = self.client.get("/customers")
        self.assertIn(
            "New Test Customer",
            response.get_data(as_text=True),
        )

    def test_register_customer_with_blank_name(self):
        response = self.client.post(
            "/customers",
            data={"name": "   "},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Customer name cannot be empty.",
            response.get_data(as_text=True),
        )

    def test_register_customer_with_too_short_name(self):
        response = self.client.post(
            "/customers",
            data={"name": "A"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Customer name must be at least 2 characters.",
            response.get_data(as_text=True),
        )

    def test_register_customer_with_too_long_name(self):
        response = self.client.post(
            "/customers",
            data={"name": "A" * 51},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Customer name cannot exceed 50 characters.",
            response.get_data(as_text=True),
        )

    def test_edit_customer_page_displays_current_name(self):
        customer_id = add_customer("Edit Test Customer", self.db_name)

        response = self.client.get(
            f"/customers/{customer_id}/edit"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'value="Edit Test Customer"',
            response.get_data(as_text=True),
        )

    def test_edit_customer_updates_name(self):
        customer_id = add_customer("Original Name", self.db_name)

        response = self.client.post(
            f"/customers/{customer_id}/edit",
            data={"name": "Updated Name"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/customers")

        response = self.client.get("/customers")
        self.assertIn(
            "Updated Name",
            response.get_data(as_text=True),
        )
        self.assertNotIn(
            "Original Name",
            response.get_data(as_text=True),
        )

    def test_edit_customer_rejects_blank_name(self):
        customer_id = add_customer("Original Name", self.db_name)

        response = self.client.post(
            f"/customers/{customer_id}/edit",
            data={"name": "   "},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Customer name cannot be empty.",
            response.get_data(as_text=True),
        )
        self.assertIn(
            'value="Original Name"',
            response.get_data(as_text=True),
        )

    def test_edit_customer_with_too_short_name(self):
        customer_id = add_customer("Original Name", self.db_name)

        response = self.client.post(
            f"/customers/{customer_id}/edit",
            data={"name": "A"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Customer name must be at least 2 characters.",
            response.get_data(as_text=True),
        )
        self.assertIn(
            'value="Original Name"',
            response.get_data(as_text=True),
        )

    def test_edit_customer_with_too_long_name(self):
        customer_id = add_customer("Original Name", self.db_name)

        response = self.client.post(
            f"/customers/{customer_id}/edit",
            data={"name": "A" * 51},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Customer name cannot exceed 50 characters.",
            response.get_data(as_text=True),
        )
        self.assertIn(
            'value="Original Name"',
            response.get_data(as_text=True),
        )

    def test_edit_nonexistent_customer_returns_404(self):
        response = self.client.get("/customers/99999/edit")

        self.assertEqual(response.status_code, 404)

class TestFlaskCSRF(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_name = str(Path(self.temp_dir.name) / "csrf_test.db")

        create_tables(self.db_name)

        self.app = create_app({
            "TESTING": True,
            "WTF_CSRF_ENABLED": True,
            "DATABASE": self.db_name,
        })

        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_post_without_csrf_token_is_rejected(self):
        response = self.client.post(
            "/customers",
            data={"name": "Unauthorized Customer"},
        )

        self.assertEqual(response.status_code, 400)

    def test_post_with_valid_csrf_token_is_accepted(self):
        response = self.client.get("/customers")
        html = response.get_data(as_text=True)

        import re
        match = re.search(
            r'name="csrf_token" value="([^"]+)"',
            html,
        )
        self.assertIsNotNone(match)

        token = match.group(1)

        response = self.client.post(
            "/customers",
            data={
                "name": "Authorized Customer",
                "csrf_token": token,
            },
        )

        self.assertEqual(response.status_code, 302)

if __name__ == "__main__":
    unittest.main()
