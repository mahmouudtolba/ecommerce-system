import logging
from typing import Dict , Any
from ecommerce.interfaces.payment import PaymentProcessor


logger = logging.getLogger(__name__)

class CreditCardProcessor(PaymentProcessor):
    """Credit card payment processor implementations"""
    def process_payment(self, amount: float, payment_details: Dict[str, Any]) -> bool:
        card_number = payment_details.get("card_number" , "")
        if len(card_number) <4:
            logger.error("Invalid card number")
            return False

        logger.info("Processing credit card payment: $%s with card ending in %s", amount, card_number[-4:])
        # Simulate payment processing
        return True
