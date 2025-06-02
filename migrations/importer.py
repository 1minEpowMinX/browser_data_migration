import os
import platform
import subprocess
import shutil

from utils.json_handler import load_from_json
from utils.check_browser_status import BROWSERS


def launch_browser_tabs(browser: str, urls: list[str], browser_data: dict):
    commands = []

    if browser_data and "executable" in browser_data:
        system = platform.system()
        commands.extend(browser_data["executable"].get(system, []))

    commands.extend(BROWSERS.get(browser, []))

    cmd_name = None
    for cmd in commands:
        if os.path.isabs(cmd) and os.path.isfile(cmd) and os.access(cmd, os.X_OK):
            cmd_name = cmd
            break
        if shutil.which(cmd):
            cmd_name = shutil.which(cmd)
            break
    else:
        print(f"[!] {browser} не найден ни по абсолютному пути, ни в PATH.")
        return

    # For Firefox, use --new-tab to open multiple URLs in new tabs
    if browser == "Firefox":
        args = [cmd_name, "--new-tab"] + urls
    else:
        args = [cmd_name] + urls

    try:
        subprocess.Popen(args)
        print(f"[+] Запущено {len(urls)} вкладок в {browser}")
    except Exception as e:
        print(f"[!] Не удалось открыть вкладки в {browser}: {e}")


def browser_data_import(session_file="browser_sessions.json"):
    data = load_from_json(session_file)

    for browser_name, browser_data in data["browsers"].items():
        tabs = browser_data.get("tabs", [])
        urls = [tab.get("url") for tab in tabs if tab.get("url")]
        if urls:
            launch_browser_tabs(browser_name, urls, browser_data)
