import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma4:e4b"

PROMPT_TEMPLATE = """You are a Linux command-line assistant.
Given a task described in plain English, respond with ONLY a valid JSON object, no other text, no markdown formatting, no code fences.

The JSON object must have exactly these three keys:
- "command": the exact Linux shell command that accomplishes the task
- "explanation": a short, plain-English explanation of what the command does
- "risk": one of "low", "medium", or "high", based on how dangerous the command is (e.g. deleting files, modifying permissions, or making irreversible changes should be "high")

IMPORTANT: The "command" value must be valid JSON string content. If the shell command contains a backslash (for example, to escape parentheses like \\( or \\)), write it as a double backslash so the JSON stays valid. Prefer writing commands that avoid unnecessary backslashes when a simpler equivalent exists (e.g. use quotes around patterns instead of escaping parentheses where possible).

Task: {task}

JSON response:"""


class OllamaError(Exception):
    """Raised when we can't get a valid response from Ollama."""


def ask_ollama(task: str) -> str:
    """Send a task to the local Ollama server and return the raw text response."""
    prompt = PROMPT_TEMPLATE.format(task=task)
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
        },
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