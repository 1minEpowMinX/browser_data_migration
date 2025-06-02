from utils.check_browser_status import is_browser_running, kill_browser_process
from utils.browser_paths import (
    get_chrome_profile_path,
    get_edge_profile_path,
    get_firefox_profiles_path,
)
from utils.json_handler import create_default_json, save_to_json
from session_parsers.chromium_parser import find_latest_snss_file, parse_snss_file
from session_parsers.firefox_parser import find_latest_recovery_file, parse_jsonlz4_file


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

    chrome_path = get_chrome_profile_path()
    json["browsers"]["Chrome"]["path"] = chrome_path
    if chrome_path:
        snss_file = find_latest_snss_file(chrome_path)
        if snss_file:
            chrome_windows = parse_snss_file(snss_file)
            json["browsers"]["Chrome"]["tabs"] = [
                {
                    "url": tab.entries[tab.index].url,
                    "title": tab.entries[tab.index].title,
                }
                for tab in chrome_windows.tabs
                if tab.entries
                and 0
                <= tab.index
                < len(
                    tab.entries
                )  # TODO: Make sure the tab index is set correctly in session_parsers/chromium_parser.py
            ]

    edge_path = get_edge_profile_path()
    json["browsers"]["Edge"]["path"] = edge_path
    if edge_path:
        snss_file = find_latest_snss_file(edge_path)
        if snss_file:
            edge_windows = parse_snss_file(snss_file)
            json["browsers"]["Edge"]["tabs"] = [
                {
                    "url": tab.entries[tab.index].url,
                    "title": tab.entries[tab.index].title,
                }
                for tab in edge_windows.tabs
                if tab.entries and 0 <= tab.index < len(tab.entries)
            ]

    firefox_path = get_firefox_profiles_path()
    json["browsers"]["Firefox"]["path"] = firefox_path
    if firefox_path:
        recovery_file = find_latest_recovery_file(firefox_path)
        if recovery_file:
            firefox_windows = parse_jsonlz4_file(recovery_file)
            json["browsers"]["Firefox"]["tabs"] = [
                {
                    "url": tab.entries[tab.index].url,
                    "title": tab.entries[tab.index].title,
                }
                for window in firefox_windows
                for tab in window.tabs
                if tab.entries and 0 <= tab.index < len(tab.entries)
            ]

    save_to_json(json, "browser_sessions.json")
