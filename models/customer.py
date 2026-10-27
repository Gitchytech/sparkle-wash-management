
from .laundry_order import LaundryOrder


class Customer:
    def __init__(self, name):

        """
            Here, Customer imports LaundryOrder using a relative import. 
            The orders list stores order objects, and total_bill() adds up their prices.
        """
        if not name.strip():
            raise ValueError("Customer name cannot be empty.")

        self.name = name.strip()
        self.orders = []

    def add_order(self, order: LaundryOrder):
        self.orders.append(order)

    def total_bill(self):
        return sum(order.calculate_price() for order in self.orders)
