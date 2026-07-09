from __future__ import annotations

import re
from urllib.parse import urlparse

from resume_profile.slug import slugify_target_role


def vacancy_slug_from_url(url: str) -> str:
    text = url.strip()
    if not text:
        return "vacancy-unknown"

    match = re.search(r"/vacancy/(\d+)", text)
    if match:
        return f"vacancy-{match.group(1)}"

    parsed = urlparse(text)
    path = parsed.path or text
    tail = path.rstrip("/").split("/")[-1]
    if tail and tail != "vacancy":
        slug = slugify_target_role(tail)
        if slug != "profile":
            return f"vacancy-{slug}"

    return "vacancy-unknown"


def vacancy_slug_from_snapshot(url: str, company: str, title: str) -> str:
    slug = vacancy_slug_from_url(url)
    if slug != "vacancy-unknown":
        return slug
    combined = f"{company}-{title}".strip("-")
    if combined:
        return f"vacancy-{slugify_target_role(combined)}"
    return "vacancy-unknown"
