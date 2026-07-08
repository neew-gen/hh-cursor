from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


PROVENANCE_VALUES = ("from_resume_link", "from_user_answer", "inferred")
SKILL_LEVELS = ("basic", "medium", "advanced")
WORK_EXPERIENCE_STATUS = ("none", "has_experience")
INPUT_MODES = ("questionnaire_with_link", "questionnaire_only")


@dataclass
class WorkExperienceEntry:
    company: str = ""
    position: str = ""
    start_date: str = ""
    end_date: Optional[str] = None
    is_current: bool = False
    description: str = ""
    company_description: Optional[str] = None
    provenance: str = "from_user_answer"


@dataclass
class SkillEntry:
    name: str = ""
    level: str = "medium"
    provenance: str = "from_user_answer"


@dataclass
class EducationEntry:
    institution: str = ""
    degree: str = ""
    specialty: str = ""
    graduation_year: Optional[int] = None
    provenance: str = "from_user_answer"


@dataclass
class WorkPreferences:
    salary: Optional[str] = None
    employment_type: Optional[str] = None
    work_format: Optional[str] = None
    commute_time: Optional[str] = None
    business_trips: Optional[str] = None


@dataclass
class LanguageEntry:
    name: str = ""
    level: str = ""


@dataclass
class SourceStats:
    resume_link_used: bool = False
    fields_from_link: int = 0
    fields_from_user: int = 0


@dataclass
class ResumeProfile:
    collected_at: str = ""
    input_mode: str = "questionnaire_only"
    resume_link: Optional[str] = None
    target_role: str = ""
    specializations: List[str] = field(default_factory=list)
    work_experience_status: str = ""
    work_experience: List[WorkExperienceEntry] = field(default_factory=list)
    skills_hard: List[SkillEntry] = field(default_factory=list)
    skills_soft: List[SkillEntry] = field(default_factory=list)
    education: List[EducationEntry] = field(default_factory=list)
    no_formal_education: bool = False
    about_me: Optional[str] = None
    work_preferences: Optional[WorkPreferences] = None
    languages: List[LanguageEntry] = field(default_factory=list)
    additional_education: List[str] = field(default_factory=list)
    portfolio_links: List[str] = field(default_factory=list)
    personal_links: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    sources: SourceStats = field(default_factory=SourceStats)


@dataclass(frozen=True)
class GapField:
    field_id: str
    question: str
    required: bool = True
