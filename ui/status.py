from contextlib import contextmanager

from ui.console import console


@contextmanager
def status_bar(message: str, spinner: str = "dots"):
    with console.status(f"[cyan]{message}...", spinner=spinner):
        yield
    console.log(f"[green]{message} завершено.[/green]")
