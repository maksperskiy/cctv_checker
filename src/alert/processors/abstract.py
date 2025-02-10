from abc import ABC, abstractmethod


# Abstract base class for the Alert system
class AbstractProcessor(ABC):
    def __init__(self, **kwargs):
        """
        Initialize the alert system with system-specific configurations using kwargs.
        """
        self.config = kwargs

    @abstractmethod
    def send_alert(self, target: str, message: str):
        """
        Send an alert to a specific target based on the check object.
        The 'check' object should contain:
        - status: str
        - created_at: datetime
        - camera: dict (which can include camera-specific information like ID, location, etc.)

        :param target: The target user/channel/etc. to send the alert to
        :param check: A dictionary containing alert-related data (status, created_at, camera object)
        """
        pass
