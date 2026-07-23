from app.communication.whatsapp.downloader import WhatsAppDownloader
from app.communication.whatsapp.parser import WhatsAppParser

from app.graph.state import AgentState
from app.graph.workflow import graph
from app.graph.workflowStatus import WorkflowStatus
from app.logs.logger import logger
from app.communication.whatsapp.sender import WhatsAppSender
from app.logs.logger import logger

class CommunicationService:
    """
    Orchestrates the communication layer.

    Responsibilities:
        - Download media
        - Convert Twilio payload into OrderMessage
        - Start LangGraph workflow
    """

    @staticmethod
    def receive_whatsapp(
        *,
        phone: str,
        sender_name: str,
        message_text: str,
        media_url: str,
        media_content_type: str,
    ):

        # ------------------------------------
        # Download image
        # ------------------------------------

        image_path = WhatsAppDownloader.download(
            media_url=media_url,
            content_type=media_content_type,
        )

        # ------------------------------------
        # Build OrderMessage
        # ------------------------------------

        order_message = WhatsAppParser.parse(
            phone=phone,
            sender_name=sender_name,
            message_text=message_text,
            image_path=image_path,
        )

        # ------------------------------------
        # Initial workflow state
        # ------------------------------------

        state: AgentState = {
            "order_message": order_message,
            "status": WorkflowStatus.RECEIVED,
            "validation_required": False,
            "errors": [],
        }

        # ------------------------------------
        # Launch LangGraph
        # ------------------------------------

        # Launch LangGraph and wait for completion
        result = graph.invoke(state)

        # Send confirmation message regardless of the workflow's internal
        # status. If the remote call fails we log the error but the main
        # flow continues.
        try:
            WhatsAppSender().send_text(
                phone=phone,
                message="✅ Votre commande a été traitée avec succès.",
            )
        except Exception as e:
            logger.error("Failed to send confirmation: %s", str(e))

        return result