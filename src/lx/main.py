from lx.ollama_client import ask_ollama, OllamaError
from lx.parser import parse_llm_response, ResponseParseError
from lx.display import display_result

MAX_ATTEMPTS = 3


def get_user_task() -> str:
    """Prompt the user until they provide non-empty text, then return it."""
    while True:
        user_input = input("What would you like to do? ").strip()
        if user_input:
            return user_input
        print("Please enter a task.")


def get_structured_response(task: str) -> dict:
    """Ask Ollama for a structured response, retrying on parse failure."""
    last_error: ResponseParseError | None = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        raw_response = ask_ollama(task)
        try:
            return parse_llm_response(raw_response)
        except ResponseParseError as exc:
            last_error = exc
            print(f"Attempt {attempt} failed to parse, retrying...")

    raise last_error


def main() -> None:
    """Entry point: get the user's task, send it to Ollama, parse and display the result."""
    task = get_user_task()
    print("Thinking...")

    try:
        result = get_structured_response(task)
    except OllamaError as exc:
        print(f"Error: {exc}")
        return
    except ResponseParseError as exc:
        print(f"Error: {exc}")
        return

    print()
    display_result(result)


if __name__ == "__main__":
    main()