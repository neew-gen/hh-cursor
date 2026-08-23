from __future__ import annotations

import re
from freelancer_core.models import EducationEntry, WorkExperienceEntry
from upwork_profile.models import UpworkProfile

UPWORK_PROFILE_LINK_PATTERN = re.compile(
    r"^https?://(www\.)?upwork\.com/freelancers/",
    re.IGNORECASE,
)


def is_valid_upwork_profile_link(url: str) -> bool:
    return bool(UPWORK_PROFILE_LINK_PATTERN.match(url.strip()))


def _dedupe_preserve_order(values: list[str]) -> list[str]:
    unique: list[str] = []
    seen: set[str] = set()
    for value in values:
        normalized = value.strip()
        if not normalized:
            continue
        key = normalized.lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(normalized)
    return unique


def extract_from_page_text(text: str, profile_link: str | None = None) -> UpworkProfile:
    from upwork_profile.models import UpworkProfile, UpworkSourceStats

    profile = UpworkProfile(
        input_mode="questionnaire_with_link" if profile_link else "questionnaire_only",
        profile_link=profile_link,
    )
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    joined = "\n".join(lines)

    title = _extract_profile_title(lines, joined)
    if title:
        profile.profile_title = title

    overview = _extract_overview(joined)
    if overview:
        profile.overview = overview

    rate = _extract_hourly_rate(joined)
    if rate:
        profile.hourly_rate = rate

    skills = _extract_skills(joined)
    if skills:
        profile.skills = skills

    experiences = _extract_work_experience(joined)
    if experiences:
        profile.work_experience = experiences
        profile.work_experience_status = "has_experience"

    education = _extract_education(joined)
    if education:
        profile.education = education

    portfolio = _extract_portfolio_links(joined)
    if portfolio:
        profile.portfolio_links = portfolio

    link_fields = sum(
        1
        for value in (
            bool(profile.profile_title),
            bool(profile.overview),
            bool(profile.hourly_rate),
            bool(profile.skills),
            bool(profile.work_experience),
            bool(profile.education),
        )
        if value
    )
    profile.sources = UpworkSourceStats(
        profile_link_used=bool(profile_link),
        fields_from_link=link_fields,
        fields_from_user=0,
    )
    return profile


def _extract_profile_title(lines: list[str], joined: str) -> str:
    for marker in ("profile title", "professional title", "title"):
        match = re.search(rf"{marker}[:\s]+(.+)", joined, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    for line in lines[:6]:
        if len(line) > 3 and not line.lower().startswith(
            ("overview", "skills", "experience", "education", "hourly")
        ):
            return line
    return ""


def _extract_overview(joined: str) -> str:
    for marker in ("overview", "about me", "summary"):
        start = joined.lower().find(marker)
        if start == -1:
            continue
        chunk = joined[start + len(marker) :]
        chunk = re.sub(r"^[:\s\-]+", "", chunk)
        end = len(chunk)
        chunk_lower = chunk.lower()
        for stop in ("skills", "work experience", "experience", "education", "portfolio"):
            idx = chunk_lower.find(stop)
            if idx > 0:
                end = min(end, idx)
        text = chunk[:end].strip()
        if text:
            return text
    return ""


def _extract_hourly_rate(joined: str) -> str:
    match = re.search(
        r"(?:hourly rate|rate)[:\s]*\$?\s*(\d+(?:\.\d+)?(?:\s*[-–—]\s*\$?\s*\d+(?:\.\d+)?)?)",
        joined,
        re.IGNORECASE,
    )
    if match:
        return match.group(1).strip()
    dollar_match = re.search(r"\$\s*(\d+(?:\.\d+)?(?:\s*/\s*hr)?)", joined)
    if dollar_match:
        return dollar_match.group(1).replace("/hr", "").strip()
    return ""


def _extract_skills(joined: str) -> list[str]:
    for marker in ("skills", "expertise", "tags"):
        start = joined.lower().find(marker)
        if start == -1:
            continue
        chunk = joined[start + len(marker) :]
        chunk = re.sub(r"^[:\s\-]+", "", chunk)
        end = len(chunk)
        chunk_lower = chunk.lower()
        for stop in ("experience", "education", "portfolio", "overview"):
            idx = chunk_lower.find(stop)
            if idx > 0:
                end = min(end, idx)
        section = chunk[:end].strip()
        if not section:
            continue
        parts = re.split(r"[,;\n•·\-–—]", section)
        names = [part.strip() for part in parts if part.strip() and len(part.strip()) >= 2]
        return _dedupe_preserve_order(names)[:30]
    return []


def _extract_work_experience(joined: str) -> list[WorkExperienceEntry]:
    for marker in ("work experience", "experience"):
        start = joined.lower().find(marker)
        if start == -1:
            continue
        chunk = joined[start + len(marker) :]
        chunk = re.sub(r"^[:\s\-]+", "", chunk)
        end = len(chunk)
        chunk_lower = chunk.lower()
        for stop in ("education", "skills", "portfolio", "overview"):
            idx = chunk_lower.find(stop)
            if idx > 0:
                end = min(end, idx)
        section = chunk[:end].strip()
        if not section:
            continue

        date_range = re.compile(
            r"(\d{1,2}[./]\d{4}|\d{4}-\d{2}|[a-z]+\s+\d{4})\s*[-–—]\s*"
            r"(\d{1,2}[./]\d{4}|\d{4}-\d{2}|[a-z]+\s+\d{4}|present|current)",
            re.IGNORECASE,
        )
        lines = [line.strip() for line in section.splitlines() if line.strip()]
        if len(lines) >= 2:
            company = lines[0]
            position = lines[1]
            start_date = ""
            end_date: str | None = None
            is_current = False
            description_lines: list[str] = []
            for line in lines[2:]:
                range_match = date_range.search(line)
                if range_match and not start_date:
                    start_date = range_match.group(1)
                    end_token = range_match.group(2)
                    if end_token.lower() in ("present", "current"):
                        is_current = True
                        end_date = None
                    else:
                        end_date = end_token
                else:
                    description_lines.append(line)
            description = "\n".join(description_lines).strip()
            if company and position and description:
                return [
                    WorkExperienceEntry(
                        company=company,
                        position=position,
                        start_date=start_date or "unknown",
                        end_date=end_date,
                        is_current=is_current,
                        description=description,
                        provenance="from_resume_link",
                    )
                ]
    return []


def _extract_education(joined: str) -> list[EducationEntry]:
    for marker in ("education",):
        start = joined.lower().find(marker)
        if start == -1:
            continue
        chunk = joined[start + len(marker) :]
        chunk = re.sub(r"^[:\s\-]+", "", chunk)
        end = len(chunk)
        chunk_lower = chunk.lower()
        for stop in ("skills", "experience", "portfolio", "overview"):
            idx = chunk_lower.find(stop)
            if idx > 0:
                end = min(end, idx)
        section = chunk[:end].strip()
        if not section:
            continue
        year_match = re.search(r"(19|20)\d{2}", section)
        year = int(year_match.group(0)) if year_match else None
        lines = [line.strip() for line in section.splitlines() if line.strip()]
        institution = lines[0] if lines else section[:120]
        specialty = lines[1] if len(lines) > 1 else ""
        degree = lines[2] if len(lines) > 2 else ""
        return [
            EducationEntry(
                institution=institution,
                degree=degree,
                specialty=specialty,
                graduation_year=year,
                provenance="from_resume_link",
            )
        ]
    return []


def _extract_portfolio_links(joined: str) -> list[str]:
    urls = re.findall(r"https?://[^\s,)]+", joined)
    return _dedupe_preserve_order(urls)
