from abc import ABC, abstractmethod

class InventoryManager(ABC):
    """Interface for inventory management"""
    
    @abstractmethod
    def check_availability(self, product_id: str, quantity: int) -> bool:
        """Check if product is available in required quantity"""
        pass
    
    @abstractmethod
    def reserve_stock(self, product_id: str, quantity: int) -> bool:
        """Reserve stock for an order"""
        pass
    
    @abstractmethod
    def release_stock(self, product_id: str, quantity: int) -> bool:
        """Release previously reserved stock"""
        pass
