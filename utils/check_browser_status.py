from datetime import datetime
from typing import Dict

import psutil

# Mapping of browser names to process names (may be different on different platforms)
BROWSERS = {
    "Firefox": ["firefox.exe", "firefox"],
    "Chrome": ["chrome.exe", "chrome"],
    "Edge": ["msedge.exe", "microsoftedge.exe", "msedge"],
}


def is_browser_running(browser: str) -> bool:
    names = BROWSERS.get(browser, [])
    all_names = [name.lower() for name in names]
    for proc in psutil.process_iter(["name"]):
        try:
            if proc.info["name"] and proc.info["name"].lower() in all_names:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False
