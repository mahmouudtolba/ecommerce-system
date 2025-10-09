from ecommerce.services.order_service import OrderService
from ecommerce.services.validators import OrderValidator
from ecommerce.services.calculators import PriceCalculator

# Payment processors
from ecommerce.implementations.payment.credit_card import CreditCardProcessor
from ecommerce.implementations.payment.crypto import CryptoProcessor

# Notification senders
from ecommerce.implementations.natifications.email_sender import EmailNotificationSender
from ecommerce.implementations.natifications.sms_sender import SMSNotificationSender

# Inventory managers
from ecommerce.implementations.inventory.in_memory import InMemoryInventoryManager

# Repositories
from ecommerce.implementations.repositories.in_memory import InMemoryOrderRepository

class OrderServicesFactory:
    """Factory to create OrderService with appropriate dependencies"""
    @staticmethod
    def create_order_service(
        payment_type:str="credit_card",
        notification_type:str = "email",
        storage_type:str = "in_memory"
    ) -> OrderService:

        # Choose payment processor
        payment_processors = {
            "credit_card": CreditCardProcessor(),
            "crypto":CryptoProcessor()
        }

        # Choose notification sender
        notification_senders = {
            "email": EmailNotificationSender(),
            "sms" : SMSNotificationSender()
        }

        # Choose inventory manager
        inventory_managers = {
            "in_memory":InMemoryInventoryManager()
        }

        # Choose repository
        repositories = {
            "in_memory": InMemoryOrderRepository()
        }

        return OrderService(
            payment_processor = payment_processors.get(payment_type , CreditCardProcessor()),
            notification_sender = notification_senders.get(notification_type ,
                                    EmailNotificationSender()),
            inventory_manager=inventory_managers.get(storage_type , InMemoryInventoryManager()),
            order_repository=repositories.get(storage_type , InMemoryOrderRepository()),
            price_calculator=PriceCalculator(),
            order_validator=OrderValidator()
        )
    
    @staticmethod
    def create_custom_service(
        payment_processor ,
        notification_sender,
        inventory_manager , 
        order_repositroy
    ) -> OrderService:
        """Create OrderService with custom implementations"""
        return OrderService(
            payment_processor=payment_processor,
            notification_sender=notification_sender , 
            inventory_manager=inventory_manager,
            order_repository=order_repositroy , 
            price_calculator=PriceCalculator(),
            order_validator=OrderValidator()

        )