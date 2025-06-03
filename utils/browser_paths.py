from os import path
import platform
from pathlib import Path
from typing import Optional

CHROME_PATH = (r"%LOCALAPPDATA%/Google/Chrome/", r"~/.config/google-chrome/")
EDGE_PATH = (r"%LOCALAPPDATA%/Microsoft/Edge/", r"~/.config/microsoft-edge/")
FIREFOX_PATH = (
    r"%APPDATA%/Mozilla/Firefox/",
    r"~/snap/firefox/common/.mozilla/firefox/",
)


def get_browser_profile_path(browser: str) -> Optional[str]:
    """
    Get the default path for browser profiles based on the operating system and browser type.

    Args:
        browser (str): The name of the browser (e.g., "Chrome", "Edge", "Firefox").

    Raises:
        NotImplementedError: If the browser is unknown or not supported on the current OS.

    Returns:
        str: The path to the browser profile directory, or None if the browser is not supported.
    """

    match platform.system():
        case "Windows":
            if browser == "Chrome":
                return path.expandvars(CHROME_PATH[0])
            elif browser == "Edge":
                return path.expandvars(EDGE_PATH[0])
            elif browser == "Firefox":
                return path.expandvars(FIREFOX_PATH[0])
            else:
                raise NotImplementedError(
                    f"Error: Unknown browser {browser} for Windows"
                )
        case "Linux":
            if browser == "Chrome":
                return path.expanduser(CHROME_PATH[1])
            elif browser == "Edge":
                return path.expanduser(EDGE_PATH[1])
            elif browser == "Firefox":
                return path.expanduser(FIREFOX_PATH[1])
            else:
                raise NotImplementedError(f"Error: Unknown browser {browser} for Linux")
        case _:
            raise NotImplementedError("Error: Unknown OS type")


def safe_ignore_errors(src: Path | str, names: list[str]) -> list[str]:
    ignore_list = []
    src_path = Path(src)
    for name in names:
        full_path = src_path / name
        if full_path.is_file():
            try:
                # try to open the file to check if it is accessible
                with open(full_path, "rb"):
                    pass
            except Exception:
                ignore_list.append(name)
    return ignore_list
