from __future__ import annotations

import re

CYRILLIC_TO_LATIN = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "e",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "h",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "sch",
    "ъ": "",
    "ы": "y",
    "ь": "",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}


def slugify_profile_title(profile_title: str) -> str:
    text = profile_title.strip().lower()
    if not text:
        return "profile"

    parts: list[str] = []
    for char in text:
        if char in CYRILLIC_TO_LATIN:
            parts.append(CYRILLIC_TO_LATIN[char])
        elif char.isascii() and char.isalnum():
            parts.append(char)
        else:
            parts.append("-")

    slug = re.sub(r"-+", "-", "".join(parts)).strip("-")
    return slug or "profile"
