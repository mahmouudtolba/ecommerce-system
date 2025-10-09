"""Module defining the InventoryManager interface for controlling orders."""
from abc import ABC, abstractmethod
from ecommerce.domain.models import Product


class InventoryManager(ABC):
    """Interface for inventory management"""

    @abstractmethod
    def add_product(self, product: Product) -> None:
        """Add product to inventory"""
        pass

    @abstractmethod
    def check_availability(self, product_id: str, quantity: int) -> bool:
        """Check if product is available in required quantity"""
        pass

    @abstractmethod
    def reserve_stock(self, product_id: str, quantity: int) -> bool:
        """Reserve stock for an order"""
        pass

    @abstractmethod
    def return_stock(self, product_id: str, quantity: int) -> bool:
        """Release previously reserved stock"""
        pass
