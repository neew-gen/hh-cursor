from __future__ import annotations

from resume_profile.models import GapField

GAP_QUESTIONS: dict[str, str] = {
    "target_role": "Какая желаемая должность указана в резюме?",
    "specializations": "Укажите специализации (до 5), через запятую.",
    "work_experience_status": "Есть ли у вас опыт работы? (да / нет)",
    "work_experience": (
        "Опишите место работы: компания, должность, период (месяц/год), "
        "обязанности и достижения."
    ),
    "skills.hard": (
        "Какие ключевые навыки и уровень владения "
        "(базовый / средний / продвинутый)?"
    ),
    "education": (
        "Где вы учились: учебное заведение, специальность, степень, год окончания?"
    ),
    "no_formal_education": "Нет формального образования для указания в резюме? (да / нет)",
    "about_me": (
        "Расскажите о себе для блока «Обо мне» на hh.ru "
        "(можно несколько абзацев)."
    ),
}

MVP_GAP_FIELD_IDS = (
    "target_role",
    "work_experience_status",
    "work_experience",
    "skills.hard",
    "education",
    "no_formal_education",
    "about_me",
)

FORBIDDEN_ARTIFACT_KEYS = frozenset({"key_phrases", "tools"})


def gap_field(field_id: str, required: bool = True) -> GapField:
    question = GAP_QUESTIONS.get(field_id, f"Укажите значение для поля {field_id}.")
    return GapField(field_id=field_id, question=question, required=required)
