import os

from lx.ollama_client import (
    list_available_models,
    get_structured_response,
    OllamaError,
    ResponseParseError,
)
from lx.display import display_result, thinking_status
from lx.clipboard import prompt_copy_to_clipboard


def get_user_task() -> str:
    """Prompt the user until they provide non-empty text, then return it."""
    while True:
        user_input = input("What would you like to do? ").strip()
        if user_input:
            return user_input
        print("Please enter a task.")


def choose_model() -> str:
    """List locally available models and let the user pick one."""
    models = list_available_models()
    print("Available models:")
    for index, name in enumerate(models, start=1):
        print(f"  {index}. {name}")

    while True:
        choice = input(f"Choose a model [1-{len(models)}]: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(models):
            return models[int(choice) - 1]
        print("Invalid choice, try again.")


def main() -> None:
    """Entry point: get the user's task, send it to Ollama, parse and display the result."""
    env_model = os.environ.get("LX_MODEL")

    try:
        model = env_model if env_model else choose_model()
    except OllamaError as exc:
        print(f"Error: {exc}")
        return

    task = get_user_task()

    try:
        with thinking_status():
            result = get_structured_response(task, model)
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