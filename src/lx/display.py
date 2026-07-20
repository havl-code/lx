from rich.console import Console
from rich.panel import Panel

console = Console()

RISK_COLORS = {
    "low": "green",
    "medium": "yellow",
    "high": "red",
}


def display_result(result: dict) -> None:
    """Render the command, explanation, and risk in a styled panel."""
    risk = result["risk"]
    risk_color = RISK_COLORS.get(risk, "white")

    body = (
        f"[bold]Command:[/bold] {result['command']}\n\n"
        f"[bold]Explanation:[/bold] {result['explanation']}\n\n"
        f"[bold]Risk:[/bold] [{risk_color}]{risk.upper()}[/{risk_color}]"
    )

    console.print(Panel(body, title="lx result", border_style=risk_color))