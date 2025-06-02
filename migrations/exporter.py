from typing import Optional

from utils.check_browser_status import is_browser_running, kill_browser_process
from utils.browser_paths import get_browser_profile_path
from utils.json_handler import create_default_json, save_to_json
from session_parsers.chromium_parser import find_latest_snss_file, parse_snss_file
from session_parsers.firefox_parser import find_latest_recovery_file, parse_jsonlz4_file


def tab_to_dict(tab) -> Optional[dict]:
    # Безопасно получаем url и title текущей вкладки
    if tab.entries and 0 <= tab.index < len(tab.entries):
        entry = tab.entries[tab.index]
        return {
            "url": getattr(entry, "url", ""),
            "title": getattr(entry, "title", ""),
        }
    return None


def get_browser_data(json: dict, browser: str) -> None:
    browser_path = get_browser_profile_path(browser)
    json["browsers"][browser]["path"] = browser_path
    if not browser_path:
        return

    if browser == "Firefox":
        recovery_file = find_latest_recovery_file(browser_path)
        if recovery_file:
            firefox_windows = parse_jsonlz4_file(recovery_file)
            tabs = [
                tab_to_dict(tab) for window in firefox_windows for tab in window.tabs
            ]
            # Убираем None, если вкладка невалидна
            json["browsers"]["Firefox"]["tabs"] = [t for t in tabs if t]
    else:
        snss_file = find_latest_snss_file(browser_path)
        if snss_file:
            browser_windows = parse_snss_file(snss_file)
            tabs = [tab_to_dict(tab) for tab in browser_windows.tabs]
            json["browsers"][browser]["tabs"] = [t for t in tabs if t]


def browser_data_export():
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
