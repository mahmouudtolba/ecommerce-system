import logging
from typing import Dict , Any , List


from ecommerce.domain.models import Order , OrderItem , OrderStatus
from ecommerce.domain.exceptions import  (InvalidOrderException ,
           PaymentProcessingException,OrderNotFoundException )
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

                # 7. Send confirmation notification
                message = f"Order {order.id} confirmed. Total: ${pricing['total']:.2f}"
                self._notification_sender.send_notification(order.customer_email , message)

                logger.info("Order %s successfully processed!", order.id)
                return True

            except Exception as e:
                # Rollback inventory reservations on any failure after reservation
                self._release_all_reservation(order.items)
                raise e

        except Exception as e:
            logger.error("Order processing failed: %s", str(e))
            return False



    def cancel_order(self , order_id : str) -> bool:
        try:
            # 1. Check if the order saved
            order = self._order_repository.get_order(order_id)
            if not order:
                raise OrderNotFoundException(f"Order {order_id} not found to cancel")

            # 2. If shipped or delivered can not be cancelled
            if order.status in [OrderStatus.SHIPPED , OrderStatus.DELIVERED]:
                raise InvalidOrderException(
                    f"Cannot cancel order {order_id} - already {order.status.value}"
                    )

            # 3. Release inventory
            self._release_all_reservation(order.items)

            # 4. Update order status
            self._order_repository.update_order_status(order_id , OrderStatus.CANCELLED)

            # 5. Send notification
            message = f"Order {order_id} has been cancelled"
            self._notification_sender.send_notification(order.customer_email , message)

            return True

        except Exception as e:
            logger.error("Order cancellation failed :%s", str(e))
            return False


    def _release_all_reservation(self , items:List[OrderItem]):
        """Release all inventory reservations"""
        for item in items:
            self._inventory_manager.return_stock(item.product.id ,item.quantity )



    def _reserve_inventory(self , items: List[OrderItem]):
        """Reserve inventory for all items"""
        reserved_items = []
        try:
            for item in items:
                if self._inventory_manager.reserve_stock(item.product.id , item.quantity):
                    reserved_items.append(item)
                else:
                    raise InvalidOrderException(f"Could not reserve stock for {item.product.name}")

        except Exception:
            for item in reserved_items:
                self._inventory_manager.return_stock(item.product.id , item.quantity)
