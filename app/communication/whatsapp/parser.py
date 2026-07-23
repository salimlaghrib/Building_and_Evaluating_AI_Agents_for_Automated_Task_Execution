from datetime import datetime

from app.models.order_message import OrderMessage


class WhatsAppParser:
    """
    Convert raw Twilio webhook data
    into an OrderMessage object.
    """

    @staticmethod
    def parse(
        *,
        phone: str,
        sender_name: str | None,
        message_text: str | None,
        image_path: str,
    ) -> OrderMessage:

        return OrderMessage(
            source="WhatsApp",
            phone=phone,
            sender_name=sender_name,
            message_text=message_text,
            image_path=image_path,
            timestamp=datetime.now(),
        )