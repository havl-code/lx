def get_user_task() -> str:
    """Prompt the user until they provide non-empty text, then return it."""
    while True:
        user_input = input("What would you like to do? ").strip()
        if user_input:
            return user_input
        print("Please enter a task.")


def main() -> None:
    """Entry point: get the user's task and print it back."""
    task = get_user_task()
    print(f"You said: {task}")


if __name__ == "__main__":
    main()