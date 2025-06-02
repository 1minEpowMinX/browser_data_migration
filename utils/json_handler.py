import json
from datetime import datetime
from pathlib import Path
from typing import Any


def create_default_json() -> dict:
    return {
        "timestamp": datetime.now().isoformat(),
        "browsers": {
            "Firefox": {"running": False, "tabs": {}},
            "Chrome": {"running": False, "tabs": {}},
            "Edge": {"running": False, "tabs": {}},
        },
    }


def save_to_json(data: Any, filename: Path | str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_from_json(filename: Path | str) -> Any:
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)
