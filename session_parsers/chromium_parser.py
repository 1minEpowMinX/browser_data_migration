from io import BytesIO
from struct import unpack
from pathlib import Path
from typing import Optional

from structrues.chormium_structures import (
    ChromiumNavigationEntry,
    ChromiumTab,
    ChromiumWindow,
)


## Chrome Session Format
# Chrome stores session state by appending binary commands to a session file.
# These commands are used to reconstruct the session upon browser restart.
# This format is internal and may change in future Chrome versions.

# File layout:
#   "SNSS"                                # Magic header
#   int32 version (typically 3)
#   <command>...

# Each command format:
#   int16(size)
#   int8(type_id)
#   payload (size-1 bytes, pickled struct)

# Source:
# https://source.chromium.org/chromium/chromium/src/+/main:components/sessions/core/session_service_commands.cc


# (Payload) Pickle order (basic structure without command specifics, etc.):

# index_
# virtual_url_
# title_
# encoded_page_state_
# transition_type_

# Added on later:

# type_mask (has_post_data_)
# referrer_url_
# referrer_policy_ (broken, crbug.com/450589)
# original_request_url_
# is_overriding_user_agent_
# timestamp_
# search_terms_ (removed)
# http_status_code_
# referrer_policy_
# extended_info_map_

# Source:
# SerializedNavigationEntry::WriteToPickle()
# https://source.chromium.org/chromium/chromium/src/+/main:components/sessions/core/serialized_navigation_entry.cc;l=116


def read_uint8(f) -> int:
    return unpack("<B", f.read(1))[0]


def read_uint16(f) -> int:
    return unpack("<H", f.read(2))[0]


def read_uint32(f) -> int:
    return unpack("<I", f.read(4))[0]


def read_uint64(f) -> int:
    return unpack("<Q", f.read(8))[0]


def read_bytestring(f: BytesIO) -> bytes:
    sz = read_uint32(f)
    pad = (4 - sz % 4) % 4
    bytestring = f.read(sz)
    f.read(pad)  # skip padding
    return bytestring


def read_string(f) -> str:
    sz = read_uint32(f)
    pad = (4 - sz % 4) % 4
    string = f.read(sz).decode("utf-8", errors="replace")
    f.read(pad)  # skip padding
    return string


def read_string16(f) -> str:
    sz = read_uint32(f)
    bytelen = sz * 2
    pad = (4 - bytelen % 4) % 4
    raw = f.read(bytelen)
    string = raw.decode("utf-16-le", errors="replace")
    f.read(pad)  # skip padding
    return string


def parse_navigation_entry(buf: BytesIO, tab: ChromiumTab) -> None:
    """
    Parses a Chrome SNSS command of type 6 (kCommandUpdateTabNavigation) and appends a navigation
    entry to the provided Tab object.

    The function reads binary payload data corresponding to a tab's navigation update, including
    tab ID, history index, URL, title, and optionally referrer, timestamp, transition type,
    POST status, original URL, and user-agent override flag. Missing fields are safely ignored.

    Args:
        buf (io.BytesIO): A BytesIO object containing the binary payload data.
        tab (Tab): The tab object to which the navigation entry should be appended.
                   If the tab lacks an ID or index, they will be set from the payload.

    Raises:
        ValueError: If the payload cannot be parsed correctly.
        ValueError: If the tab is None.
    """

    try:
        _ = read_uint32(
            buf
        )  # skip the tab index because the value is duplicated in the payload
        # if tab.index is None: May be use this in future to set index or update index
        #     tab.index = index

        url = read_string(buf)
        title = read_string16(buf)

        # this field is currently unused but reserved for future support
        _ = read_bytestring(buf)  # encoded_page_state_

        transition_type = read_uint32(buf)
        has_post_data = read_uint32(buf) > 0

        referrer = read_string(buf)
        _ = read_uint32(buf)  # referrer_policy_ (broken, crbug.com/450589)

        original_request_url = read_string(buf)
        is_overriding_user_agent = read_uint32(buf) > 0

    except:
        raise ValueError("Failed to parse navigation entry")

    if tab is None:
        raise ValueError("Tab not found")

    tab.entries.append(
        ChromiumNavigationEntry(
            url=url,
            title=title,
            transition_type=transition_type,
            has_post_data=has_post_data,
            referrer=referrer,
            original_request_url=original_request_url,
            is_overriding_user_agent=is_overriding_user_agent,
        )
    )


def parse_snss_file(path: Path | str) -> ChromiumWindow:
    """
    Parses a Chrome SNSS session file and extracts window/tab/navigation structure.

    This function reads and validates the SNSS file format (used in Chromium-based browsers
    for session persistence, e.g. "Current Session" or "Last Session"). It processes
    commands of type 6 (kCommandUpdateTabNavigation) to reconstruct tab histories. Additionally,
    It also processes commands of type 7 (kCommandSetSelectedNavigationIndex) to group tabs into windows.

    The function groups all tabs into a single Window object, as Chromium's SNSS format does not
    explicitly separate windows (though tabs contain IDs that may allow grouping in the future).

    Args:
        path (Path | str): Path to the SNSS file to parse.

    Raises:
        ValueError: If the file does not start with the expected "SNSS" signature.
        ValueError: If the SNSS version is not supported (currently only version 3 is supported).

    Returns:
        ChromiumWindow: A specific ChromiumWindow object containing the parsed Tab objects with their navigation entries.
    """

    with open(path, "rb") as f:
        if f.read(4) != b"SNSS":
            raise ValueError("Invalid SNSS signature")
        version = read_uint32(f)
        if version != 3:
            raise ValueError(f"Unsupported SNSS version: {version}")

        tabs: dict[int, ChromiumTab] = {}

        while True:
            size_bytes = f.read(2)
            if len(size_bytes) < 2:
                break
            size = unpack("<H", size_bytes)[0]
            if size == 0:
                break
            command_type = read_uint8(f)
            payload = f.read(size - 1)
            buf = BytesIO(payload)

            match command_type:
                case 6:  # kCommandUpdateTabNavigation
                    _ = read_uint32(buf)  # pickle header size
                    tab_id = read_uint32(buf)
                    if tab_id not in tabs:
                        tabs[tab_id] = ChromiumTab(entries=[], tab_id=tab_id)
                    parse_navigation_entry(buf, tabs[tab_id])

                case 7:  # kCommandSetSelectedNavigationIndex
                    tab_id = read_uint32(buf)
                    selected_index = read_uint32(buf)
                    if tab_id not in tabs:
                        tabs[tab_id] = ChromiumTab(entries=[], tab_id=tab_id)
                    tabs[tab_id].index = selected_index

    window = ChromiumWindow(tabs=list(tabs.values()))
    return window
