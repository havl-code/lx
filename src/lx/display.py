from rich.console import Console
from rich.markup import escape
from rich.panel import Panel

from lx.parser import command_has_valid_syntax

console = Console()

RISK_COLORS = {
    "low": "green",
    "medium": "yellow",
    "high": "red",
}


def thinking_status():
    """Return a Rich status context manager showing an animated 'thinking' spinner."""
    return console.status("[bold cyan]Thinking...[/bold cyan]")


def display_result(result: dict, target_console: Console = console) -> None:
    """Render the command, explanation, and risk in a styled panel."""
    risk = result["risk"]
    risk_color = RISK_COLORS.get(risk, "white")

    command = escape(result["command"])
    explanation = escape(result["explanation"])

    body = (
        f"[bold]Command:[/bold] {command}\n\n"
        f"[bold]Explanation:[/bold] {explanation}\n\n"
        f"[bold]Risk:[/bold] [{risk_color}]{risk.upper()}[/{risk_color}]"
    )

    if not command_has_valid_syntax(result["command"]):
        body += (
            "\n\n[bold red]⚠ Warning:[/bold red] this command failed a basic "
            "syntax check and may not run correctly. Review it carefully before using."
        )

    target_console.print(Panel(body, title="lx result", border_style=risk_color))