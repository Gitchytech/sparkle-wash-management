
from .laundry_order import LaundryOrder
from database.operations import add_order as save_order_to_db

class Customer:
    def __init__(self, name, customer_id=None):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Customer name cannot be empty.")

        self.name = name.strip()
        self.customer_id = customer_id
        self.orders = []

    def add_order(self, order: LaundryOrder):
        self.orders.append(order)

    def total_bill(self):
        return sum(order.calculate_price() for order in self.orders)


    def save_order(self, order: LaundryOrder):
        if self.customer_id is None:
            raise ValueError("Customer must be saved to the database first.")

        order_id = save_order_to_db(self.customer_id, order.weight)
        order.order_id = order_id
        self.add_order(order)
        return order_id

