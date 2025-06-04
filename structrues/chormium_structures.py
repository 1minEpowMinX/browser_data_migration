from dataclasses import dataclass
from typing import Optional

from structrues import base_structures


@dataclass
class ChromiumNavigationEntry(base_structures.BaseNavigationEntry):
    """
    Extends BaseNavigationEntry with Chromium-specific metadata.

    Attributes:
        url (str): The visited URL.
        title (str): Title of the page at the time of visit.
        state (Optional[bytes]): A data structure provided by the WebKit engine describing the current state of the page.
                                 This field is currently unused but reserved for future support.
        transition_type (Optional[int]): Navigation type.
        has_post_data (Optional[bool]): Whether the navigation used POST.
        referrer (Optional[str]): Referring URL, if available.
        original_request_url (Optional[str]): Original URL before redirects.
        is_overriding_user_agent (Optional[bool]): Whether a custom user-agent was used.
    """

    # state: Optional[bytes] = None
    transition_type: Optional[int] = None
    has_post_data: Optional[bool] = None
    referrer: Optional[str] = None
    original_request_url: Optional[str] = None
    is_overriding_user_agent: Optional[bool] = None


@dataclass
class ChromiumTab(base_structures.BaseTab[ChromiumNavigationEntry]):
    """
    Extends BaseTab with Chromium-specific metadata.

    Attributes:
        entries (List[ChromiumNavigationEntry]): The list of navigation entries (tab history).
        index (int): The index of the current navigation entry.
        tab_id (Optional[int]): Tab identifier.
    """

    tab_id: Optional[int] = None


@dataclass
class ChromiumWindow(base_structures.BaseWindow[ChromiumTab]):
    """
    Chromium-specific implementation of a browser window.

    Inherits the `tabs` attribute from BaseWindow, typed as List[ChromiumTab].
    No need to override `tabs` here because the generic base class
    already specifies the correct type.
    """

    pass
