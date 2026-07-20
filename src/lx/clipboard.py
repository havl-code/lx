import pyperclip


def copy_to_clipboard(text: str) -> None:
    """Copy the given text to the system clipboard."""
    pyperclip.copy(text)


def prompt_copy_to_clipboard(command: str) -> None:
    """Ask the user whether to copy the command, and do so if they confirm."""
    answer = input("Copy command to clipboard? [y/N] ").strip().lower()
    if answer == "y":
        copy_to_clipboard(command)
        print("Copied.")