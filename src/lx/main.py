from lx.ollama_client import get_structured_response, OllamaError, ResponseParseError
from lx.display import display_result
from lx.clipboard import prompt_copy_to_clipboard

def get_user_task() -> str:
    """Prompt the user until they provide non-empty text, then return it."""
    while True:
        user_input = input("What would you like to do? ").strip()
        if user_input:
            return user_input
        print("Please enter a task.")


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
    prompt_copy_to_clipboard(result["command"])


if __name__ == "__main__":
    main()