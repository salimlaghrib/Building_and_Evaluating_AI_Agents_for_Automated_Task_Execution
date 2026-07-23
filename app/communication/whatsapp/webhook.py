from fastapi import APIRouter, Form
from fastapi.responses import PlainTextResponse
from app.logs.logger import logger
from app.services.communication_service import CommunicationService

router = APIRouter(
    prefix="/webhook",
    tags=["WhatsApp"],
)

communication_service = CommunicationService()

@router.post("/whatsapp")
async def receive_whatsapp_message(
    From: str = Form(...),
    ProfileName: str = Form(default=""),
    Body: str = Form(default=""),
    NumMedia: int = Form(default=0),
    MediaUrl0: str | None = Form(default=None),
    MediaContentType0: str | None = Form(default=None),
):
    """
    Entry point for incoming WhatsApp messages.
    """
    # 1. Vérifier la présence d'un média
    if NumMedia == 0 or not MediaUrl0:
        return PlainTextResponse("No media received.", status_code=400)

    # 2. Nettoyer le numéro
    phone = From.replace("whatsapp:", "")

    # 3. Exécuter le service avec un logger complet
    try:
        communication_service.receive_whatsapp(
            phone=phone,
            sender_name=ProfileName,
            message_text=Body,
            media_url=MediaUrl0,
            media_content_type=MediaContentType0 or "image/jpeg",
        )
        return PlainTextResponse("OK", status_code=200)

    except Exception as e:
        # Affiche la StackTrace complète dans les logs du serveur
        logger.exception("Erreur lors du traitement du message WhatsApp : %s", e)
        return PlainTextResponse(f"Internal Error: {str(e)}", status_code=500)