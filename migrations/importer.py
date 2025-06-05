import platform
from pathlib import Path
import subprocess
import shutil

from utils.json_handler import load_from_json
from utils.check_browser_status import (
    BROWSERS,
    is_browser_running,
    kill_browser_process,
)
from utils.logger import logger
from ui.console import (
    print_success,
    print_warning,
    print_error,
)


def restore_profile_files(export_path: Path | str, profile_path: Path | str) -> None:
    """
    Restores a browser profile from an exported path to a specified profile path.

    This function checks if the export path exists, and if so, it copies the contents
    to the profile path, removing any existing profile directory first.

    Args:
        export_path (Path | str): The path to the exported profile directory.
        profile_path (Path | str): The path where the profile should be restored.
    """

    export_path = Path(export_path)
    profile_path = Path(profile_path)

    if not export_path.exists():
        logger.warning(f"Exported profile not found: {export_path}")
        print_warning(f"Экспортированный профиль не найден: {export_path}")
        return

    try:
        if profile_path.exists():
            shutil.rmtree(profile_path)
        shutil.copytree(
            export_path, profile_path, ignore_dangling_symlinks=True, dirs_exist_ok=True
        )
        logger.info(f"Profile restored from {export_path} to {profile_path}")
        print_success(f"Профиль восстановлен из {export_path} в {profile_path}")
    except Exception as e:
        logger.error(f"Error restoring profile: {e}")
        print_error(f"Ошибка при восстановлении профиля: {e}")


def launch_browser_tabs(browser: str, urls: list[str], browser_data: dict) -> None:
    """
    Launches the specified URLs in new tabs of the given browser.

    This function checks if the browser is available, constructs the command to open
    the URLs in new tabs, and executes it. If the browser is not found, it prints an error message.

    Args:
        browser (str): The name of the browser to use.
        urls (list[str]): A list of URLs to open in new tabs.
        browser_data (dict): A dictionary containing browser-specific data.
    """

    commands = []

    if browser_data and "executable" in browser_data:
        system = platform.system()
        commands.extend(browser_data["executable"].get(system, []))

    commands.extend(BROWSERS.get(browser, []))

    cmd_name = ""
    for cmd in commands:
        cmd_path = Path(cmd)
        if cmd_path.is_absolute() and cmd_path.is_file():
            cmd_name = str(cmd_path)
            break
        found = shutil.which(cmd)
        if found:
            cmd_name = found
            break
    else:
        logger.warning(f"{browser} not found in PATH or absolute path.")
        print_warning(f"{browser} не найден ни по абсолютному пути, ни в PATH.")
        return

    # For Firefox, use --new-tab to open multiple URLs in new tabs
    if browser == "Firefox":
        args = [cmd_name, "--new-tab"] + urls
    else:
        args = [cmd_name] + urls

    logger.info(f"Launching {len(urls)} tabs in {browser}")

    try:
        subprocess.Popen(args)
        logger.info(f"Opened {len(urls)} tabs in {browser}")
        print_success(f"Открыто {len(urls)} вкладок в {browser}")
    except Exception as e:
        logger.error(f"Failed to open tabs in {browser}: {e}")
        print_error(f"Не удалось открыть вкладки в {browser}: {e}")


def browser_data_import(session_file: str = "browser_data.json") -> None:
    """
    Imports browser session data from a JSON file and restores the profiles.

    This function reads the session data from the specified JSON file, checks if the
    browsers are running, and if so, kills their processes. It then restores the profiles.

    Args:
        session_file (str): The path to the JSON file containing browser session data. Default is "browser_data.json".
    """

    logger.info("Starting browser data import...")

    try:
        data = load_from_json(session_file)

        for browser_name, browser_data in data["browsers"].items():
            if is_browser_running(browser_name):
                logger.info(f"{browser_name} is running, killing the process.")
                print_warning(f"{browser_name} запущен, процесс будет завершен.")
                kill_browser_process(browser_name)

            export_path = browser_data.get("export_path")
            profile_path = browser_data.get("profile_path")

            if not export_path and not profile_path:
                logger.warning(f"No export or profile path found for {browser_name}.")
                print_warning(
                    f"Не найден путь экспорта или профиля для {browser_name}."
                )
                continue

            restore_profile_files(export_path, profile_path)

            tabs = browser_data.get("tabs", [])
            urls = [tab.get("url") for tab in tabs if tab.get("url")]
            if urls:
                launch_browser_tabs(browser_name, urls, browser_data)

        logger.info("Browser data import completed.")
        print_success("Импорт данных браузера завершен.")
    except Exception as e:
        logger.error(f"Error importing browser data: {e}")
        print_error(f"Ошибка при импорте данных браузера: {e}")
