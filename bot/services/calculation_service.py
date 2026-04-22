class CalculationService:
    @staticmethod
    def calculate_total(amount: float, price_per_unit: float) -> float:
        """Рассчитать общую сумму"""
        return round(amount * price_per_unit, 2)
    
    @staticmethod
    def calculate_discount(price: float, discount_percent: int) -> float:
        """Рассчитать цену со скидкой"""
        if discount_percent <= 0 or discount_percent > 100:
            return price
        return round(price * (1 - discount_percent / 100), 2)