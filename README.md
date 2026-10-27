# Sparkle Wash Management System

A Python-based laundry management application built to practise object-oriented programming (OOP), input validation, automated testing, and software version control.

## Features

- Customer management using Python classes
- Laundry order creation and pricing
- Configurable price per kilogram
- Input validation and error handling
- Customer order collections and total bill calculation
- Automated unit tests using `unittest`

## Technology Stack

- Python
- Object-oriented programming
- Git and GitHub
- Python `unittest`

## Project Structure

```text
sparkle-wash-management/
├── main.py
├── models/
│   ├── __init__.py
│   ├── customer.py
│   └── laundry_order.py
├── tests/
│   └── test_orders.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### Requirements

Python 3.10 or later is recommended.

### Run the application

Clone the repository:

```bash
git clone https://github.com/Gitchytech/sparkle-wash-management.git
cd sparkle-wash-management
```

Run the application:

```bash
python main.py
```

### Run the tests

```bash
python -m unittest discover -s tests -v
```

The current test suite checks price calculation, customer totals, empty customer names, and invalid order weights.

## Example Output

```text
Customer: Gianna
Total bill: KSh 900
```

## Planned Improvements

- SQLite database storage
- Persistent customer and order records
- Order history and reporting
- Improved command-line interaction
- Additional automated tests

## Author

GitHub: [Gitchytech](https://github.com/Gitchytech)

