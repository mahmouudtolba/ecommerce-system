import logging
from ecommerce.interfaces.notification import NotificationSender


logger = logging.getLogger(__name__)

class SMSNotificationSender(NotificationSender):
    """SMS notification sender implementation"""

    def send_notification(self, recipient: str, message: str) -> bool:
        # Basic phone number validation
        if not recipient or len(recipient.replace("+","").replace("-" , "").replace(" " , "")) < 10 :
            logger.error("Invalid phone number: %s", recipient)
            return False

        logger.info("Sending SMS to %s: %s", recipient, message)
        # Here you would integrate with SMS service
        return True
