from typing import Dict
from ecommerce.domain.models import Order

class PriceCalculator:
    """Responsible only for calculating prices"""
    
    def calculate_tax(self, amount:float , tax_rate:float = 0.10) ->float:
        """Calculate tax amount"""

        return amount * tax_rate
    
    def calculate_shipping(self , total_amount:float) -> float:
        """Calculating shipping cost"""
        if total_amount > 100:
            return 0
        return 100
    
    def calculate_final_total(self , order:Order) -> Dict[str , float]:
        """Calculate final order totals"""

        subtotal = order.total_amount
        tax = self.calculate_tax(subtotal)
        shipping = self.calculate_shipping(subtotal)
        total = subtotal + tax + shipping

        return {
            "subtotal":subtotal ,
            "tax" : tax ,
            "shipping" : shipping ,
            "total":total
        }