from __future__ import annotations

import re
from urllib.parse import urlparse

from resume_profile.slug import slugify_target_role


def job_slug_from_url(url: str) -> str:
    text = url.strip()
    if not text:
        return "job-unknown"

    match = re.search(r"~([0a-f]{10,})", text, re.IGNORECASE)
    if match:
        return f"job-{match.group(1).lower()}"

    parsed = urlparse(text)
    path = parsed.path or text
    tail = path.rstrip("/").split("/")[-1]
    if tail and tail not in {"jobs", "apply", "freelance-jobs"}:
        slug = slugify_target_role(tail)
        if slug != "profile":
            return f"job-{slug}"

    return "job-unknown"


def job_slug_from_snapshot(url: str, client: str, title: str) -> str:
    slug = job_slug_from_url(url)
    if slug != "job-unknown":
        return slug
    combined = f"{client}-{title}".strip("-")
    if combined:
        return f"job-{slugify_target_role(combined)}"
    return "job-unknown"
