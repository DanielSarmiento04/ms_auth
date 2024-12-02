import os
import resend
from ..constants import (
    RESEND_API_KEY
)

resend.api_key = RESEND_API_KEY

class Emails:

    @staticmethod
    def send(
        to:str,
    ):
        params: resend.Emails.SendParams = {
            "from": "Acme <onboarding@resend.dev>",
            "to": [to],
            "subject": "hello world",
            "html": "<strong>it works!</strong>",
        }

        email = resend.Emails.send(params)
        
        return email
