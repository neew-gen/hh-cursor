from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from resume_profile.models import ResumeProfile

FILL_MODES = ("create_new", "edit_existing")
SECTION_STATUSES = ("filled", "skipped", "failed", "partial")

CREATE_ENTRY_URL = "https://hh.ru/applicant/resumes"


@dataclass
class RewriteApplied:
    about_me: bool = False
    work_experience_descriptions: bool = False


@dataclass
class IntelligenceBrief:
    generated_at: Optional[str] = None
    what_to_write: List[str] = field(default_factory=list)
    how_to_build_resume: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    source_ids: List[str] = field(default_factory=list)


@dataclass
class FillPlanMeta:
    composed_at: str = ""
    source_profile: str = ""
    intelligence_path: Optional[str] = None
    intelligence_freshness: Optional[str] = None
    fill_mode: str = "create_new"
    target_url: str = CREATE_ENTRY_URL
    rewrite_applied: RewriteApplied = field(default_factory=RewriteApplied)
    intelligence_citations: List[str] = field(default_factory=list)


@dataclass
class FillPlan:
    profile: ResumeProfile
    meta: FillPlanMeta


@dataclass
class SectionStatus:
    section_id: str
    status: str
    notes: str = ""


@dataclass
class FillReport:
    reported_at: str = ""
    fill_plan_path: str = ""
    fill_mode: str = "create_new"
    sections: List[SectionStatus] = field(default_factory=list)
    blockers: List[str] = field(default_factory=list)
    published: bool = False
