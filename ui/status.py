from contextlib import contextmanager
from typing import Generator

from ui.console import console


@contextmanager
def status_bar(message: str, spinner: str = "dots") -> Generator[None, None, None]:
    """
    Displays a status bar with a message and spinner.

    Args:
        message (str): The message to display.
        spinner (str, optional): The spinner to use. Defaults to "dots".

    Yields:
        Generator[None, None, None]: None.
    """

    console.print()
    console.log(f"[green]{message} запущен...[/green]")
    try:
        with console.status(f"[cyan]{message}...", spinner=spinner):
            yield
    except Exception as e:
        console.log(f"[red]{message} завершен с ошибкой: {e}[/red]")
    else:
        console.log(f"[green]{message} завершен успешно.[/green]")
