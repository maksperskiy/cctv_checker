import smtplib
from email.mime.text import MIMEText

from .abstract import AbstractProcessor


class EmailProcessor(AbstractProcessor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.smtp_server = self.config.get("smtp_server")
        self.smtp_port = self.config.get("smtp_port")
        self.smtp_username = self.config.get("smtp_username")
        self.smtp_password = self.config.get("smtp_password")
        self.sender_email = self.config.get("sender_email")

    def send_alert(self, target: str, message_content: str):
        msg = MIMEText(message_content)
        msg["Subject"] = "Security Alert"
        msg["From"] = self.sender_email
        msg["To"] = target

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            server.sendmail(self.sender_email, target, msg.as_string())
