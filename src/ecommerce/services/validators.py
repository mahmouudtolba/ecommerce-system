import logging
from ecommerce.domain.models import Order



logger = logging.getLogger(__name__)

class OrderValidator:
    """Responsible only for validating orders"""

    def validate_order(self , order : Order) -> bool:
        """Validate order data"""

        if not order.customer_email or "@" not in order.customer_email:
            logger.error("Invalid customer email")
            return False


        if not order.items:
            logger.error("Order has no items")
            return False

        if order.total_amount <= 0 :
            logger.error("Invalid order total")
            return False

        return True
