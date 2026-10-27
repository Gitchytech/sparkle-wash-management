
from database.db import create_tables
from database.operations import (
    add_customer,
    find_customer_by_name,
    get_customer_orders,
)
from models.customer import Customer
from models.laundry_order import LaundryOrder


def main():
    create_tables()

    name = input("Enter customer name: ").strip()
    if not name:
        print("Customer name cannot be empty.")
        return

    existing = find_customer_by_name(name)

    if existing:
        customer_id, saved_name = existing
        customer = Customer(saved_name, customer_id)
        print(f"Welcome back, {customer.name}!")
        print("Previous orders:")

        for order_id, weight in get_customer_orders(customer_id):
            price = weight * LaundryOrder.PRICE_PER_KG
            print(
                f"Order {order_id}: {weight:g} kg - "
                f"KSh {price:.2f}"
            )
    else:
        customer_id = add_customer(name)
        customer = Customer(name, customer_id)
        print(f"New customer registered: {customer.name}")

    while True:
        try:
            weight = float(input("Enter laundry weight in kg (0 to finish): "))

            if weight == 0:
                break

            order = LaundryOrder(weight)
            customer.save_order(order)
            print(f"Order saved. Price: KSh {order.calculate_price():.2f}")

        except ValueError as error:
            print(f"Invalid input: {error}")

    print(f"\nCustomer: {customer.name}")
    print(f"Total bill for new orders: KSh {customer.total_bill():.2f}")


if __name__ == "__main__":
    main()
            
