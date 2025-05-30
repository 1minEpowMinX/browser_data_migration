import json
from typing import Any
from pathlib import Path
from datetime import datetime

json_structure = {
    "timestamp": datetime.now().isoformat(),
    "browsers": {
        "Firefox": {
            "running": False,
            "tabs": {},
        },
        "Chrome": {
            "running": False,
            "tabs": {},
        },
        "Edge": {
            "running": False,
            "tabs": {},
        },
    },
}


def save_to_json(data: Any, filename: Path | str):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_from_json(filename: Path | str) -> Any:
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)
