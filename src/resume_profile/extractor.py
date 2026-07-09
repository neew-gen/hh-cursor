from __future__ import annotations

import html
import re
from typing import Any

from resume_profile.models import (
    EducationEntry,
    LanguageEntry,
    ResumeProfile,
    SkillEntry,
    SourceStats,
    WorkExperienceEntry,
    WorkPreferences,
)

HH_RESUME_LINK_PATTERN = re.compile(
    r"^https?://([a-z0-9-]+\.)?hh\.ru/resume/[a-zA-Z0-9]+",
    re.IGNORECASE,
)

MONTH_YEAR_PATTERN = re.compile(
    r"(\d{1,2})\.(\d{4})|(\d{4})-(\d{2})|([а-яa-z]+)\s+(\d{4})",
    re.IGNORECASE,
)

SKILL_LEVEL_MAP = {
    "базовый": "basic",
    "basic": "basic",
    "средний": "medium",
    "medium": "medium",
    "продвинутый": "advanced",
    "advanced": "advanced",
}

CURRENT_END_MARKERS = (
    "по настоящее время",
    "настоящее время",
    "present",
    "сейчас",
)

SKILL_NOISE_NAMES = {
    "продвинутый уровень",
    "средний уровень",
    "...",
    "указать уровни",
    "редактировать",
    "посмотреть всё",
    "посмотреть все",
    "знание языков",
    "навыки",
}


def is_valid_hh_resume_link(url: str) -> bool:
    return bool(HH_RESUME_LINK_PATTERN.match(url.strip()))


def _normalize_level(raw: str) -> str:
    key = raw.strip().lower()
    return SKILL_LEVEL_MAP.get(key, "medium")


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


def _dedupe_work_entries(entries: list[WorkExperienceEntry]) -> list[WorkExperienceEntry]:
    unique: list[WorkExperienceEntry] = []
    seen: set[tuple[str, str, str, str | None, bool, str]] = set()
    for entry in entries:
        key = (
            entry.company.strip().lower(),
            entry.position.strip().lower(),
            entry.start_date.strip().lower(),
            (entry.end_date or "").strip().lower() or None,
            entry.is_current,
            entry.description.strip().lower(),
        )
        if key in seen:
            continue
        seen.add(key)
        unique.append(entry)
    return unique


def _dedupe_skill_entries(entries: list[SkillEntry]) -> list[SkillEntry]:
    unique: list[SkillEntry] = []
    seen: set[str] = set()
    for entry in entries:
        key = entry.name.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        unique.append(entry)
    return unique


def _dedupe_language_entries(entries: list[LanguageEntry]) -> list[LanguageEntry]:
    unique: list[LanguageEntry] = []
    seen: set[str] = set()
    for entry in entries:
        key = entry.name.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        unique.append(entry)
    return unique


def extract_resume_content(content: str, resume_link: str | None = None) -> ResumeProfile:
    lowered = content.lower()
    if "<html" in lowered and "resume-experience" in lowered:
        return extract_from_download_html(content, resume_link=resume_link)
    return extract_from_page_text(content, resume_link=resume_link)


