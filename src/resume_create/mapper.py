from __future__ import annotations

from dataclasses import dataclass

from resume_create.validator import normalize_date

SKILL_LEVEL_LABELS = {
    "basic": "Базовый",
    "medium": "Средний",
    "advanced": "Продвинутый",
}


@dataclass(frozen=True)
class FormFieldMapping:
    field_id: str
    hh_block: str
    hh_step: int
    selector: str
    selector_fallback: str


FORM_MAPPINGS: tuple[FormFieldMapping, ...] = (
    FormFieldMapping(
        "target_role",
        "Профессия",
        1,
        '[data-qa="resume-profession-input"]',
        "Профессия",
    ),
    FormFieldMapping(
        "specializations",
        "Специализации",
        1,
        '[data-qa="resume-specialization"]',
        "Специализация",
    ),
    FormFieldMapping(
        "education",
        "Образование",
        2,
        '[data-qa="resume-education-add"]',
        "Добавить образование",
    ),
    FormFieldMapping(
        "no_formal_education",
        "Нет образования",
        2,
        "checkbox",
        "Нет образования",
    ),
    FormFieldMapping(
        "skills.hard",
        "Ключевые навыки",
        3,
        '[data-qa="skills-input"]',
        "Ключевые навыки",
    ),
    FormFieldMapping(
        "work_experience",
        "Опыт работы",
        4,
        '[data-qa="resume-experience-add"]',
        "Добавить место работы",
    ),
    FormFieldMapping(
        "work_preferences",
        "Условия",
        5,
        "salary/format",
        "Условия",
    ),
    FormFieldMapping(
        "about_me",
        "Обо мне",
        6,
        '[data-qa="resume-about-block"] textarea',
        "Обо мне",
    ),
    FormFieldMapping(
        "languages",
        "Языки",
        7,
        "language-block",
        "Языки",
    ),
)


def list_form_mappings() -> list[dict[str, str | int]]:
    return [
        {
            "field_id": mapping.field_id,
            "hh_block": mapping.hh_block,
            "hh_step": mapping.hh_step,
            "selector": mapping.selector,
            "selector_fallback": mapping.selector_fallback,
        }
        for mapping in FORM_MAPPINGS
    ]


def skill_level_label(level: str) -> str:
    return SKILL_LEVEL_LABELS.get(level, SKILL_LEVEL_LABELS["medium"])


def format_date_for_form(value: str | None) -> str:
    return normalize_date(value)
