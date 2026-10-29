
import math


class LaundryOrder:
    PRICE_PER_KG = 150

    def __init__(self, weight, order_id=None):
        if not isinstance(weight, (int, float)) or isinstance(weight, bool):
            raise ValueError("Weight must be a number.")

        if not math.isfinite(weight):
            raise ValueError("Weight must be a finite number.")

        if weight <= 0:
            raise ValueError("Weight must be greater than zero.")

        self.weight = weight
        self.order_id = order_id

    def calculate_price(self):
        return self.weight * self.PRICE_PER_KG

