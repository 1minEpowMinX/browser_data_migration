from rich.panel import Panel
from rich.prompt import IntPrompt

from migrations.exporter import browser_data_export
from migrations.importer import browser_data_import
from ui.console import console
from ui.status import status_bar


help_text = """
[bold cyan]Помощь[/bold cyan]

Приложение предназначено для переноса данных браузеров Chrome, Edge и Firefox между компьютерами.

[bold green]1. Экспорт данных[/bold green] — сохраняет:
  • текущие открытые вкладки;
  • профили браузеров (настройки, расширения, кэш и прочее).

[bold green]2. Импорт данных[/bold green] — восстанавливает вкладки и профили из ранее сохранённых данных.

Результат сохраняется в файл [bold]browser_data.json[/bold] и директорию с папками профилей в текущей папке.

[bold yellow]Важно:[/bold yellow]
  • производите перенос между одинаковыми профилями, либо редактируйте путь
    [bold]browser_data.json["browsers"][<browser_name>]["export_path"][/bold] после экспорта;
  • если вы хотите, чтобы вкладки были автоматически восстановлены после переноса —
    не закрывайте браузер. Программа сделает это автоматически.
"""


def main_menu() -> None:
    """
    The main CLI application menu.

    This function displays a menu with options for exporting and importing browser data,
    as well as displaying help information.
    """

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
                    browser_data_export()
            case 2:
                with status_bar("Импорт данных браузера"):
                    browser_data_import()
            case 3:
                console.print(
                    Panel(
                        help_text,
                        title="[bold yellow]Как пользоваться?[/bold yellow]",
                        border_style="bright_blue",
                        width=100,
                    )
                )
            case 0:
                console.print("[bold cyan]Выход из приложения...[/bold cyan]")
                break

        console.input("\n[bold cyan]Нажмите Enter для возврата в меню...[/bold cyan]")
