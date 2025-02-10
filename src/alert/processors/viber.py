import requests

from .abstract import AbstractProcessor


class ViberProcessor(AbstractProcessor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = self.config.get("api_key")

    def send_alert(self, target: str, message: str):
        url = f"https://chatapi.viber.com/pa/send_message"
        data = {
            "receiver": target,
            "min_api_version": 1,
            "sender": {"name": "SecurityBot"},
            "tracking_data": "tracking data",
            "type": "text",
            "text": message,
        }
        headers = {"X-Viber-Auth-Token": self.api_key}
        response = requests.post(url, json=data, headers=headers)
        return response.json()
