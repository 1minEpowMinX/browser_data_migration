from typing import Optional

MESSAGES_EN: dict = {}

MESSAGES_RU: dict = {}


def get_message(lang: str, key: str) -> Optional[str]:
    """
    Returns the message for the given language and key.

    This function returns the message for the given language and key.
    If the language is not supported, it returns None.

    Args:
        lang (str): selected language
        key (str): message key

    Returns:
        Optional[str]: translate message or None
    """

    if lang == "en":
        return MESSAGES_EN.get(key)
    if lang == "ru":
        return MESSAGES_RU.get(key)

    return None