def extract_from_download_html(html_content: str, resume_link: str | None = None) -> ResumeProfile:
    profile = ResumeProfile(
        input_mode="questionnaire_with_link" if resume_link else "questionnaire_only",
        resume_link=resume_link,
    )

    role_match = re.search(
        r'<p[^>]*class="resume__position"[^>]*>(.*?)</p>',
        html_content,
        re.DOTALL | re.IGNORECASE,
    )
    if role_match:
        profile.target_role = _html_to_text(role_match.group(1))

    specializations = re.findall(
        r'<li[^>]*class="resume-profession-role"[^>]*>(.*?)</li>',
        html_content,
        re.DOTALL | re.IGNORECASE,
    )
    profile.specializations = _dedupe_preserve_order(
        [_html_to_text(item) for item in specializations if _html_to_text(item)]
    )

    experiences = _extract_work_experience_from_download_html(html_content)
    if experiences:
        profile.work_experience = _dedupe_work_entries(experiences)
        profile.work_experience_status = "has_experience"

    education = _extract_education_from_download_html(html_content)
    if education:
        profile.education = education

    skills = _extract_skills_from_download_html(html_content)
    if skills:
        profile.skills_hard = _dedupe_skill_entries(skills)

    languages = _extract_languages_from_download_html(html_content)
    if languages:
        profile.languages = _dedupe_language_entries(languages)

    about = _extract_about_me_from_download_html(html_content)
    if about:
        profile.about_me = about

    link_fields = sum(
        1
        for value in (
            bool(profile.target_role),
            bool(profile.skills_hard),
            bool(profile.work_experience),
            bool(profile.education),
            bool(profile.about_me),
        )
        if value
    )
    profile.sources = SourceStats(
        resume_link_used=bool(resume_link),
        fields_from_link=link_fields,
        fields_from_user=0,
    )
    return profile


def extract_from_page_text(text: str, resume_link: str | None = None) -> ResumeProfile:
    profile = ResumeProfile(
        input_mode="questionnaire_with_link" if resume_link else "questionnaire_only",
        resume_link=resume_link,
    )
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    joined = "\n".join(lines)

    role = _extract_target_role(lines, joined)
    if role:
        profile.target_role = role

    skills = _extract_skills(joined)
    if skills:
        profile.skills_hard = _dedupe_skill_entries(skills)

    experiences = _extract_work_experience(joined)
    if experiences:
        profile.work_experience = _dedupe_work_entries(experiences)
        profile.work_experience_status = "has_experience"

    education = _extract_education(joined)
    if education:
        profile.education = education

    about = _extract_about_me(joined)
    if about:
        profile.about_me = about

    link_fields = sum(
        1
        for value in (
            bool(profile.target_role),
            bool(profile.skills_hard),
            bool(profile.work_experience),
            bool(profile.education),
            bool(profile.about_me),
        )
        if value
    )
    profile.sources = SourceStats(
        resume_link_used=bool(resume_link),
        fields_from_link=link_fields,
        fields_from_user=0,
    )
    return profile


