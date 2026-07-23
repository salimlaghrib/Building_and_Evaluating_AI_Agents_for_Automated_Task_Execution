from pathlib import Path
from uuid import uuid4
import mimetypes
import httpx
from app.logs.logger import logger

from app.config import (
    UPLOAD_FOLDER,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
)


class WhatsAppDownloader:
    """
    Download media from Twilio and save it locally.
    """

    @staticmethod
    def download(
        media_url: str,
        content_type: str,
    ) -> str:

        upload_dir = Path(UPLOAD_FOLDER)
        upload_dir.mkdir(parents=True, exist_ok=True)

        extension = mimetypes.guess_extension(content_type) or ".bin"
        filename = f"{uuid4().hex}{extension}"
        destination = upload_dir / filename

        auth = (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN else None

        with httpx.Client(timeout=30.0) as client:
            # Step 1: Requête vers Twilio avec Auth (SANS suivre la redirection automatiquement)
            response = client.get(media_url, auth=auth, follow_redirects=False)

            # Step 2: Si Twilio renvoie une redirection (301, 302, 307, etc.)
            if response.is_redirect or response.status_code in (301, 302, 303, 307, 308):
                cdn_url = response.headers.get("location")
                if not cdn_url:
                    raise ValueError(f"Redirection HTTP {response.status_code} reçue sans en-tête 'Location'.")
                
                # Step 3: Téléchargement depuis l'URL CDN sans authentification
                response = client.get(cdn_url, follow_redirects=True)

            # Step 4: On vérifie le statut SEULEMENT sur le résultat final (Doit être 200 OK)
            response.raise_for_status()

        destination.write_bytes(response.content)
        return str(destination)