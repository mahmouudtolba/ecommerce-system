from dataclasses import dataclass
from typing import List
from enum import Enum
from datetime import datetime


@dataclass
class Product:
    id:str
    name:str
    price:str
    stock_quantity:int



@dataclass
class OrderItem:
    product: Product
    quantity: int
    
    @property
    def total_price(self) -> float:
        return float(self.product.price * self.quantity)
    


class OrderStatus(Enum):
    PENDING= "pending"
    CONFIRMED = "confirmed"
    SHIPPED="shipped"
    DELIVERED="delivered"
    CANCELLED = "cancelled"


@dataclass
class Order:
    id:str
    customer_email:str
    items:List[OrderItem]
    status:OrderStatus
    created_at:datetime


    @property
    def total_amount(self) -> float:
        return sum(item.total_price for item in self.items)