import logging
from typing import Optional
from ecommerce.interfaces.repositroy import OrderRepository
from ecommerce.domain.models import Order , OrderStatus
from ecommerce.domain.exceptions import OrderNotFoundException

logger = logging.getLogger(__name__)

class InMemoryOrderRepository(OrderRepository):
    """In-memory order repository implementation"""
    def __init__(self):
        self.orders = {}


    def save_order(self, order: Order) -> bool:
        """Save order in memory storage"""
        try:
            self.orders[order.id] = order
            logger.info("Saved order %s to in-memory storage", order.id)
            return True

        except Exception as e :
            logger.error("Failed to save order %s : %s", order.id, str(e))
            return False
        

    def get_order(self, order_id: str) -> Optional[Order]:
        """Retrieve order by ID"""
        order = self.orders.get(order_id)
        if order :
            logger.info("Retrieved order %s from in-memory storage" , order_id)
        else:
            logger.warning("Order %s not found in in-memory storage" , order_id)
            
        return order
    
    def update_order_status(self, order_id: str, status: OrderStatus) -> bool:
        """Update order status"""
        try:
            if order_id in self.orders:
                self.orders[order_id].status = status
                logger.info("Updated order %s status to %s" , order_id, status.value) 
                return True
            else:
                logger.error("Order %s not found for status update" , order_id)
                return False
        except Exception as e:
            logger.error("Failed to update order %s  status: %s " , order_id ,str(e) )
            return False

    def list_orders(self) -> list[Order]:
        """List all orders (additional utility method)"""
        return list(self.orders.values())

    def delete_order(self , order_id:str) -> bool:
        """Delete order (additional utility method)"""
        try:
            if order_id in self.orders:
                del self.orders[order_id]
                logger.info("Deleted order %s from in-memory storage" , order_id)
                return True
            else:
                logger.info("Order %s not found for deletion" , order_id)
                return False
        except Exception as e :
            logger.error("Failed to delete order %s: %s" , order_id , str(e))
            return False
