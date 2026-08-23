from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from freelancer_core.models import EducationEntry, WorkExperienceEntry

INPUT_MODES = ("questionnaire_with_link", "questionnaire_only")
WORK_EXPERIENCE_STATUS = ("none", "has_experience")


@dataclass
class UpworkSourceStats:
    profile_link_used: bool = False
    fields_from_link: int = 0
    fields_from_user: int = 0


@dataclass
class UpworkProfile:
    collected_at: str = ""
    input_mode: str = "questionnaire_only"
    profile_link: Optional[str] = None
    profile_title: str = ""
    overview: str = ""
    hourly_rate: Optional[str] = None
    skills: List[str] = field(default_factory=list)
    work_experience_status: str = ""
    work_experience: List[WorkExperienceEntry] = field(default_factory=list)
    education: List[EducationEntry] = field(default_factory=list)
    portfolio_links: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    sources: UpworkSourceStats = field(default_factory=UpworkSourceStats)


@dataclass(frozen=True)
class GapField:
    field_id: str
    question: str
    required: bool = True
