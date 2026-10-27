
from models.customer import Customer
from models.laundry_order import LaundryOrder


def main():
    customer = Customer("Gianna")
    customer.add_order(LaundryOrder(4))
    customer.add_order(LaundryOrder(2))

    print(f"Customer: {customer.name}")
    print(f"Total bill: KSh {customer.total_bill()}")


if __name__ == "__main__":
    main()
