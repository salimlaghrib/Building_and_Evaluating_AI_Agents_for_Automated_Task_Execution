from app.config import _normalize_ollama_base_url
from app.services.ollama.client import OllamaClient


def test_ollama_base_url_strips_api_suffix():
    assert _normalize_ollama_base_url("https://ollama.com/api") == "https://ollama.com"


def test_ollama_client_builds_api_chat_url_once():
    client = OllamaClient(base_url="https://ollama.com", api_key="test-key")

    assert client._api_url("chat") == "https://ollama.com/api/chat"
