from twilio.rest import Client

from app.config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_WHATSAPP_NUMBER,
)


class TwilioClient:
    """
    Wrapper around the Twilio SDK.

    This class centralizes every interaction
    with the Twilio API.
    """

    def __init__(self):

        # Normalise the WhatsApp sending number to include the required
        # ``whatsapp:`` prefix.  The .env file may store the number
        # with or without the prefix.
        global TWILIO_WHATSAPP_NUMBER
        if not TWILIO_WHATSAPP_NUMBER.startswith("whatsapp:"):
            TWILIO_WHATSAPP_NUMBER = f"whatsapp:{TWILIO_WHATSAPP_NUMBER}"
        self.client = Client(
            TWILIO_ACCOUNT_SID,
            TWILIO_AUTH_TOKEN,
        )

    # -------------------------------------------------
    # Send WhatsApp message
    # -------------------------------------------------

    def send_message(
        self,
        to: str,
        body: str,
    ):

        return self.client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            to=f"whatsapp:{to}",
            body=body,
        )

    # -------------------------------------------------
    # Get media information
    # -------------------------------------------------

    def get_media(self, media_sid: str):

        return self.client.messages.media(media_sid).fetch()