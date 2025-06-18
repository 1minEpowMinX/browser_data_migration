from utils.logger import logger
from platform import system
from pathlib import Path
from rich.prompt import IntPrompt
from typing import Optional, Iterable
from ui.console import (
    console,
    print_warning,
)

WINDOWS_CHROME = Path("AppData/Local/Google/Chrome/User Data")
WINDOWS_EDGE = Path("AppData/Local/Microsoft/Edge/User Data")
WINDOWS_FIREFOX = Path("AppData/Roaming/Mozilla/Firefox/Profiles")

LINUX_CHROME = Path(".config/google-chrome")
LINUX_EDGE = Path(".config/microsoft-edge")
LINUX_FIREFOX = Path(".mozilla/firefox")


def get_user_profiles() -> list[Path]:
    """
    Get a list of user profiles based on the operating system.

    This function returns a list of user profile names for the current operating system.
    It uses environment variables for Windows paths and expands user directories for Linux paths.

    Raises:
        NotImplementedError: If the operating system is unknown.

    Returns:
        list[str]: A list of user profile names.
    """

    system_name = system()
    if system_name == "Windows":
        base_path = Path("C:/Users")
    elif system_name == "Linux":
        base_path = Path("/home")
    else:
        raise NotImplementedError(f"Error: Unknown OS type")

    return [p for p in base_path.iterdir() if p.is_dir()]


def select_user_profile(profiles: list[Path]) -> Optional[Path]:
    """
    Select a user profile from a list of available profiles.

    This function prompts the user to select a user profile from a list of available profiles.
    It returns the selected user profile path if one is selected, or None if no profile is selected.

    Args:
        profiles (list[Path]): A list of user profile paths.

    Raises:
        ValueError: If no user profiles are found.
        Exception: Throwing the exception above.

    Returns:
        Optional[Path]: The selected user profile path, or None if no profile is selected.
    """

    if not profiles:
        raise ValueError("No user profiles found.")

    console.print("\n[bold cyan]Выберите профиль пользователя:[/bold cyan]")
    for idx, profile in enumerate(profiles, start=1):
        console.print(f"[bold green]{idx}.[/bold green] {profile.name}")

    while True:
        try:
            selection = IntPrompt.ask(
                "\n[bold cyan]Введите номер:[/bold cyan]",
                default=1,
                choices=[str(n) for n in range(1, len(profiles) + 1)],
            )
            if 1 <= selection <= len(profiles):
                return profiles[selection - 1]
            else:
                print_warning("Номер вне диапазона. Попробуйте снова.")
        except Exception as e:
            logger.error(f"Error selecting user profile: {e}")
            raise


def get_browser_profile_path(user_path: Path, browser: str) -> Optional[Path]:
    """
    Get the default path for browser profiles based on the operating system and browser type.

    This function determines the default path for browser profiles based on the operating system
    and browser type (e.g., Chrome, Edge, Firefox).

    Args:
        user_path (Path): The path to the user directory.
        browser (str): The name of the browser (e.g., "Chrome", "Edge", "Firefox").

    Raises:
        NotImplementedError: If the browser is unknown or not supported on the current OS.

    Returns:
        Optional[Path]: The path to the browser profile directory, or None if the browser is not supported.
    """

    match system():
        case "Windows":
            if browser == "Chrome":
                return user_path / WINDOWS_CHROME
            elif browser == "Edge":
                return user_path / WINDOWS_EDGE
            elif browser == "Firefox":
                return user_path / WINDOWS_FIREFOX
            else:
                raise NotImplementedError(
                    f"Error: Unknown browser {browser} for Windows"
                )
        case "Linux":
            if browser == "Chrome":
                return user_path / LINUX_CHROME
            elif browser == "Edge":
                return user_path / LINUX_EDGE
            elif browser == "Firefox":
                return user_path / LINUX_FIREFOX
            else:
                raise NotImplementedError(f"Error: Unknown browser {browser} for Linux")
        case _:
            raise NotImplementedError("Error: Unknown OS type")


def safe_ignore_errors(src: Path | str, names: list[str]) -> list[str]:
    """
    Safely ignore files that cannot be accessed in the source directory.

    This function checks each file in the source directory and adds it to the ignore list
    if it cannot be opened. This is useful for avoiding errors when copying files.

    Args:
        src (Path | str): The source directory path.
        names (list[str]): List of file names in the source directory.

    Returns:
        list[str]: A list of file names that could not be accessed.
    """

    ignore_list = []
    src_path = Path(src)
    for name in names:
        full_path = src_path / name
        if full_path.is_dir():
            continue  # Skip directories, they will be handled by shutil.copytree
        try:
            # try to open the file to check if it is accessible
            with open(full_path, "rb"):
                pass
        except Exception:
            ignore_list.append(name)

    return ignore_list


def find_latest_file_by_patterns(
    directory: Path, patterns: Iterable[str]
) -> Optional[Path]:
    """
    Searches the given directory recursively for files matching any of the specified patterns.
    Returns the most recently modified one.

    Args:
        directory (Path): Directory to search in.
        patterns (Iterable[str]): Glob patterns to match (e.g., ["Session_*", "Recovery_*.json"]).

    Returns:
        Optional[Path]: The newest matching file, or None if none found.
    """
    if not directory.exists():
        return None

    files: list[Path] = []
    for pattern in patterns:
        files.extend(directory.rglob(pattern))

    if not files:
        return None

    return max(files, key=lambda f: f.stat().st_mtime)


def find_latest_snss_file(directory: Path) -> Optional[Path]:
    return find_latest_file_by_patterns(directory, ["Session_*"])


def find_latest_recovery_file(directory: Path) -> Optional[Path]:
    return find_latest_file_by_patterns(
        directory, ["recovery*.jsonlz4", "previous.jsonlz4"]
    )
