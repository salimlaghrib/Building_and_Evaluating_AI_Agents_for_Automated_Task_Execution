from datetime import datetime

from app.models.order_message import OrderMessage


class GmailSimulator:

    def simulate(self) -> OrderMessage:
        return OrderMessage(
            source="gmail",
            email="ahmed@example.com",
            sender_name="Ahmed",
            message_text="""
Bonjour,

Je souhaite fabriquer ce matelas.
Vous trouverez le dessin en pièce jointe.

Merci.
""",
            image_path="matelas_01.jpg",
            timestamp=datetime.now()
        )