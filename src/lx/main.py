from lx.ollama_client import ask_ollama, OllamaError

def get_user_task() -> str:
    """Prompt the user until they provide non-empty text, then return it."""
    while True:
        user_input = input("What would you like to do? ").strip()
        if user_input:
            return user_input
        print("Please enter a task.")


def main() -> None:
    """Entry point: get the user's task, send it to Ollama, print the response."""
    task = get_user_task()
    print("Thinking...")
    try:
        answer = ask_ollama(task)
    except OllamaError as exc:
        print(f"Error: {exc}")
        return
    print(answer)


if __name__ == "__main__":
    main()