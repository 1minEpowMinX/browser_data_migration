from json import dump, load
from datetime import datetime
from pathlib import Path


def create_default_json() -> dict:
    """
    Creates a default JSON structure for browser session data.

    This function initializes a JSON structure with default values for browsers,
    including their running status, tabs, profile paths, executable paths, and export paths.
    Additionally it sets minimal application configuration.

    Returns:
        dict: The default JSON structure.
    """

    return {
        "ui_language": "en",  # "en" or "ru" at the moment
        "timestamp": datetime.now().isoformat(),
        "browsers": {
            "Firefox": {
                "running": False,
                "tabs": [],
                "profile_path": r"",
                "executable": {
                    "Windows": [
                        r"C:/Program Files/Mozilla Firefox/firefox.exe",
                        r"C:/Program Files (x86)/Mozilla Firefox/firefox.exe",
                    ],
                    "Linux": [r"/usr/bin/firefox"],
                },
                "export_path": "",
            },
            "Chrome": {
                "running": False,
                "tabs": [],
                "profile_path": r"",
                "executable": {
                    "Windows": [
                        r"C:/Program Files/Google\Chrome/Application/chrome.exe",
                        r"C:/Program Files (x86)/Google\Chrome/Application/chrome.exe",
                    ],
                    "Linux": [r"/usr/bin/google-chrome", r"/usr/bin/chromium-browser"],
                },
                "export_path": "",
            },
            "Edge": {
                "running": False,
                "tabs": [],
                "profile_path": r"",
                "executable": {
                    "Windows": [
                        r"C:/Program Files/Microsoft/Edge/Application/msedge.exe",
                        r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
                    ],
                    "Linux": [r"/usr/bin/microsoft-edge", r"/usr/bin/msedge"],
                },
                "export_path": "",
            },
        },
    }


def save_to_json(data: dict, filename: Path | str) -> None:
    """
    Saves the given data to a JSON file.

    This function writes the provided data dictionary to a specified JSON file.
    It raises a ValueError if the specified file is not a JSON file.

    Args:
        data (dict): The data to save.
        filename (Path | str): The path to the JSON file.

    Raises:
        ValueError: If the specified file is not a JSON file.
    """

    if not str(filename).endswith(".json"):
        raise ValueError(f"File '{filename}' is not a JSON file.")

    with open(filename, "w", encoding="utf-8") as f:
        dump(data, f, indent=4, ensure_ascii=False)


def load_from_json(filename: Path | str) -> dict:
    """
    Loads data from a JSON file.

    This function reads a JSON file and returns the data as a dictionary.
    It raises a FileNotFoundError if the specified file does not exist,
    and a ValueError if the specified file is not a JSON file.

    Args:
        filename (Path | str): The path to the JSON file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the specified file is not a JSON file.

    Returns:
        dict: The data loaded from the JSON file.
    """

    if not Path(filename).exists():
        raise FileNotFoundError(f"File '{filename}' does not exist.")

    if not str(filename).endswith(".json"):
        raise ValueError(f"File '{filename}' is not a JSON file.")

    with open(filename, "r", encoding="utf-8") as f:
        return load(f)
