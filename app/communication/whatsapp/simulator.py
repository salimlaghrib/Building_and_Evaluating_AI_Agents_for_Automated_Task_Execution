from datetime import datetime

from app.models.order_message import OrderMessage


class WhatsAppSimulator:
    def simulate(self)->OrderMessage:
        return OrderMessage(
            source="whatsapp",
            phone="+212600000000",
            sender_name="Salim laghrib",
            message_text="""
            Bonjour,
            Je souhaite fabriquer ce matelas.
            """,
            image_path="matelas_01.jpg",
            timestamp=datetime.now()
        )