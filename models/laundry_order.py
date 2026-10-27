
class LaundryOrder:
    PRICE_PER_KG = 150

    def __init__(self, weight):
    
        """ 
        PRICE_PER_KG is a class attribute, so the rate is defined in one place.
        The constructor rejects non-numeric values, booleans, zero, and negative weights.
        """

        if not isinstance(weight, (int, float)) or isinstance(weight, bool):
            raise ValueError("Weight must be a number.")

        if weight <= 0:
            raise ValueError("Weight must be greater than zero.")

        self.weight = weight

    def calculate_price(self):
        return self.weight * self.PRICE_PER_KG
