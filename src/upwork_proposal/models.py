from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

SECTION_STATUSES = ("filled", "skipped", "failed", "partial")
PROPOSAL_SECTION_IDS = (
    "job_opened",
    "cover_letter_filled",
    "screening_questions_filled",
    "contract_terms_filled",
)


@dataclass
class JobSnapshot:
    url: str = ""
    title: str = ""
    client: str = ""
    description: str = ""
    budget_type: str = ""
    key_skills: List[str] = field(default_factory=list)
    screening_questions: List[str] = field(default_factory=list)
    extracted_at: str = ""


@dataclass
class ProposalCoverLetter:
    text: str = ""
    language: str = "en"
    char_count: int = 0


@dataclass
class ScreeningAnswer:
    question: str = ""
    answer: str = ""


@dataclass
class ContractTerms:
    bid_type: Optional[str] = None
    hourly_rate: Optional[str] = None
    fixed_price: Optional[str] = None
    duration: Optional[str] = None
    weekly_hours: Optional[str] = None
    milestones: List[str] = field(default_factory=list)
    connects_required: Optional[int] = None


@dataclass
class ProposalPlan:
    composed_at: str = ""
    job: JobSnapshot = field(default_factory=JobSnapshot)
    source_profile: str = ""
    target_role: str = ""
    profile_match_hint: str = ""
    cover_letter: ProposalCoverLetter = field(default_factory=ProposalCoverLetter)
    screening_answers: List[ScreeningAnswer] = field(default_factory=list)
    contract_terms: Optional[ContractTerms] = None
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
class ProposalReport:
    reported_at: str = ""
    proposal_plan_path: str = ""
    submitted: bool = False
    sections: List[SectionStatus] = field(default_factory=list)
    blockers: List[str] = field(default_factory=list)
