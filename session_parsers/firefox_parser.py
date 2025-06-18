from json import loads
from pathlib import Path
from typing import Optional

from lz4.block import decompress  # type: ignore

from structrues.firefox_structures import (
    FirefoxNavigationEntry,
    FirefoxTab,
    FirefoxWindow,
)


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


def parse_jsonlz4_file(path: Path | str) -> list[FirefoxWindow]:
    """
    Parses a Firefox session file (e.g., recovery.jsonlz4) and returns structured FirefoxWindow objects.

    The session file must begin with the `mozLz40\0` magic header and contain an LZ4-compressed JSON payload.
    The JSON structure is expected to contain a list of windows, each with tabs and navigation entries.
    The entries include URL, title, referrer, and last accessed timestamp.

    Args:
        path (Path | str): Path to the .jsonlz4 file to parse.

    Raises:
        ValueError: If the file does not start with the expected magic header.

    Returns:
        list[FirefoxWindow]: A list of FirefoxWindow objects representing the session.
    """

    with open(path, "rb") as f:
        magic = f.read(8)
        if magic != b"mozLz40\0":
            raise ValueError("Not a valid Firefox session file.")
        compressed = f.read()
        json_bytes = decompress(compressed)
        data = loads(json_bytes)

    windows: list[FirefoxWindow] = []

    for window_data in data.get("windows", []):
        tabs: list[FirefoxTab] = []
        for tab_data in window_data.get("tabs", []):
            entries: list[FirefoxNavigationEntry] = []
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
