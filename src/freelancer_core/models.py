from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

PROVENANCE_VALUES = ("from_resume_link", "from_user_answer", "inferred")


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
