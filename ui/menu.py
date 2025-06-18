from pathlib import Path
from rich.panel import Panel
from rich.prompt import IntPrompt

from migrations.exporter import browser_data_export
from migrations.importer import browser_data_import
from ui.console import console
from ui.status import status_bar
from utils.get_browser_profile_paths import get_user_profiles, select_user_profile
from utils.logger import logger


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


def get_valid_user_profile(action: str) -> Path:
    """
    Get a valid user profile path.

    This function prompts the user to select a user profile and returns the selected path.
    If no user profiles are found, it raises an exception.

    Args:
        action (str): The action to perform on the user profile.

    Raises:
        RuntimeError: If the user profile path is not valid.

    Returns:
        Path: The valid user profile path.
    """

    try:
        user_profiles = get_user_profiles()
        if not user_profiles:
            logger.error(f"User profiles not found to {action} data.")
            raise RuntimeError(f"User profiles not found to {action} data.")

        user_profile_path = select_user_profile(user_profiles)
        if not user_profile_path:
            logger.error(f"User profile not selected to {action} data.")
            raise RuntimeError(f"User profile not selected to {action} data.")

        return user_profile_path
    except Exception as e:
        raise RuntimeError(f"Ошибка выбора профиля: {e}")


def main_menu() -> None:
    """
    The main CLI application menu.

    This function displays a menu with options for exporting and importing browser data,
    as well as displaying help information.

    Raises:
        RuntimeError: If the user profile path is not valid.
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
            "\n[bold cyan]Выберите действие:[/bold cyan]",
            default=3,
            choices=["1", "2", "3", "0"],
        )

        match choice:
            case 1:
                try:
                    user_profile_path = get_valid_user_profile("export")
                except Exception as e:
                    raise RuntimeError(f"Ошибка выбора профиля: {e}")

                with status_bar("Экспорт данных браузера"):
                    browser_data_export(user_profile_path)
            case 2:
                console.print(
                    "\n[bold cyan]Выберите режим:\n[/bold cyan][bold green]1.[/bold green] Использовать путь из JSON\n[green]2.[/green] Выбрать профиль вручную\n"
                )

                choice = IntPrompt.ask(
                    "\n[bold cyan]Выберите действие:[/bold cyan]",
                    default=1,
                    choices=["1", "2"],
                )

                try:
                    user_profile_path = get_valid_user_profile("import")
                except Exception as e:
                    raise RuntimeError(f"Ошибка выбора профиля: {e}")

                with status_bar("Импорт данных браузера"):
                    browser_data_import(user_profile_path)
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
