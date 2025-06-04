import os
import shutil
from typing import Optional, Union

from session_parsers.chromium_parser import find_latest_snss_file, parse_snss_file
from session_parsers.firefox_parser import find_latest_recovery_file, parse_jsonlz4_file
from structrues.chormium_structures import ChromiumTab
from structrues.firefox_structures import FirefoxTab
from utils.check_browser_status import is_browser_running, kill_browser_process
from utils.browser_paths import get_browser_profile_path
from utils.json_handler import create_default_json, save_to_json


def tab_to_dict(tab: Union[ChromiumTab, FirefoxTab]) -> Optional[dict]:
    """
    Converts a browser tab object to a dictionary representation.

    This function extracts the URL and title from the tab object if available,
    and returns a dictionary with these details. If the tab does not have entries.

    Args:
        tab (Union[ChromiumTab, FirefoxTab]): The tab object to convert.

    Returns:
        Optional[dict]: A dictionary representation of the tab or None if not convertible.
    """

    if tab.entries and 0 <= tab.index < len(tab.entries):
        entry = tab.entries[tab.index]
        return {
            "url": getattr(entry, "url", ""),
            "title": getattr(entry, "title", ""),
        }
    return None


def safe_ignore_errors(src, names):
    ignore_list = []
    for name in names:
        full_path = os.path.join(src, name)
        try:
            # try to open the file to check if it is accessible
            with open(full_path, "rb"):
                pass
        except Exception:
            ignore_list.append(name)
    return ignore_list


def export_profile_files(browser: str, profile_path: str, output_root: str) -> str:
    """
    Copies the full browser profile directory to a destination folder.

    Args:
        browser (str): Browser name (used to name the export folder).
        profile_path (str): Path to the profile directory to copy.
        output_root (str): Root output directory for all exports.

    Returns:
        str: The destination path or error message.
    """
    if not os.path.exists(profile_path):
        print(f"[!] Профиль {browser} не найден по пути: {profile_path}")
        return ""

    destination = os.path.join(output_root, browser)
    try:
        # Очистим предыдущую копию, если она была
        if os.path.exists(destination):
            shutil.rmtree(destination)

        shutil.copytree(
            profile_path,
            destination,
            ignore=safe_ignore_errors,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=False,
        )
        return destination
    except Exception as e:
        raise ValueError(f"Error exporting profile files: {e}")


def get_browser_data(json: dict, browser: str) -> None:
    """
    Retrieves browser session data for the specified browser and updates the JSON structure.

    This function checks the browser's profile path, retrieves the latest session file,
    and extracts tab information to populate the JSON structure.

    Args:
        json (dict): The JSON structure to update with browser data.
        browser (str): The name of the browser to retrieve data for.
    """

    browser_path = get_browser_profile_path(browser)
    json["browsers"][browser]["profile_path"] = browser_path
    if not browser_path:
        return

    if browser == "Firefox":
        recovery_file = find_latest_recovery_file(browser_path)
        if recovery_file:
            firefox_windows = parse_jsonlz4_file(recovery_file)
            tabs = [
                tab_to_dict(tab) for window in firefox_windows for tab in window.tabs
            ]
            # Filter out None values from tabs
            json["browsers"]["Firefox"]["tabs"] = [t for t in tabs if t]
    else:
        snss_file = find_latest_snss_file(browser_path)
        if snss_file:
            browser_windows = parse_snss_file(snss_file)
            tabs = [tab_to_dict(tab) for tab in browser_windows.tabs]
            json["browsers"][browser]["tabs"] = [t for t in tabs if t]

    export_dir = "exported_profiles"
    export_result = export_profile_files(browser, browser_path, export_dir)
    json["browsers"][browser]["export_path"] = export_result


def browser_data_export():
    """
    Exports browser session data for all supported browsers into a JSON file.

    This function checks if each browser is running, kills the process if it is,
    retrieves the session data, and saves it to a JSON file named 'browser_sessions.json'.
    """

    json = create_default_json()

    for browser in json["browsers"]:
        running = is_browser_running(browser)
        json["browsers"][browser]["running"] = running
        if running:
            print(
                f"[!] {browser} запущен, завершаем процесс для безопасного экспорта..."
            )
            kill_browser_process(browser)
        get_browser_data(json, browser)

    save_to_json(json, "browser_sessions.json")
