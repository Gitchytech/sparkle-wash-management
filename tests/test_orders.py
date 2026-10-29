
import unittest

from models.customer import Customer
from models.laundry_order import LaundryOrder


class TestLaundryOrder(unittest.TestCase):
    def test_calculate_price(self):
        order = LaundryOrder(4)
        self.assertEqual(order.calculate_price(), 600)

    def test_invalid_weight(self):
        with self.assertRaises(ValueError):
            LaundryOrder(-2)

    def test_nan_weight(self):
        with self.assertRaises(ValueError):
            LaundryOrder(float("nan"))

    def test_positive_infinity_weight(self):
        with self.assertRaises(ValueError):
            LaundryOrder(float("inf"))

    def test_negative_infinity_weight(self):
        with self.assertRaises(ValueError):
            LaundryOrder(float("-inf"))

    def test_empty_customer_name(self):
        with self.assertRaises(ValueError):
            Customer("   ")

    def test_customer_total_bill(self):
        customer = Customer("Gianna")
        customer.add_order(LaundryOrder(4))
        customer.add_order(LaundryOrder(2))

        self.assertEqual(customer.total_bill(), 900)


if __name__ == "__main__":
    unittest.main()
