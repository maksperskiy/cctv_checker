import requests

from .abstract import AbstractProcessor


class SlackProcessor(AbstractProcessor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.webhook_url = self.config.get("webhook_url")

    def send_alert(self, target: str, message: str):
        data = {"channel": target, "text": message}
        response = requests.post(self.webhook_url, json=data)
        return response.json()
