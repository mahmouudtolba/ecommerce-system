"""Module defining the NotificationSender interface for sending notifications."""

from abc import ABC , abstractmethod

class NotificationSender(ABC):
    """Interface for sending notifications"""

    @abstractmethod
    def send_notification(self , recipient:str , message:str) -> bool:
        """Send notification and return success status"""
        pass