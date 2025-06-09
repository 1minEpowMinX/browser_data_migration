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
                "[bold cyan]Menu[/bold cyan]\n"
                "1. Экспорт данных\n"
                "2. Импорт данных\n"
                "3. Помощь\n"
                "0. Выход",
                title="[bold yellow]Browser Data Migration[/bold yellow]",
                border_style="bright_blue",
            )
        )

        choice = IntPrompt.ask(
            "\n[bold green]Выберите действие[/bold green]", choices=["1", "2", "3", "0"]
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
            case 3:
                console.print(
                    Panel.fit(
                        "[bold cyan]Помощь[/bold cyan]\n\n"
                        "Приложение предназначено для переноса данных браузеров Chrome, Edge и Firefox между компьютерами.\n\n"
                        "[bold green]1. Экспорт данных[/bold green] — сохраняет:\n"
                        "   • текущие открытые вкладки;\n"
                        "   • профили браузеров (настройки, расширения, кэш и прочее).\n\n"
                        "[bold green]2. Импорт данных[/bold green] — восстанавливает вкладки и профили из ранее сохранённых данных.\n\n"
                        "Результат сохраняется в файл [bold]browser_data.json[/bold] и директорию с папками профилей в текущей папке.\n\n"
                        "[bold yellow]Важно:[/bold yellow] Если вы хотите чтобы вкладки снова были открыты после переноса - не закрывайте браузер. Программа сделает это автоматически.\n",
                        title="[bold cyan]Как пользоваться?[/bold cyan]",
                        border_style="bright_blue",
                    )
                )
            case 0:
                console.print("[bold cyan]Выход из приложения...[/bold cyan]")
                break

        console.input("\n[bold cyan]Нажмите Enter для возврата в меню...[/bold cyan]")
