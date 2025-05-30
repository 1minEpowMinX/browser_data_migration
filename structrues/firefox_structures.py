from dataclasses import dataclass
from typing import Optional

from structrues import base_structures


@dataclass
class FirefoxNavigationEntry(base_structures.BaseNavigationEntry):
    """
    Extends BaseNavigationEntry with Firefox-specific metadata.

    Attributes:
        url (str): The visited URL.
        title (str): Title of the page at the time of visit.
        last_accessed (Optional[int]): Timestamp of when the tab was last active.
        referrer (Optional[str]): Referring URL, if available.
    """

    last_accessed: Optional[int] = None
    referrer: Optional[str] = None


@dataclass
class FirefoxTab(base_structures.BaseTab[FirefoxNavigationEntry]):
    """
    Extends BaseTab with Firefox-specific metadata.

    Attributes:
        entries (List[FirefoxNavigationEntry]): The list of navigation entries (tab history).
        index (int): The index of the current navigation entry.
        pinned (Optional[bool]): Whether the tab is pinned.
        is_hidden (Optional[bool]): Whether the tab is hidden in the tab strip.
    """

    pinned: Optional[bool] = False
    is_hidden: Optional[bool] = False


@dataclass
class FirefoxWindow(base_structures.BaseWindow[FirefoxTab]):
    """
    Firefox-specific implementation of a browser window.

    Inherits the `tabs` attribute from BaseWindow, typed as List[FirefoxTab].
    No need to override `tabs` here because the generic base class
    already specifies the correct type.
    """

    pass
