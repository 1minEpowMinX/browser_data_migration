import psutil
from datetime import datetime
from typing import Dict, Union, Any

from utils import json_handler

# Mapping of browser names to process names (may be different on different platforms)
BROWSERS = {
    "Firefox": ["firefox.exe", "firefox"],
    "Chrome": ["chrome.exe", "chrome"],
    "Edge": ["msedge.exe", "microsoftedge.exe", "msedge"],
}


def is_browser_running(process_names: Dict[str, list[str]]) -> bool:
    for proc in psutil.process_iter(["name"]):
        try:
            if proc.info["name"] and proc.info["name"].lower() in [
                name.lower() for name in process_names
            ]:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


def generate_report() -> Dict[str, Union[str, Dict[str, Dict[str, Any]]]]: # TODO: implement this function in different way
    report = {"timestamp": datetime.now().isoformat(), "browsers": {}}

    for browser, process_names in BROWSERS.items():
        report["browsers"][browser] = {"running": is_browser_running(process_names)}

    return report


def save_report_to_json(report, filename="browser_status_report.json"):
    json_handler.save_to_json(report, filename)

