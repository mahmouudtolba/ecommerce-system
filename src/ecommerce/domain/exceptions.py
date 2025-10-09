

class EcommerceException(Exception):
    """Base exception for ecommerce system"""
    pass

class InvalidOrderException(EcommerceException):
    """Raised when order validation fails"""
    pass

class InsufficientStockException(EcommerceException):
    """Raised when not enough stock is available"""
    pass

class PaymentProcessingException(EcommerceException):
    """Raised when payment processing fails"""
    pass

class OrderNotFoundException(EcommerceException):
    """Raised when order is not found"""
    pass
