from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass(frozen=True)
class SourceDescriptor:
    id: str
    title: str
    url: str
    source_class: str
    trust_tier: str
    topics: List[str]


@dataclass
class SourceFetchResult:
    descriptor: SourceDescriptor
    status: str
    fetched_at: datetime
    text: str = ""
    http_status: Optional[int] = None
    error_message: Optional[str] = None


@dataclass(frozen=True)
class EvidenceClaim:
    claim_text: str
    section: str
    confidence: str
    trust_tier: str
    source_id: str
    topic: str


@dataclass(frozen=True)
class RecommendationItem:
    recommendation_text: str
    target: str
    rationale: str
    confidence: str
    supporting_sources: List[str]
    conflict_note: Optional[str] = None


@dataclass
class ResumeIntelligenceReport:
    summary_points: List[str] = field(default_factory=list)
    screening_findings: List[RecommendationItem] = field(default_factory=list)
    content_recommendations: List[RecommendationItem] = field(default_factory=list)
    format_recommendations: List[RecommendationItem] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    source_notes: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    generated_at: Optional[datetime] = None
    artifact_path: str = ""


@dataclass
class PipelineRun:
    started_at: datetime
    finished_at: datetime
    requested_sources: int
    successful_sources: int
    failed_sources: int
    artifact_path: str
