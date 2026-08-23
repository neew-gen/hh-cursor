from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

FILL_MODES = ("create_new", "edit_existing")
SECTION_STATUSES = ("filled", "skipped", "failed", "partial")

CREATE_ENTRY_URL = "https://www.upwork.com/freelancer/settings/profile"


@dataclass
class WorkExperienceEntry:
    company: str = ""
    position: str = ""
    start_date: str = ""
    end_date: Optional[str] = None
    is_current: bool = False
    description: str = ""
    provenance: str = "from_user_answer"


@dataclass
class SourceStats:
    profile_link_used: bool = False
    fields_from_link: int = 0
    fields_from_user: int = 0


@dataclass
class UpworkProfile:
    collected_at: str = ""
    input_mode: str = "questionnaire_only"
    profile_link: Optional[str] = None
    profile_title: str = ""
    overview: Optional[str] = None
    hourly_rate: Optional[str] = None
    work_experience: List[WorkExperienceEntry] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    portfolio_links: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    sources: SourceStats = field(default_factory=SourceStats)


@dataclass
class RewriteApplied:
    overview: bool = False
    profile_title: bool = False
    work_experience_descriptions: bool = False
    skills_tags: bool = False


@dataclass
class IntelligenceBrief:
    generated_at: Optional[str] = None
    what_to_write: List[str] = field(default_factory=list)
    how_to_build_profile: List[str] = field(default_factory=list)
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
    profile: UpworkProfile
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
