import logging
from ecommerce.interfaces.inventory import InventoryManager
from ecommerce.domain.models import Product

logger = logging.getLogger(__name__)


class InMemoryInventoryManager(InventoryManager):
    def __init__(self):
        self.inventory = {} # product_id -> available_quantity

    def add_product(self, product : Product):
        """Add product to inventory"""
        self.inventory[product.id] = product.stock_quantity

    def check_availability(self, product_id: str, quantity: int) -> bool:
        availabe = self.inventory.get(product_id , 0)
        return availabe >= quantity
    
    def reserve_stock(self, product_id: str, quantity: int) -> bool:
        if self.check_availability(product_id , quantity):
            self.inventory[product_id] -= quantity
            logger.info(f"Reserved {quantity} units of product {product_id}")
            return True
        logger.error(f"Insufficient stock for product {product_id}")
        return False
    
    def return_stock(self, product_id: str, quantity: int) -> bool:
        self.inventory[product_id] = self.inventory.get(product_id , 0) + quantity
        logger.info(f"Returning {quantity} units of product {product_id}")
        return True