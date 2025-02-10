import requests

from .abstract import AbstractProcessor


class TelegramProcessor(AbstractProcessor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bot_token = self.config.get("bot_token")

    def send_alert(self, target: str, message):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        data = {"chat_id": target, "text": message}
        response = requests.post(url, data=data)
        return response.json()
