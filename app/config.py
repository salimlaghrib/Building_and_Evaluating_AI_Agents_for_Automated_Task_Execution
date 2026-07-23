import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV", "development")

MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")




def _normalize_ollama_base_url(base_url: str) -> str:
    base_url = base_url.rstrip("/")
    if base_url.endswith("/api"):
        return base_url[: -len("/api")]
    return base_url


_default_ollama_base_url = "https://ollama.com" if OLLAMA_API_KEY else "http://localhost:11434"
OLLAMA_BASE_URL = _normalize_ollama_base_url(
    os.getenv("OLLAMA_BASE_URL", _default_ollama_base_url)
)
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.1")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

OPENCLAW_GATEWAY_URL = os.getenv("OPENCLAW_GATEWAY_URL")
OPENCLAW_GATEWAY_TOKEN = os.getenv("OPENCLAW_GATEWAY_TOKEN")


WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")
BASE_URL=os.getenv("BASE_URL", "http://127.0.0.1:8000/api")
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

UPLOAD_FOLDER="uploads/raw"
TWILIO_ACCOUNT_SID= os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN=os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER=os.getenv("TWILIO_WHATSAPP_NUMBER")