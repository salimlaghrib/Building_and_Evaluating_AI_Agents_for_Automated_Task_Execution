import httpx

from app.config import MODEL_NAME, OLLAMA_API_KEY, OLLAMA_BASE_URL


class OllamaClient:
    def __init__(self, base_url: str = OLLAMA_BASE_URL, api_key: str | None = OLLAMA_API_KEY):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _headers(self) -> dict[str, str]:
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _api_url(self, path: str) -> str:
        return f"{self.base_url}/api/{path.lstrip('/')}"

    async def chat(self, message: str, model: str = MODEL_NAME) -> str:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": message}],
            "stream": False,
        }

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                self._api_url("chat"),
                json=payload,
                headers=self._headers(),
            )
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                detail = response.text[:500]
                raise RuntimeError(
                    f"Ollama request failed with HTTP {response.status_code}: {detail}"
                ) from exc

        data = response.json()
        return data.get("message", {}).get("content", "")


ollama_client = OllamaClient()
