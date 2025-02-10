import requests

from .abstract import AbstractProcessor


class WhatsAppProcessor(AbstractProcessor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_url = self.config.get("api_url")
        self.api_key = self.config.get("api_key")

    def send_alert(self, target: str, message: str):
        url = f"{self.api_url}/send"
        data = {"to": target, "message": message, "token": self.api_key}
        response = requests.post(url, json=data)
        return response.json()
