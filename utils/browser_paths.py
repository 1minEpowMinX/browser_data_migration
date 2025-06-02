from os import path
import platform
from typing import Optional


def get_chrome_profile_path() -> Optional[str]:
    """
    Returns the default path for Chrome profiles based on the operating system.

    Raises:
            NotImplementedError: If the operating system is not supported.

    Returns:
            str: The default path for Chrome profiles.
    """

    if platform.system() == "Windows":
        return path.expandvars(r"%LOCALAPPDATA%/Google/Chrome/")
    elif platform.system() == "Linux":
        return path.expanduser("~/.config/google-chrome/")
    else:
        raise NotImplementedError("Error: Unknown OS type")


def get_edge_profile_path() -> Optional[str]:
    """
    Returns the default path for Edge profiles based on the operating system.

    Raises:
        NotImplementedError: If the operating system is not supported.

    Returns:
        str: The default path for Edge profiles.
    """

    if platform.system() == "Windows":
        return path.expandvars(r"%LOCALAPPDATA%/Microsoft/Edge/")
    elif platform.system() == "Linux":
        return path.expanduser(r"~/.config/microsoft-edge/")
    else:
        raise NotImplementedError("Error: Unknown OS type")


def get_firefox_profiles_path() -> Optional[str]:
    """
    Returns the default path for Firefox profiles based on the operating system.

    Raises:
        NotImplementedError: If the operating system is not supported.

    Returns:
        str: The default path for Firefox profiles.
    """

    if platform.system() == "Windows":
        return path.expandvars(r"%APPDATA%/Mozilla/")
    elif platform.system() == "Linux":
        return path.expanduser(r"~/snap/firefox/common/.mozilla/")
    else:
        raise NotImplementedError("Error: Unknown OS type")
