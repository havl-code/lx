from rich.console import Console
from rich.markup import escape
from rich.panel import Panel

console = Console()

RISK_COLORS = {
    "low": "green",
    "medium": "yellow",
    "high": "red",
}


def thinking_status():
    """Return a Rich status context manager showing an animated 'thinking' spinner."""
    return console.status("[bold cyan]Thinking...[/bold cyan]")


def display_result(result: dict) -> None:
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

    console.print(Panel(body, title="lx result", border_style=risk_color))