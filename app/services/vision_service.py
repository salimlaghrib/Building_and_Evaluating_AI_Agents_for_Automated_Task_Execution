import json
import mimetypes
from pathlib import Path

from app.models.extracted_order import ExtractedOrder
from google import genai
from google.genai import types
from app.config import GEMINI_API_KEY

class VisionService:

    def __init__(self):
        # Chemin relatif au fichier actuel pour éviter les erreurs d'exécution
        self.app_dir = Path(__file__).resolve().parent.parent
        self.project_root = self.app_dir.parent
        self.uploads_dir = self.project_root / "uploads" / "raw"
        self.prompt_path = self.app_dir / "prompts" / "vision_prompt.txt"
        self.client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

    def _load_prompt(self) -> str:
        """Charge le prompt Vision depuis le fichier texte."""
        return self.prompt_path.read_text(encoding="utf-8")

    def analyze(self, image_name: str) -> ExtractedOrder:
        """
        Analyse une image de matelas située dans uploads/raw/ et retourne un ExtractedOrder.
        """
        # 1. Construire et vérifier le chemin vers l'image
        image_file = self._resolve_image_path(image_name)
        if image_file is None:
            raise FileNotFoundError(
                f"Image introuvable dans le dossier spécifié : {image_name}"
            )
        
        # 2. Bloquer l'extraction si Gemini n'est pas configuré
        if self.client is None:
            raise RuntimeError("GEMINI_API_KEY non configurée.")

        # 3. Charger le prompt et l'image (bytes)
        prompt = self._load_prompt()
        image_bytes = image_file.read_bytes()

        # 4. Deviner le type MIME
        mime_type, _ = mimetypes.guess_type(image_file)
        if not mime_type:
            mime_type = "image/jpeg"

        contents = [
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type,
            ),
            prompt
        ]

        # 5. Appeler le modèle Gemini
        try:
            response = self.client.models.generate_content(
                model="gemini-3.5-flash",
                contents=contents,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                ),
            )
        except Exception as exc:
            raise RuntimeError(f"Gemini indisponible: {exc}") from exc

        # 6. Parser et valider le JSON
        json_response = self._parse_json_response(response.text)
        return ExtractedOrder.model_validate(json_response)

    def _parse_json_response(self, text: str) -> dict:
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.removeprefix("```json").removeprefix("```").strip()
            cleaned = cleaned.removesuffix("```").strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            start = cleaned.find("{")
            end = cleaned.rfind("}")
            if start != -1 and end != -1 and end > start:
                return json.loads(cleaned[start : end + 1])
            raise

    def _resolve_image_path(self, image_name: str) -> Path | None:
        image_path = Path(image_name)

        candidates = []
        if image_path.is_absolute():
            candidates.append(image_path)
        else:
            candidates.extend([
                self.project_root / image_path,
                self.uploads_dir / image_path.name,
                image_path,
            ])

        for candidate in candidates:
            if candidate.exists():
                return candidate.resolve()

        if image_path.suffix.lower() in {".jpg", ".jpeg"}:
            alternate_suffix = ".jpeg" if image_path.suffix.lower() == ".jpg" else ".jpg"
            alternate_name = image_path.with_suffix(alternate_suffix)
            alternate_candidates = []
            if alternate_name.is_absolute():
                alternate_candidates.append(alternate_name)
            else:
                alternate_candidates.extend([
                    self.project_root / alternate_name,
                    self.uploads_dir / alternate_name.name,
                    alternate_name,
                ])

            for candidate in alternate_candidates:
                if candidate.exists():
                    return candidate.resolve()

        return None
