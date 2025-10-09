
"""This module defines core data models for an ordering system , including:
- Product: Represents items available for purchase.
- OrderItem: Represents products within an order, with quantity and total price.
- OrderStatus: Enum for tracking the state of an order.
- Order: Represents a customer order with items, status, and creation date.
"""

from dataclasses import dataclass
from typing import List
from enum import Enum
from datetime import datetime


@dataclass
class Product: # pylint: disable=missing-class-docstring
    id:str
    name:str
    price:float
    stock_quantity:int



@dataclass
class OrderItem: # pylint: disable=missing-class-docstring
    product: Product
    quantity: int

    @property
    def total_price(self) -> float: # pylint: disable=missing-function-docstring
        return float(self.product.price * self.quantity)




class OrderStatus(Enum): # pylint: disable=missing-class-docstring
    PENDING= "pending"
    CONFIRMED = "confirmed"
    SHIPPED="shipped"
    DELIVERED="delivered"
    CANCELLED = "cancelled"


@dataclass
class Order: # pylint: disable=missing-class-docstring
    id:str
    customer_email:str
    items:List[OrderItem]
    status:OrderStatus
    created_at:datetime


    @property
    def total_amount(self) -> float: # pylint: disable=missing-function-docstring
        return sum(item.total_price for item in self.items)
