from rich.console import Console
from rich.panel import Panel

console = Console()


def print_header(text: str) -> None:
    """
    Prints a header in the console with a specific style.

    Args:
        text (str): The header text to print.
    """

    console.print(Panel(text, style="bold white on blue", expand=False))


def print_success(text: str) -> None:
    """
    Prints a success message in the console.

    Args:
        text (str): The success message to print.
    """

    console.print(f"[bold green]✔ {text}[/]")


def print_warning(text: str) -> None:
    """
    Prints a warning message in the console.

    Args:
        text (str): The warning message to print.
    """

    console.print(f"[bold yellow]⚠ {text}[/]")


def print_error(text: str) -> None:
    """
    Prints an error message in the console.

    Args:
        text (str): The error message to print.
    """

    console.print(f"[bold red]✖ {text}[/]")
