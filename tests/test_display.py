import io

from rich.console import Console

from lx.display import display_result


def render_to_string(result: dict) -> str:
    """Render a result using display_result, capturing output as plain text."""
    buffer = io.StringIO()
    test_console = Console(file=buffer, width=100)
    display_result(result, target_console=test_console)
    return buffer.getvalue()


def test_displays_plain_command_correctly():
    result = {"command": "ls -la", "explanation": "Lists files.", "risk": "low"}
    output = render_to_string(result)
    assert "ls -la" in output
    assert "Lists files." in output
    assert "LOW" in output


def test_escapes_brackets_in_command_so_they_are_not_swallowed():
    result = {
        "command": "[find /var/log -name '*.log' -delete]",
        "explanation": "Deletes old logs.",
        "risk": "low",
    }
    output = render_to_string(result)
    assert "find /var/log -name '*.log' -delete" in output