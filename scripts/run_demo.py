import sys
import os
from datetime import datetime
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


from ecommerce.domain.models import Product , Order , OrderItem , OrderStatus
from ecommerce.services.factories import OrderServicesFactory



def demo_basic_order():
    """Demo basic order processing"""
    print("== Basic Order Processing Demo ==\n")
    order_service = OrderServicesFactory.create_order_service()

    # Create products
    laptop = Product("P100" , "Gaming laptop" ,999.99 ,  10)
    mouse = Product("P200" , "Wireless mouse" , 29.99 , 50)

    # Add to inventory
    order_service._inventory_manager.add_product(laptop)
    order_service._inventory_manager.add_product(mouse)



def main():
    """Run all demos"""
    demo_basic_order()


if __name__ == "__main__":
    main()