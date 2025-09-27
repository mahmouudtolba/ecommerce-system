import logging
from typing import Dict , Any , List


from ecommerce.domain.models import Order , OrderItem , OrderStatus
from ecommerce.domain.exceptions import InvalidOrderException , PaymentProcessingException
from ecommerce.interfaces.payment import PaymentProcessor
from ecommerce.interfaces.notification import NotificationSender
from ecommerce.interfaces.inventory import InventoryManager
from ecommerce.interfaces.repositroy import OrderRepository
from ecommerce.services.validators import OrderValidator
from ecommerce.services.calculators import PriceCalculator

logger = logging.getLogger(__name__)

class OrderService:
    """
    High-level service that orchestrates order processing
    Depends on abstractions (interfaces) , not concrete implementations
    """

    def __init__(self , 
                payment_processor : PaymentProcessor,
                notification_sender : NotificationSender,
                inventory_manager : InventoryManager , 
                order_repository : OrderRepository,
                price_calculator:PriceCalculator,
                order_validator : OrderValidator ):
        self._payment_processor = payment_processor
        self._notification_sender = notification_sender
        self._inventory_manager = inventory_manager
        self._order_repository = order_repository
        self._price_calculator = price_calculator
        self._order_validator = order_validator


    def create_order(self , order : Order , payment_details:Dict[str , Any]) ->bool:
        """Process a complete order from validation to confirmation"""
        try:
            # 1. Validate the order
            if not self._order_validator.validate_order(order):
                raise InvalidOrderException("Order validation failed")
            # 2. Check inventory availability
            for item in order.items:
                if not self._inventory_manager.check_availability(item.product.id , item.quantity):
                    raise InvalidOrderException(f"Product {item.product.name} not available")
                
            # 3. Calculate final pricing
            pricing = self._price_calculator.calculate_final_total(order)

            # 4. Reserve Inventory
            self._reserve_inventory(order.items)


            try:
                # 5. process payment
                if not self._payment_processor.process_payment(pricing["total"] , payment_details):
                    raise PaymentProcessingException("Payment processing failed")      
                

                # 6. Save order
                order.status = OrderStatus.CONFIRMED
                self._order_repository.save_order(order)



            
        


