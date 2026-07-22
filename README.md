# Building-and-Evaluating-AI-Agents

## Ollama configuration

Local Ollama:

```env
MODEL_PROVIDER=ollama
MODEL_NAME=llama3.1
OLLAMA_BASE_URL=http://localhost:11434
```

Ollama cloud with API key:

```env
MODEL_PROVIDER=ollama
MODEL_NAME=gpt-oss:120b
OLLAMA_BASE_URL=https://ollama.com
OLLAMA_API_KEY=your_api_key
```

Ollama cloud through a signed-in local installation:

```env
MODEL_PROVIDER=ollama
MODEL_NAME=gpt-oss:120b-cloud
OLLAMA_BASE_URL=http://localhost:11434
```

If `OLLAMA_BASE_URL` is set to `https://ollama.com/api`, the app normalizes it to
`https://ollama.com` before calling `/api/chat`.
