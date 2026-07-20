import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma4:e4b"


class OllamaError(Exception):
    """Raised when we can't get a valid response from Ollama."""


def ask_ollama(prompt: str) -> str:
    """Send a prompt to the local Ollama server and return the raw text response."""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as exc:
        raise OllamaError(
            "Could not connect to Ollama. Is it running? Try: ollama serve"
        ) from exc
    except requests.exceptions.HTTPError as exc:
        raise OllamaError(f"Ollama returned an error: {exc}") from exc

    data = response.json()
    return data["response"]