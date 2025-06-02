import psutil

# Mapping of browser names to process names (may be different on different platforms)
BROWSERS = {
    "Firefox": ["firefox.exe", "firefox"],
    "Chrome": ["chrome.exe", "chrome"],
    "Edge": ["msedge.exe", "microsoftedge.exe", "msedge"],
}


def is_browser_running(browser: str) -> bool:
    """Check if a specified browser is currently running.

    Args:
        browser (str): The name of the browser to check.

    Raises:
        ValueError: If the browser is unknown or not supported.

    Returns:
        bool: True if the browser is running, False otherwise.
    """

    names = BROWSERS.get(browser, [])
    if not names:
        raise ValueError(f"Error: unknown browser {browser}")

    all_names = [name.lower() for name in names]
    for proc in psutil.process_iter():
        try:
            proc_name = proc.name()
            if proc_name and proc_name.lower() in all_names:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


def kill_browser_process(browser: str):
    """
    Kills all processes associated with the specified browser by matching process names.

    Args:
        browser (str): The name of the browser to kill processes for.

    Raises:
        ValueError: If the browser is unknown or not supported.
    """

    targets = BROWSERS.get(browser, [])
    if not targets:
        raise ValueError(f"Error: unknown browser {browser}")

    all_names = [name.lower() for name in targets]
    for proc in psutil.process_iter():
        try:
            proc_name = proc.name()
            if proc_name and proc_name.lower() in all_names:
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