def _extract_target_role(lines: list[str], joined: str) -> str:
    for marker in ("желаемая должность", "desired position"):
        match = re.search(rf"{marker}[:\s]+(.+)", joined, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    for line in lines[:8]:
        if len(line) > 3 and not line.lower().startswith(("опыт", "образование", "навыки")):
            return line
    return ""


DEFAULT_SECTION_STOP_MARKERS = (
    "опыт работы",
    "образование",
    "ключевые навыки",
    "навыки",
    "языки",
)

ABOUT_ME_STOP_MARKERS = (
    "повышение квалификации",
    "курсы",
    "портфолио",
    "пройденные тесты",
    "подтверждение навыков",
    "сканируйте qr",
    "headhunter",
    "скачать приложение",
)


def _html_to_text(fragment: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", fragment, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).strip()


def _is_current_end_token(token: str) -> bool:
    normalized = token.strip().lower()
    return normalized in CURRENT_END_MARKERS or normalized.startswith("настоящее время")


def _is_skill_noise(name: str) -> bool:
    normalized = name.strip().lower()
    return not normalized or normalized in SKILL_NOISE_NAMES or normalized.startswith("посмотреть")


def _parse_date_range(text: str) -> tuple[str, str | None, bool]:
    match = re.search(
        r"([А-Яа-яA-Za-z]+\s+\d{4})\s*[-—]\s*"
        r"((?:[А-Яа-яA-Za-z]+\s+\d{4})|(?:по\s+)?настоящее\s+время|present|сейчас)",
        text,
        re.IGNORECASE,
    )
    if not match:
        return "", None, False
    start_date = _normalize_date_token(match.group(1))
    end_token = match.group(2).strip()
    if _is_current_end_token(end_token):
        return start_date, None, True
    return start_date, _normalize_date_token(end_token), False


def _extract_work_experience_from_download_html(html_content: str) -> list[WorkExperienceEntry]:
    entries: list[WorkExperienceEntry] = []
    for block in re.findall(
        r'<li[^>]*class="resume-experience"[^>]*>(.*?)</li>',
        html_content,
        re.DOTALL | re.IGNORECASE,
    ):
        company_match = re.search(
            r'<span[^>]*class="resume-experience__company"[^>]*>\s*(.*?)\s*</span>',
            block,
            re.DOTALL | re.IGNORECASE,
        )
        position_match = re.search(
            r'<p[^>]*class="resume-experience__position"[^>]*>(.*?)</p>',
            block,
            re.DOTALL | re.IGNORECASE,
        )
        hint_match = re.search(
            r'<p[^>]*class="bloko-form-hint"[^>]*>\s*(.*?)\s*</p>',
            block,
            re.DOTALL | re.IGNORECASE,
        )
        description_match = re.search(
            r'<p[^>]*class="resume-experience__position"[^>]*>.*?</p>\s*<p[^>]*>(.*?)</p>',
            block,
            re.DOTALL | re.IGNORECASE,
        )
        if not company_match or not position_match or not hint_match or not description_match:
            continue

        company = _html_to_text(company_match.group(1))
        position = _html_to_text(position_match.group(1))
        start_date, end_date, is_current = _parse_date_range(_html_to_text(hint_match.group(1)))
        description = _html_to_text(description_match.group(1))
        if not company or not position or not start_date or not description:
            continue

        entries.append(
            WorkExperienceEntry(
                company=company,
                position=position,
                start_date=start_date,
                end_date=end_date,
                is_current=is_current,
                description=description,
                provenance="from_resume_link",
            )
        )
    return entries


def _extract_education_from_download_html(html_content: str) -> list[EducationEntry]:
    entries: list[EducationEntry] = []
    education_section_match = re.search(
        r'<p[^>]*class="resume__block"[^>]*>Образование</p>\s*<ul>(.*?)</ul>',
        html_content,
        re.DOTALL | re.IGNORECASE,
    )
    if not education_section_match:
        return entries

    section = education_section_match.group(1)
    for match in re.finditer(
        r'<li[^>]*class="resume-education"[^>]*>(.*?)</li>\s*(?:<p[^>]*>(.*?)</p>)?',
        section,
        re.DOTALL | re.IGNORECASE,
    ):
        block = match.group(1)
        specialty = _html_to_text(match.group(2) or "")
        institution_match = re.search(
            r'<span[^>]*class="resume-education__name"[^>]*>(.*?)</span>',
            block,
            re.DOTALL | re.IGNORECASE,
        )
        hints = [
            _html_to_text(item)
            for item in re.findall(
                r'<p[^>]*class="bloko-form-hint"[^>]*>(.*?)</p>',
                block,
                re.DOTALL | re.IGNORECASE,
            )
        ]
        if not institution_match:
            continue

        institution = _html_to_text(institution_match.group(1))
        graduation_year = None
        degree = ""
        for hint in hints:
            year_match = re.fullmatch(r"(19|20)\d{2}", hint)
            if year_match:
                graduation_year = int(year_match.group(0))
            elif hint:
                degree = hint

        entries.append(
            EducationEntry(
                institution=institution,
                degree=degree,
                specialty=specialty,
                graduation_year=graduation_year,
                provenance="from_resume_link",
            )
        )
    return entries


def _extract_skills_from_download_html(html_content: str) -> list[SkillEntry]:
    skills_match = re.search(
        r'<span[^>]*class="bloko-form-hint"[^>]*>Навыки</span>\s*<p[^>]*class="(?:resume-skils|resume-skills)__item"[^>]*>(.*?)</p>',
        html_content,
        re.DOTALL | re.IGNORECASE,
    )
    if not skills_match:
        return []

    raw_names = re.findall(
        r"<span>\s*(.*?)\s*</span>",
        skills_match.group(1),
        re.DOTALL | re.IGNORECASE,
    )
    entries: list[SkillEntry] = []
    seen: set[str] = set()
    for raw_name in raw_names:
        name = _html_to_text(raw_name).rstrip(";").strip()
        if _is_skill_noise(name):
            continue
        key = name.lower()
        if key in seen:
            continue
        seen.add(key)
        entries.append(SkillEntry(name=name, level="", provenance="from_resume_link"))
    return entries


def _extract_languages_from_download_html(html_content: str) -> list[LanguageEntry]:
    languages_match = re.search(
        r'<span[^>]*class="bloko-form-hint"[^>]*>Знание языков</span>\s*<ul[^>]*class="resume-skils__item"[^>]*>(.*?)</ul>',
        html_content,
        re.DOTALL | re.IGNORECASE,
    )
    if not languages_match:
        return []

    entries: list[LanguageEntry] = []
    for block in re.findall(r"<li[^>]*>(.*?)</li>", languages_match.group(1), re.DOTALL | re.IGNORECASE):
        text = _html_to_text(block)
        if not text:
            continue
        if "—" in text:
            name, level = [part.strip() for part in text.split("—", 1)]
        else:
            name, level = text, ""
        entries.append(LanguageEntry(name=name, level=level))
    return entries


def _extract_about_me_from_download_html(html_content: str) -> str:
    about_match = re.search(
        r'<span[^>]*class="bloko-form-hint"[^>]*>Обо мне</span>\s*<p[^>]*class="resume-skils__item"[^>]*>(.*?)</p>',
        html_content,
        re.DOTALL | re.IGNORECASE,
    )
    if not about_match:
        return ""
    return _html_to_text(about_match.group(1))


def _clean_section_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]
    cleaned: list[str] = []
    for line in lines:
        if not line:
            if cleaned and cleaned[-1] != "":
                cleaned.append("")
            continue
        cleaned.append(line)
    while cleaned and cleaned[0] == "":
        cleaned.pop(0)
    while cleaned and cleaned[-1] == "":
        cleaned.pop()
    return "\n".join(cleaned)


def _extract_section_text(
    joined: str,
    markers: tuple[str, ...],
    stop_markers: tuple[str, ...] = DEFAULT_SECTION_STOP_MARKERS,
    max_length: int | None = None,
) -> str:
    lower = joined.lower()
    for marker in markers:
        start = lower.find(marker)
        if start == -1:
            continue
        chunk = joined[start + len(marker) :]
        if max_length is not None:
            chunk = chunk[:max_length]
        chunk = re.sub(r"^[:\s\-]+", "", chunk)
        end = len(chunk)
        chunk_lower = chunk.lower()
        for stop in stop_markers:
            idx = chunk_lower.find(stop)
            if idx > 0:
                end = min(end, idx)
        return _clean_section_text(chunk[:end])
    return ""


def _extract_about_me(joined: str) -> str:
    return _extract_section_text(
        joined,
        ("обо мне", "о себе", "about me"),
        stop_markers=ABOUT_ME_STOP_MARKERS,
        max_length=None,
    )


def _extract_skills(joined: str) -> list[SkillEntry]:
    section = _extract_section_text(
        joined,
        ("ключевые навыки", "навыки", "skills"),
        stop_markers=DEFAULT_SECTION_STOP_MARKERS,
        max_length=800,
    )
    if not section:
        return []

    entries: list[SkillEntry] = []
    for part in re.split(r"[,;\n•·\-–—]", section):
        name = part.strip()
        if not name or len(name) < 2:
            continue
        level_match = re.search(r"\(([^)]+)\)", name)
        level = ""
        if level_match:
            level = _normalize_level(level_match.group(1))
            name = name[: level_match.start()].strip()
        if name and not _is_skill_noise(name):
            entries.append(
                SkillEntry(name=name, level=level, provenance="from_resume_link")
            )
    return entries[:30]


def _extract_work_experience(joined: str) -> list[WorkExperienceEntry]:
    section = _extract_section_text(
        joined,
        ("опыт работы", "experience"),
        stop_markers=DEFAULT_SECTION_STOP_MARKERS,
        max_length=None,
    )
    if not section:
        return []

    date_range = re.compile(
        r"(\d{1,2}[./]\d{4}|\d{4}-\d{2}|[а-яa-z]+\s+\d{4})\s*[-–—]\s*"
        r"(\d{1,2}[./]\d{4}|\d{4}-\d{2}|[а-яa-z]+\s+\d{4}|"
        r"по настоящее время|настоящее время|present|сейчас)",
        re.IGNORECASE,
    )
    duration_line = re.compile(
        r"^\d+\s+(год|года|лет|month|months)\b.*",
        re.IGNORECASE,
    )
    company_marker = re.compile(r"^(компания|company)[:\s]+(.+)", re.IGNORECASE)
    position_marker = re.compile(r"^(должность|position)[:\s]+(.+)", re.IGNORECASE)

    lines = [line.strip() for line in section.splitlines() if line.strip()]
    if not lines:
        return []

    entries: list[WorkExperienceEntry] = []
    index = 0

    def is_probable_company_start(line_index: int) -> bool:
        if line_index >= len(lines):
            return False
        line = lines[line_index]
        if company_marker.search(line):
            return True
        if date_range.search(line) or duration_line.match(line):
            return False
        if line.startswith(("-", "•", "Стек:", "Достижения:")):
            return False
        if line_index + 2 >= len(lines):
            return False
        return bool(duration_line.match(lines[line_index + 1]) and not date_range.search(lines[line_index + 2]))

    while index < len(lines):
        if not is_probable_company_start(index):
            index += 1
            continue

        company = ""
        position = ""
        start_date = ""
        end_date: str | None = None
        is_current = False
        description_lines: list[str] = []

        company_match = company_marker.search(lines[index])
        if company_match:
            company = company_match.group(2).strip()
            index += 1
        else:
            company = lines[index]
            index += 1

        if index < len(lines) and duration_line.match(lines[index]):
            index += 1

        if index < len(lines):
            position_match = position_marker.search(lines[index])
            if position_match:
                position = position_match.group(2).strip()
                index += 1
            elif not date_range.search(lines[index]):
                position = lines[index]
                index += 1

        while index < len(lines):
            line = lines[index]
            if description_lines and is_probable_company_start(index):
                break

            range_match = date_range.search(line)
            if range_match and not start_date:
                start_date = _normalize_date_token(range_match.group(1))
                end_token = range_match.group(2)
                if _is_current_end_token(end_token):
                    is_current = True
                    end_date = None
                else:
                    end_date = _normalize_date_token(end_token)
                index += 1
                continue
            description_lines.append(line)
            index += 1

        description = "\n".join(description_lines).strip()
        if company and position and start_date and description:
            entries.append(
                WorkExperienceEntry(
                    company=company,
                    position=position,
                    start_date=start_date,
                    end_date=end_date,
                    is_current=is_current,
                    description=description,
                    provenance="from_resume_link",
                )
            )

    return entries


def _normalize_date_token(token: str) -> str:
    token = token.strip()
    dot_match = re.match(r"(\d{1,2})[./](\d{4})", token)
    if dot_match:
        return f"{dot_match.group(2)}-{int(dot_match.group(1)):02d}"
    dash_match = re.match(r"(\d{4})-(\d{2})", token)
    if dash_match:
        return f"{dash_match.group(1)}-{dash_match.group(2)}"
    return token


def _extract_education(joined: str) -> list[EducationEntry]:
    section = _extract_section_text(
        joined,
        ("образование", "education"),
        stop_markers=DEFAULT_SECTION_STOP_MARKERS,
        max_length=800,
    )
    if not section:
        return []

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
