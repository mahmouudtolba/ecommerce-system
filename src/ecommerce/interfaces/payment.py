from abc import ABC , abstractmethod
from typing import Dict , Any

class PaymentProcessor(ABC):
    """Interface for payment processing"""

    @abstractmethod
    def process_payment(self , amount:float , payment_details:Dict[str , Any]) -> bool:
        """Process payment and return success status"""
        pass
