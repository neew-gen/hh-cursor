from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

SECTION_STATUSES = ("filled", "skipped", "failed", "partial")
APPLICATION_SECTION_IDS = (
    "vacancy_opened",
    "resume_selected",
    "cover_letter_filled",
)


@dataclass
class VacancySnapshot:
    url: str = ""
    title: str = ""
    company: str = ""
    requirements: List[str] = field(default_factory=list)
    key_skills: List[str] = field(default_factory=list)
    extracted_at: str = ""


@dataclass
class CoverLetter:
    text: str = ""
    language: str = "ru"
    char_count: int = 0


@dataclass
class ApplicationPlan:
    composed_at: str = ""
    vacancy: VacancySnapshot = field(default_factory=VacancySnapshot)
    source_profile: str = ""
    target_role: str = ""
    resume_match_hint: str = ""
    cover_letter: CoverLetter = field(default_factory=CoverLetter)
    rewrite_applied: bool = False
    intelligence_path: Optional[str] = None
    intelligence_freshness: Optional[str] = None
    intelligence_citations: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)


@dataclass
class SectionStatus:
    section_id: str
    status: str
    notes: str = ""


@dataclass
class ApplicationReport:
    reported_at: str = ""
    application_plan_path: str = ""
    submitted: bool = False
    sections: List[SectionStatus] = field(default_factory=list)
    blockers: List[str] = field(default_factory=list)
