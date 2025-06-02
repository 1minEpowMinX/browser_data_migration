import json
from datetime import datetime
from pathlib import Path
from typing import Any


def create_default_json() -> dict:
    """Creates a default JSON structure for browser session data.

    Returns:
        dict: The default JSON structure.
    """
    return {
        "timestamp": datetime.now().isoformat(),
        "browsers": {
            "Firefox": {"running": False, "tabs": [], "path": r""},
            "Chrome": {"running": False, "tabs": [], "path": r""},
            "Edge": {"running": False, "tabs": [], "path": r""},
        },
    }


def save_to_json(data: Any, filename: Path | str) -> None:
    """Saves the given data to a JSON file.

    Args:
        data (Any): The data to save.
        filename (Path | str): The path to the JSON file.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_from_json(filename: Path | str) -> Any:
    """Loads data from a JSON file.

    Args:
        filename (Path | str): The path to the JSON file.
    """

    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)
