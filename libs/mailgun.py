import os
from typing import List
from requests import Response, post


class MailgunException(Exception):
    def __init__(self, message: str):
        self.message = message


class Mailgun:

    FROM_TITLE = 'Pricing Service'
    FROM_EMAIL = 'do-not-reply@sandbox425d5eccfea04ef09a8db98d62adee67.mailgun.org'

    @classmethod
    def send_mail(cls, email: List[str], subject: str, text: str, html: str) -> Response:
        spi_key = os.environ.get('MAILGUN_API_KEY', None)
        domain = os.environ.get('MAILGUN_DOMAIN', None)
        if spi_key is None:
            raise MailgunException('Failed to load Mailgun API key.')

        if domain is None:
            raise MailgunException('Failed to load Mailgun domain.')
        response = post(f"{domain}/messages",
                        auth=("api", spi_key),
                        data={
                            "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                            "to": email,
                            "subject": subject,
                            "text": text,
                            "html": html})
        if response.status_code != 200:
            print(response.status_code)
            raise MailgunException('An error occurred while sending e-mail.')
        return response
