"""A module for sending notification using email"""
import logging
from ecommerce.interfaces.notification import NotificationSender

logger = logging.getLogger(__name__)

class EmailNotificationSender(NotificationSender):
    """Email notification sender implementation"""

    def send_notification(self, recipient: str, message: str) -> bool:
        if '@' not in recipient:
            logger.error("Invalid email address: %s", recipient)
            return False
        logger.info("Sending email to %s : %s", recipient, message)
        # Here you would integrate with actual email service like sendGrid
        return True
