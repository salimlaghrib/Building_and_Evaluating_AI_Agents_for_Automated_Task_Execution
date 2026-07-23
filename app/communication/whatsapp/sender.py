from app.communication.whatsapp.twilio_client import TwilioClient


class WhatsAppSender:
    """
    Service responsible for sending WhatsApp messages.

    This class delegates all communication
    to the TwilioClient.
    """

    def __init__(self):

        self.client = TwilioClient()

    def send_text(
        self,
        phone: str,
        message: str,
    ) -> None:
        """
        Send a text message to a WhatsApp user.

        Args:
            phone: Customer phone number.
            message: Message content.
        """

        self.client.send_message(
            to=phone,
            body=message,
        )