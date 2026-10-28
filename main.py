
from database.db import create_tables
from models.customer import Customer
from database.operations import (
    add_customer,
    find_customer_by_name,
    get_customer_orders,
    get_customer_report,
    record_payment
)
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

    while True:
        report = get_customer_report(customer.customer_id)
        summary = report

        print("\n--- Customer Billing Summary ---")
        print(f"Customer: {customer.name}")

        print("\n--- Order Details ---")

        for order_id, weight in report["orders"]:
            price = weight * LaundryOrder.PRICE_PER_KG
            print(
                f"Order {order_id}: {weight:g} kg - "
                f"KSh {price:.2f}"
            )

        print(f"Total orders: {summary['order_count']}")
        print(f"Total laundry: {summary['total_weight']:g} kg")
        print(f"Total billed: KSh {summary['total_billed']:.2f}")
        print(f"Total paid: KSh {summary['total_paid']:.2f}")
        print(f"Outstanding balance: KSh {summary['balance']:.2f}")

        if summary["balance"] <= 0:
            break

        choice = input("Record a payment? (y/n): ").strip().lower()

        if choice != "y":
            break

        try:
            amount = float(input("Enter payment amount (KSh): "))

            if amount <= 0:
                print("Payment must be greater than zero.")
                continue

            if amount > summary["balance"]:
                print("Payment cannot exceed the outstanding balance.")
                continue

            record_payment(customer.customer_id, amount)
            print("Payment recorded successfully.")

        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    main()
            
