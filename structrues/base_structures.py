from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar


# Base class definitions


@dataclass
class BaseNavigationEntry:
    """
    Represents a base abstraction of a single navigation event within a browser tab.

    Attributes:
        url (str): The visited URL.
        title (str): Title of the page at the time of visit.
    """

    url: str
    title: str


TEntry = TypeVar(
    "TEntry", bound="BaseNavigationEntry"
)  # All must be a BaseNavigationEntry subclass


@dataclass
class BaseTab(Generic[TEntry]):
    """
    Represents a base abstraction of a browser tab consisting of multiple navigation entries.

    Attributes:
        entries (List[TEntry]): The list of navigation entries (tab history).
        index (int): The index of the current navigation entry.
    """

    entries: List[TEntry]
    index: int = 0

    def current_entry(self) -> Optional[TEntry]:
        """
        Returns the currently selected navigation entry based on index.

        Returns:
            Optional[TEntry]: The active entry or None if out of bounds.
        """

        if not self.entries or self.index >= len(self.entries):
            return None
        return self.entries[self.index]


TTab = TypeVar("TTab", bound="BaseTab")  # All must be a BaseTab subclass


@dataclass
class BaseWindow(Generic[TTab]):
    """
    Represents a base abstraction of a browser window containing tabs.

    Attributes:
        tabs (List[TTab]): A list of tabs in this window.
    """

    tabs: List[TTab]
