from os import path
from platform import system
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

    This function returns the path to the browser profile directory for Chrome, Edge, or Firefox.
    It uses environment variables for Windows paths and expands user directories for Linux paths.

    Args:
        browser (str): The name of the browser (e.g., "Chrome", "Edge", "Firefox").

    Raises:
        NotImplementedError: If the browser is unknown or not supported on the current OS.

    Returns:
        str: The path to the browser profile directory, or None if the browser is not supported.
    """

    match system():
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
    """
    Safely ignore files that cannot be accessed in the source directory.

    This function checks each file in the source directory and adds it to the ignore list
    if it cannot be opened. This is useful for avoiding errors when copying files.

    Args:
        src (Path | str): The source directory path.
        names (list[str]): List of file names in the source directory.

    Returns:
        list[str]: A list of file names that could not be accessed.
    """

    ignore_list = []
    src_path = Path(src)
    for name in names:
        full_path = src_path / name
        if full_path.is_dir():
            continue  # Skip directories, they will be handled by shutil.copytree
        try:
            # try to open the file to check if it is accessible
            with open(full_path, "rb"):
                pass
        except Exception:
            ignore_list.append(name)

    return ignore_list
