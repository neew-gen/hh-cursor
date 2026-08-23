from __future__ import annotations

from upwork_profile.models import GapField

GAP_QUESTIONS: dict[str, str] = {
    "profile_title": "What is your Upwork profile title?",
    "overview": (
        "Write your professional overview for Upwork "
        "(skills, experience, and what you offer clients)."
    ),
    "hourly_rate": "What is your hourly rate in USD? (e.g. 50 or 50-75)",
    "skills": "List your Upwork skills/tags, separated by commas.",
    "work_experience_status": "Do you have work experience to list? (yes / no)",
    "work_experience": (
        "Describe a work experience entry: company, role, period (month/year), "
        "and responsibilities or achievements."
    ),
    "education": (
        "Where did you study: institution, degree, field of study, graduation year?"
    ),
    "portfolio_links": "Share portfolio or project links (comma-separated URLs).",
}

MVP_GAP_FIELD_IDS = (
    "profile_title",
    "overview",
    "hourly_rate",
    "skills",
    "work_experience_status",
    "work_experience",
    "education",
)

FORBIDDEN_ARTIFACT_KEYS = frozenset({"key_phrases", "tools"})


def gap_field(field_id: str, required: bool = True) -> GapField:
    question = GAP_QUESTIONS.get(field_id, f"Provide a value for field {field_id}.")
    return GapField(field_id=field_id, question=question, required=required)
