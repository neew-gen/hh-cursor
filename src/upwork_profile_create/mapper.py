from __future__ import annotations

from dataclasses import dataclass

from upwork_profile_create.validator import normalize_date


@dataclass(frozen=True)
class FormFieldMapping:
    field_id: str
    upwork_block: str
    upwork_step: int
    selector: str
    selector_fallback: str


FORM_MAPPINGS: tuple[FormFieldMapping, ...] = (
    FormFieldMapping(
        "profile_title",
        "Title",
        1,
        '[data-test="profile-title-input"]',
        "Title",
    ),
    FormFieldMapping(
        "hourly_rate",
        "Hourly rate",
        2,
        '[data-test="hourly-rate-input"]',
        "Hourly rate",
    ),
    FormFieldMapping(
        "overview",
        "Overview",
        3,
        '[data-test="overview-textarea"]',
        "Overview",
    ),
    FormFieldMapping(
        "skills",
        "Skills",
        4,
        '[data-test="skills-input"]',
        "Skills",
    ),
    FormFieldMapping(
        "work_experience",
        "Employment History",
        5,
        '[data-test="employment-add"]',
        "Add employment",
    ),
)



def list_form_mappings() -> list[dict[str, str | int]]:
    return [
        {
            "field_id": mapping.field_id,
            "upwork_block": mapping.upwork_block,
            "upwork_step": mapping.upwork_step,
            "selector": mapping.selector,
            "selector_fallback": mapping.selector_fallback,
        }
        for mapping in FORM_MAPPINGS
    ]


def format_date_for_form(value: str | None) -> str:
    return normalize_date(value)
