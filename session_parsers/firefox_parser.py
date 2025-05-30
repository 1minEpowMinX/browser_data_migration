from pathlib import Path
from typing import Optional, List
import json

import lz4.block

from structrues.firefox_structures import (
    FirefoxNavigationEntry,
    FirefoxTab,
    FirefoxWindow,
)

"""
This module contains the extended base structures used by the Firefox session parser.
"""


## Firefox Session Format
# Firefox uses a compressed JSON file (e.g., recovery.jsonlz4) to store session data.

# File layout:
#   "mozLz40\0"                           # Magic header
#   LZ4-compressed UTF-8 JSON payload

# After decompression:
# {
#     "windows": [
#         {
#             "tabs": [
#                 {
#                     "entries": [
#                         { "url": "...", "title": "...", "referrer": "...", "lastAccessed": ... },
#                         ...
#                     ],
#                     "index": 1,         # 1-based index of selected entry
#                     "pinned": false,
#                     "hidden": false
#                 },
#                 ...
#             ]
#         },
#         ...
#     ]
# }

# Notes:
# - "entries" is the tab's full history stack.
# - "index" points to the active entry.
# - Format is stable across recent Firefox versions.

# Source:
# https://searchfox.org/mozilla-central/source/browser/components/sessionstore


def parse_jsonlz4_file(path: Path | str) -> List[FirefoxWindow]:
    """
    Parses a Firefox session file (e.g., recovery.jsonlz4) and returns structured FirefoxWindow objects.

    The session file must begin with the `mozLz40\0` magic header and contain an LZ4-compressed JSON payload.

    Args:
        path (Path | str): Path to the .jsonlz4 file to parse.

    Returns:
        List[FirefoxWindow]: A list of FirefoxWindow objects representing the session.
    """
    with open(path, "rb") as f:
        magic = f.read(8)
        if magic != b"mozLz40\0":
            raise ValueError("Not a valid Firefox session file.")
        compressed = f.read()
        json_bytes = lz4.block.decompress(compressed)
        data = json.loads(json_bytes)

    windows: List[FirefoxWindow] = []

    for window_data in data.get("windows", []):
        tabs: List[FirefoxTab] = []
        for tab_data in window_data.get("tabs", []):
            entries: List[FirefoxNavigationEntry] = []
            for entry_data in tab_data.get("entries", []):
                entry = FirefoxNavigationEntry(
                    url=entry_data.get("url", ""),
                    title=entry_data.get("title", ""),
                    last_accessed=entry_data.get("lastAccessed"),
                    referrer=entry_data.get("referrer"),
                )
                entries.append(entry)

            tab = FirefoxTab(
                entries=entries,
                index=tab_data.get("index", 1) - 1,
                pinned=tab_data.get("pinned", False),
                is_hidden=tab_data.get("hidden", False),
            )
            tabs.append(tab)

        window = FirefoxWindow(tabs=tabs)
        windows.append(window)

    return windows


def find_latest_recovery_file(directory: str) -> Optional[Path]:
    """
    Searches the given directory for the most recently modified Firefox recovery session file.

    Looks for files matching patterns like 'recovery.jsonlz4' or 'previous.jsonlz4' in the provided directory.
    This is useful for automatically finding the latest session state of Firefox.

    Args:
        directory (str): The directory to search for session files.

    Returns:
        Optional[Path]: Path to the most recent recovery file, or None if none found.
    """
    session_path = Path(directory)
    if not session_path.exists():
        return None

    candidates = list(session_path.glob("recovery*.jsonlz4")) + list(
        session_path.glob("previous.jsonlz4")
    )

    if not candidates:
        return None

    return max(candidates, key=lambda f: f.stat().st_mtime)


if __name__ == "__main__":
    session_path = find_latest_recovery_file(
        "/home/host/snap/firefox/common/.mozilla/firefox/7oq7in7a.default/sessionstore-backups"
    )

    if session_path is None:
        print("No recovery.lz4 files found")
        exit(1)

    windows = read_firefox_session(session_path)
    for window in windows:
        for tab in window.tabs:
            print(tab)
            # current = tab.current_entry()
            # if current:
            #     print(f"{current.title} — {current.url}")
