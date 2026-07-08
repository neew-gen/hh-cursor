from __future__ import annotations

from resume_profile.models import ResumeProfile
from resume_profile.schema import GAP_QUESTIONS

DEFER_OPTION_ID = "defer_to_chat"
DEFER_OPTION_LABEL = "Отвечу в следующем сообщении"

FIXED_ASK_OPTIONS: dict[str, list[tuple[str, str]]] = {
    "work_experience_status": [
        ("has_experience", "Да, есть опыт работы"),
        ("none", "Нет опыта работы"),
    ],
    "no_formal_education": [
        ("yes", "Да, нет формального образования"),
        ("no", "Нет, есть формальное образование"),
    ],
}


def gap_question(field_id: str, profile: ResumeProfile, meta: dict | None = None) -> str:
    meta = meta or {}
    if field_id == "skills.hard" and meta.get("skills_mode") == "append":
        return "Какие навыки добавить к сохранённому профилю?"
    if field_id == "target_role":
        if profile.resume_link or profile.input_mode == "questionnaire_with_link":
            return "Какая желаемая должность указана в резюме?"
        return "Какая ваша желаемая должность?"
    return GAP_QUESTIONS.get(field_id, f"Укажите значение для поля {field_id}.")


def _draft_suggestions(field_id: str, profile: ResumeProfile) -> list[str]:
    suggestions: list[str] = []

    if field_id == "target_role" and profile.target_role.strip():
        suggestions.append(profile.target_role.strip())

    if field_id == "about_me" and (profile.about_me or "").strip():
        suggestions.append((profile.about_me or "").strip()[:120])

    return suggestions


def _option_id(label: str, index: int) -> str:
    slug = "".join(ch if ch.isalnum() else "_" for ch in label.lower()).strip("_")
    slug = slug[:40] or "option"
    return f"{slug}_{index}"


def build_ask_options(field_id: str, profile: ResumeProfile) -> list[dict[str, str]]:
    if field_id in FIXED_ASK_OPTIONS:
        return [{"id": option_id, "label": label} for option_id, label in FIXED_ASK_OPTIONS[field_id]]

    options: list[dict[str, str]] = []
    seen_labels: set[str] = set()

    for index, suggestion in enumerate(_draft_suggestions(field_id, profile)):
        if suggestion in seen_labels:
            continue
        seen_labels.add(suggestion)
        options.append({"id": _option_id(suggestion, index), "label": suggestion})

    options.append({"id": DEFER_OPTION_ID, "label": DEFER_OPTION_LABEL})
    return options
