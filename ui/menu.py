from rich.panel import Panel
from rich.prompt import IntPrompt

from migrations.exporter import browser_data_export
from migrations.importer import browser_data_import
from ui.console import console
from ui.status import status_bar


def main_menu():
    while True:
        console.clear()
        console.print()
        console.print(
            Panel.fit(
                "[bold cyan]Меню переноса данных браузеров[/bold cyan]\n"
                "1. Экспорт данных\n"
                "2. Импорт данных\n"
                "0. Выход",
                title="[bold yellow]Browser Data Migration[/bold yellow]",
                border_style="bright_blue",
            )
        )

        choice = IntPrompt.ask(
            "\n[bold green]Выберите действие[/bold green]", choices=["1", "2", "0"]
        )

        match choice:
            case 1:
                with status_bar("Экспорт данных браузера"):
                    try:
                        console.print(
                            "\n[bold green]Начинается экспорт данных...[/bold green]"
                        )
                        browser_data_export()
                        console.print(
                            "[bold green]Экспорт успешно завершен![/bold green]"
                        )
                    except Exception as e:
                        console.print(f"[bold red]Ошибка при экспорте: {e}[/bold red]")
            case 2:
                with status_bar("Импорт данных браузера"):
                    try:
                        console.print(
                            "\n[bold green]Начинается импорт данных...[/bold green]"
                        )
                        browser_data_import()
                        console.print(
                            "[bold green]Импорт успешно завершен![/bold green]"
                        )
                    except Exception as e:
                        console.print(f"[bold red]Ошибка при импорте: {e}[/bold red]")
            case 0:
                console.print("[bold red]Выход...[/bold red]")
                break

        console.input("\n[cyan]Нажмите Enter для возврата в меню...[/cyan]")
