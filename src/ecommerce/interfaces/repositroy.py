from abc import ABC , abstractmethod
from ecommerce.domain.models import Order , OrderStatus
from typing import Optional


class OrderRepository(ABC):
    """Interface for order persistence"""

    @abstractmethod
    def save_order(self , order:Order) -> bool:
        "save order to storage"
        pass

    @abstractmethod
    def get_order(self, order_id: str) -> Optional[Order]:
        """Retrieve order by ID"""
        pass

    @abstractmethod
    def update_order_status(self, order_id: str, status: OrderStatus) -> bool:
        """Update order status"""
        pass
